import scipy.io.wavfile as scp
import numpy as np
import math
import copy
import os

################################################## Embedding method ##################################################

def read_payload(file_payload):
    binary_data = list(open(file_payload))[0]
    binary_data = binary_data.split('\t')
    binary_data = [x.strip('ÿþ') for x in binary_data]
    return binary_data

def segmentation_payload(binary_payload):
    binary_payload = [x.strip('\x00') for x in binary_payload]
    binary_payload = ''.join(binary_payload)

    index = 0
    segmented_bit = [] #panjang bit payload yg telah dipotong [5,3, ...]
    segmented_payload = [] #payload yg telah dipotong ['00001','001', ...]
    for x in range(1,len(binary_payload)+1):
        if(binary_payload[x-1]=='1'): # jika payload ketemu angka 1, maka cut , ex: 00001, 001, 01
            string = binary_payload[index:x]
            segmented_bit.append(len(string))
            segmented_payload.append(binary_payload[index:x])
            index = x

    return segmented_bit, segmented_payload

def sampling(file_audio):
    rate, data = scp.read(file_audio)
    data = np.add(np.int16(data),[32768])
    return rate, data

def interpolation_linear(input_sampling):
    index_odd = [x for x in range (0, (len(input_sampling)*2) - 1) if x%2 == 1]
    index_even = [x for x in range (0, (len(input_sampling)*2)) if x%2 == 0]
    interpolated_sample = np.interp(index_odd, index_even, input_sampling)
    interpolated_sample = np.floor(interpolated_sample)
    return interpolated_sample

def fuzzifikasi(interpolated_sample, original_sample):
    data = [0,16384,32768,49152,65536]
    upper = []
    lower = []
    bit = []
    for x in range (len(interpolated_sample)):
        for y in range(1, len(data)):
            if(data[y-1] <= interpolated_sample[x] < data[y]):
                up = (data[y] - interpolated_sample[x])/(data[y]-data[y-1])
                low = 1 - up
                upper.append(up)
                lower.append(low)

                selisih_up = abs(interpolated_sample[x] - original_sample[x+1])
                selisih_down = abs(interpolated_sample[x] - original_sample[x])

                total = math.floor((up * selisih_up) + (low * selisih_down))
                if total == 0:
                    bit.append(0)
                else:
                    bit.append(math.floor(math.log(total,2)))

    return bit

def get_unique_bit(bit): 
    unique_bit = []
    index = []
    for x in range(len(bit)):
        if bit[x] not in unique_bit:
            unique_bit.append(bit[x])
            index.append(x)
    print(unique_bit, index)
    return unique_bit, index

def payload_process(segmented_bit ,segmented_payload, unique_bit):
    average_bit = np.mean(unique_bit)
    new_data = [0 for x in range(len(unique_bit))] #init array of selisih
    
    for x in range(len(segmented_bit)):
        for y in range (len(unique_bit)):
            if(segmented_bit[x] == unique_bit[y]):
                new_data[y] += int(segmented_payload[x],2)
                break
    
    flag = True
    number = 0
    while flag == True:
        print(new_data)
        mod, divided, new_data = get_mod_divided(new_data, average_bit)
        flag = check_selisih(new_data, average_bit)
        number += 1
        print(new_data)
    return mod, divided, number

def check_selisih(selisih, average_bit):
    for x in selisih:
        if(x>average_bit):
            return True
    return False

def get_mod_divided(new_data, average_bit):
    divided = [math.floor(new_data[x]/average_bit) for x in range(len(new_data))]
    mod = [int(new_data[x]%average_bit) for x in range(len(new_data))]
    selisih = [mod[x]+ divided[x] for x in range(len(mod))]

    return mod, divided, selisih

def embedding(processed_payload, index_bit, interpolated_sample, divided, last_index, smooth):
    new_data = copy.copy(interpolated_sample)
    index_divided = 0
    for x in range(len(interpolated_sample)):
        for y in range(len(index_bit)):
            if(x == index_bit[y]):
                new_data[x] += processed_payload[y]
        
        if(x > last_index and x < last_index+len(divided)):
            new_data[x] += divided[index_divided]
            index_divided+=1
        if(x == len(interpolated_sample)-1):
            new_data[x]+=smooth
    return new_data

def combine(input_sampling, embed_data, data_interpolation):
    new_embed_data = [embed_data[x] if x < len(embed_data) else data_interpolation[x] for x in range (len(data_interpolation))]
    stego_data = []
    index_stego = 0
    index_sample = 0
    index_embed = 0

    for x in range (0, len(input_sampling)*2 - 1):
        if (index_stego % 2 == 0):
            stego_data.append(input_sampling[index_sample])
            index_sample += 1
        else:
            stego_data.append(new_embed_data[index_embed])
            index_embed += 1
        index_stego += 1

    return stego_data

def create_stego_audio(stego_data, filepath):
    process_1 = np.subtract(stego_data, [32768])
    stego_audio = np.array(process_1, dtype=np.int16)

    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    scp.write(filepath, 88200, stego_audio)

################################################## Extracting method ##################################################

def divide_stego_sample(data):
    cover_audio_data = [data[x] for x in range (len(data)) if x % 2 == 0]
    stego_audio_data = [data[x] for x in range (len(data)) if x % 2 == 1]
    return cover_audio_data, stego_audio_data

def differencing(unique_bit, index_bit, interpolated_sample, embedded_sample):
    average_bit = int(np.mean(unique_bit))
    times = 0 # menunjukkkan berapa kali process smoothing

    divide = [] #berisi hasil pembagian yg dibulatkan kebawah
    mod_difference = [] # berisi mod
    for x in range(len(interpolated_sample)):
        for y in range(len(unique_bit)):
            if( x == index_bit[y]):
                mod_difference.append(int(embedded_sample[x] - interpolated_sample[x]))
                break
        if(x > index_bit[-1] and x < index_bit[-1] + len(index_bit)+1):
            divide.append(int(embedded_sample[x]-interpolated_sample[x]))
        if(x == len(interpolated_sample)-1):
            times = int(embedded_sample[x]-interpolated_sample[x])

    # menghitung first smoothing yang telah diketahui
    selisih = [(divide[x] * average_bit) + mod_difference[x] for x in range(len(divide))]

    # menghitung selisih tanpa mengetahui mod dan divide nya
    data = []
    for x in range(len(selisih)):
        tmp = selisih[x] * average_bit
        dif_prob = []
        while tmp > 0:
            if(tmp%average_bit < selisih[x]):
                dif_prob.append(object)


