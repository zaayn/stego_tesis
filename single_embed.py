from EmbedMethod import read_payload
from EmbedMethod import segmentation_payload
from EmbedMethod import sampling
from EmbedMethod import interpolation_linear
from EmbedMethod import fuzzifikasi
from EmbedMethod import payload_process
from EmbedMethod import combine
from EmbedMethod import create_stego_audio

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
embedded = payload_process(segmented_bit, segmented_payload, bit, interpolated_sample)

#create output
stego_data = combine(original_sample, embedded, interpolated_sample)
create_stego_audio(stego_data, stego_audio)