import numpy as np
import pyaudio
import struct
import cv2
import threading
import matplotlib.pyplot as plt
import sounddevice
import vibe3

data = []

def getfreq():
	filepath = 'jdcnet/output/pitch_pop1.txt'
	#filepath = 'jdcnet/output/pitch_test.wav.txt'
	with open(filepath, 'r') as file:
		for line in file:
			line = line.strip()  # 行3先頭と末尾の空白を削除

			if line:  # 空行でない場合のみ処理を行う
				timestamp, frequency = line.split()  # スペースで行を分割
				if float(timestamp)*100 % 10 == 0:
					data.append((float(timestamp), float(frequency)))
	# データから時間と周波数のリストを作成
	timestamps, frequencies = zip(*data)

	#frequencies1 = np.array(frequencies)
	frequencies2 = np.array(frequencies)
	return frequencies2, timestamps

def getpitch():
    notes = np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24])
    pitchs = 440*(np.power(2,(notes-9)/12))
    result = getfreq()
    freq = result[0]
    octave_multiplier = 2.0
    print(freq)
    while pitchs.min() > np.min(freq[freq != 0]):
        print(np.min(freq[freq != 0]))
        freq = freq * octave_multiplier
    
        
    # 各値に対して最も近い要素番号を求めて新しい配列に格納
    closest_indices = np.abs(pitchs[:, np.newaxis] - freq).argmin(axis=0)
    # closest_indicesを使用して、最も近い値に対応するpitchsの要素を選択
    closest_pitchs = pitchs[closest_indices]
    closest_pitchs[freq==0] = 0 
    closest_indices[freq==0] = -100
    print(closest_indices)
    print(closest_pitchs)
    print(pitchs)
    return closest_indices, closest_pitchs
    


# 音声再生関数
def play_sound_vibe(vibenum, frequencies, sample_rate=44100):
    p = pyaudio.PyAudio()
    v = vibe3.vibePattern()
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=sample_rate,
                    output=True)

    # 音声再生
    for frequency, num in zip(frequencies, vibenum):
        print(frequency)
        print(num)
        v.set_b_values(num)
        v.vibe()
        samples = (0.5 * np.sin(2 * np.pi * np.arange(sample_rate/(2.5)) * frequency / sample_rate)).astype(np.float32)
        stream.write(samples)

    v.set_b_values(-100)
    v.vibe()
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


#画面描画
if __name__ == "__main__": 
    #test()
    pitchs = getpitch()
    num = pitchs[0]
    freq = pitchs[1]
    play_sound_vibe(num, freq)
    
    '''
    flag = 1
    result = getfreq()
    vibe_sound(flag, result[0], result[1])
    '''
