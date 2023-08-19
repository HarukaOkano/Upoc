import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import sounddevice
from audio_record import record_audio
import subprocess
from vibe_control import vibe_sound

data = []

Frequencies = []
Timestamp = []

flag = 0

def getfreq():
	#filepath = 'jdcnet/output/pitch_pop1.txt'
	filepath = 'jdcnet/output/pitch_test.wav.txt'
	with open(filepath, 'r') as file:
		for line in file:
			line = line.strip()  # 行3先頭と末尾の空白を削除

			if line:  # 空行でない場合のみ処理を行う
				timestamp, frequency = line.split()  # スペースで行を分割
				if float(timestamp)*100 % 5 == 0:
					data.append((float(timestamp), float(frequency)))

	print(data)



	# データから時間と周波数のリストを作成
	timestamps, frequencies = zip(*data)

	#frequencies1 = np.array(frequencies)
	
	frequencies2 = np.array(frequencies)
	'''
	peakpoint = []
	flag = 0
	peak = 0

	for i, f1 in enumerate(frequencies2):
		if i==0 or i==len(frequencies2)-1:
			peakpoint.append(i)
			continue
		if frequencies2[i-1]<frequencies2[i] and frequencies2[i]>=frequencies2[i+1]:
			peakpoint.append(i)
	print(peakpoint)

	for i, point in enumerate(peakpoint):
		if i == len(peakpoint)-1:
			continue
		templist = list(range(peakpoint[i], peakpoint[i+1]))
		for l, element in enumerate(templist):
			frequencies1[element] = frequencies2[point]
	'''		
	return timestamps, frequencies2


def getFreqTime():
	return flag, Frequencies, Timestamp
	


# 音声再生関数
def play_sound(frequencies, sample_rate=44100):
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=sample_rate,
                    output=True)

    # 音声再生
    for frequency in frequencies:
        samples = (np.sin(2 * np.pi * np.arange(sample_rate/(5)) * frequency / sample_rate)).astype(np.float32)
        stream.write(samples)

    stream.stop_stream()
    stream.close()
    p.terminate()

# グラフのプロット
def plot_data(timestamps, frequencies):
    plt.plot(timestamps, frequencies)
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency')
    plt.title('Frequency vs Time')
    plt.grid()
    plt.show()

def jdc_exe():
	# 実行したいコマンドと引数を指定
	command = ["python", "melodyExtraction_JDC.py", "-p", "../record/test.wav", "-o", "./output/"]

	working_directory = "jdcnet/"
	
	# subprocessを使用してコマンドを実行
	try:
		result = subprocess.run(
			command,
			cwd=working_directory,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE,
			text=True,
			check=True
		)
		# コマンドの実行結果を表示
		print("Standard Output:", result.stdout)
		print("Standard Error:", result.stderr)
    
	except subprocess.CalledProcessError as e:
		print("Error:", e)


if __name__ == "__main__":
	print("cd")
	record_audio()
	print("a")
	jdc_exe()
	print("cc")
	results = getfreq()
	timestamps = results[0]
	freqs = results[1]
	Frequencies = freqs
	Timestamp = timestamps
	flag = 1
	vibe_sound(flag, Frequencies, Timestamp)
	# 音声再生とグラフのプロット
	play_sound(freqs)
	#play_sound(frequencies)
	plot_data(timestamps, freqs)
	#plot_data(timestamps, frequencies)

