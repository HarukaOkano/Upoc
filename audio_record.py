import pyaudio
import wave
import sounddevice


p = pyaudio.PyAudio()
for i in range(p.get_device_count()):
    audiodev = p.get_device_info_by_index(i)
    if "USB PnP Sound Device: Audio" in audiodev['name']:
        index = audiodev['index']

form_1 = pyaudio.paInt16 # 16-bit resolution
chans = 1 # 1 channel
samp_rate = 44100 # 44.1kHz　サンプリング周波数
chunk = 512 # 2^12 一度に取得するデータ数
record_secs = 10 # 録音する秒数
dev_index = index # デバイス番号
wav_output_filename = 'record/test.wav' # 出力するファイル


def record_audio():
	audio = pyaudio.PyAudio() # create pyaudio instantiation

	# create pyaudio stream
	stream = audio.open(format = form_1,rate = samp_rate,channels = chans, \
                    input_device_index = dev_index,input = True, \
                    frames_per_buffer=chunk)
	print("recording")
	frames = []

	# loop through stream and append audio chunks to frame array
	for i in range(0,int((samp_rate/chunk)*record_secs)):
		data = stream.read(chunk)
		frames.append(data)

	print("finished recording")

	# stop the stream, close it, and terminate the pyaudio instantiation
	stream.stop_stream()
	stream.close()
	audio.terminate()

	# save the audio frames as .wav file
	wavefile = wave.open(wav_output_filename,'wb')
	wavefile.setnchannels(chans)
	wavefile.setsampwidth(audio.get_sample_size(form_1))
	wavefile.setframerate(samp_rate)
	wavefile.writeframes(b''.join(frames))
	wavefile.close()

if __name__=="__main__":
	record_audio()
