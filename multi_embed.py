from EmbedMethod import read_payload
from EmbedMethod import segmentation_payload

from EmbedMethod import sampling
from EmbedMethod import interpolation_linear
from EmbedMethod import fuzzifikasi

from EmbedMethod import get_unique_bit
from EmbedMethod import payload_process
from EmbedMethod import embedding

from EmbedMethod import combine
from EmbedMethod import create_stego_audio

def main():
    total_file_payload = 11
    total_file_cover_audio = 15

    folder_file_payload = 'dataset/Payload/'
    folder_file_audio = 'dataset/Audio/'
    folder_stego_audio = 'stego_audio/'
    folder_info = 'stego_audio/'

    for x in range(1, total_file_cover_audio+1):
        for y in range(1, total_file_payload+1):
            
            # init file
            audio_file = folder_file_audio + 'data' + str(x) + '_mono.wav'
            payload_file = folder_file_payload + 'payload' + str(y) + '.txt'
            stego_audio = folder_stego_audio + 'stego_audio' + str(x) + '_payload' + str(y) +'/stegoaudio.wav'

            #payload process
            binary_payload = read_payload(payload_file)
            segmented_bit ,segmented_payload = segmentation_payload(binary_payload)

            #audio process
            freame_rate, original_sample = sampling(audio_file)
            interpolated_sample = interpolation_linear(original_sample)
            bit = fuzzifikasi(interpolated_sample, original_sample)

            #embedding process
            unique_bit, index_bit = get_unique_bit(bit)
            processed_payload, divided = payload_process(segmented_bit, segmented_payload, unique_bit)
            embedded = embedding(processed_payload, index_bit, interpolated_sample, divided, index_bit[-1])

            #create output
            stego_data = combine(original_sample, embedded, interpolated_sample)
            create_stego_audio(stego_data, stego_audio)
            print('Create stego_audio'+ str(x) +'_payload'+ str(y) +'.wav SUKSES')

main()