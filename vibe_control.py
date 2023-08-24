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
    #filepath = 'jdcnet/output/pitch_pop1.txt'
    filepath = 'jdcnet/output/pitch_test.wav.txt'
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

def check_majority(arr):
    if not len(arr):
        return False

    # 要素の個数を数える
    element_count = {}
    for elem in arr:
        if elem in element_count:
            element_count[elem] += 1
        else:
            element_count[elem] = 1

    # 最頻値の個数と全体の要素数を比較
    majority_count = max(element_count.values())
    total_count = len(arr)
    if majority_count / total_count >= 0.7:
        return True
    else:
        return False




def getpitch():
    notes = np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24])
    allnotes = np.arange(-30, 50+1)
    
    pitchs = 440*(np.power(2,(notes-9)/12))
    allpitchs = 440*(np.power(2,(allnotes-9)/12))
    
    result = getfreq()
    freq = result[0]
    octave_multiplier = 2.0
    print(freq)
    while np.any(freq != 0) and pitchs.min() > np.min(freq[freq != 0]):
        print(np.min(freq[freq != 0]))
        freq = freq * octave_multiplier
    print(freq)
        
    # 各値に対して最も近い要素番号を求めて新しい配列に格納
    closest_indices = np.abs(pitchs[:, np.newaxis] - freq).argmin(axis=0)
    # closest_indicesを使用して、最も近い値に対応するpitchsの要素を選択
    closest_pitchs = pitchs[closest_indices]
    closest_pitchs[freq==0] = 0 
    closest_indices[freq==0] = -100

    # 各値に対して最も近い要素番号を求めて新しい配列に格納
    closest_allindices = np.abs(allpitchs[:, np.newaxis] - freq).argmin(axis=0)
    # closest_indicesを使用して、最も近い値に対応するpitchsの要素を選択
    closest_allpitchs = allpitchs[closest_allindices]
    closest_allpitchs[freq==0] = 0

    #if check_majority(closest_pitchs) == True:
    #    closest_indices = [-100]*len(closest_indices)
    #    closest_pitchs = [0]*len(closest_pitchs)
    
    return closest_indices, closest_allpitchs#closest_pitchs
    

phase = 0.0  # 初期位相
# 音声再生関数
def play_sound_vibe(vibenum, frequencies, sample_rate=5000):
    global phase
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
        if num == 12 or num == 24:
            v.set_b_values(-100)
        elif num < 12:
            v.set_b_values(num)
        elif num > 12:
            v.set_b_values(num-1)
            
        v.vibe()
        samples = (0.5 * np.sin(2 * np.pi * ((np.arange(sample_rate/(1.5))+phase) * frequency / sample_rate))).astype(np.float32)
        phase += sample_rate/(2.5)
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

def vibe_sound():
    pitchs = getpitch()
    num = pitchs[0]
    freq = pitchs[1]
    play_sound_vibe(num, freq)


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
