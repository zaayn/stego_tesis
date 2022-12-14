from Methods import read_payload
from Methods import segmentation_payload

from Methods import sampling
from Methods import interpolation_linear
from Methods import fuzzifikasi

from Methods import get_unique_bit
from Methods import payload_process
from Methods import embedding

from Methods import combine
from Methods import create_stego_audio

audio = '1'
payload = '1'
audio_file = 'dataset/Audio/data'+audio+'_mono.wav'
payload_file = 'dataset/Payload/payload'+payload+'.txt'
stego_audio = 'stego_audio/stego_audio'+audio+'_payload'+payload+'/stegoaudio.wav'

#payload process
binary_payload = read_payload(payload_file)
segmented_bit ,segmented_payload = segmentation_payload(binary_payload)

#audio process
freame_rate, original_sample = sampling(audio_file)
interpolated_sample = interpolation_linear(original_sample)
bit = fuzzifikasi(interpolated_sample, original_sample)

#embedding process
unique_bit, index_bit = get_unique_bit(bit)
processed_payload, divided, smooth = payload_process(segmented_bit, segmented_payload, unique_bit)
embedded = embedding(processed_payload, index_bit, interpolated_sample, divided, index_bit[-1], smooth)

#create output
stego_data = combine(original_sample, embedded, interpolated_sample)
create_stego_audio(stego_data, stego_audio)