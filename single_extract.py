from Methods import sampling
from Methods import divide_stego_sample
from Methods import interpolation_linear
from Methods import fuzzifikasi

from Methods import get_unique_bit
from Methods import differencing

# from Methods import combine
# from Methods import process_bit
# from Methods import create_payload
# from Methods import create_cover_audio


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
    differenced = differencing(unique_bit, index_bit, interpolated_sample, embedded_sample)

    # payload_desimal = selisih(embedded_sample,interpolated_sample)

    # processed_bit = process_bit(payload_desimal, bit, interpolated_sample)

    # create_payload(processed_bit, extracted_payload)
    # create_cover_audio(original_sample, extracted_audio)

main()