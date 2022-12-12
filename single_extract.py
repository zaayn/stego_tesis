from Methods import sampling
from Methods import divide_stego_sample
from Methods import interpolation_linear
from Methods import fuzzifikasi

from Methods import get_unique_bit
from Methods import differencing
from Methods import extracting

def main():
    audio = '1'
    payload = '1'
    filename = 'stego_audio'+audio+'_payload'+payload

    # init file
    stego_audio = 'stego_audio/stego_audio'+audio+'_payload'+payload+'/stegoaudio.wav'
    extracted_payload = 'extracted/stego_audio'+audio+'_payload'+payload+'/payload.txt'
    extracted_audio = 'extracted/stego_audio'+audio+'_payload'+payload+'/audio.wav'

    # audio process
    freame_rate, stego_audio_sample = sampling(stego_audio)
    original_sample, embedded_sample = divide_stego_sample(stego_audio_sample)
    interpolated_sample = interpolation_linear(original_sample)
    bit = fuzzifikasi(interpolated_sample, original_sample)

    # extracting process
    unique_bit, index_bit = get_unique_bit(bit)
    differenced, differenced2 = differencing(index_bit, interpolated_sample, embedded_sample)
    processed_payload = extracting(differenced, differenced2, unique_bit)
    

main()