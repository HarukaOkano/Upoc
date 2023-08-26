import numpy as np
import pyaudio
import struct
import cv2
import threading
import matplotlib.pyplot as plt
import sounddevice
import snd_kairo as kairo

RATE=5000       
bufsize = 128      

#鍵盤のGUI作成
ksx = 800
ksy = 200
keyboard = np.zeros([ksy,ksx,3])
keyboard[:,:,:] = 255
for i in range(15):
    cv2.rectangle(keyboard, (int(ksx/15*i), 0), (int(ksx/15*(i+1)),ksy), (0, 0, 0), 5)
for i in range(15):
    if i in {0,1,3,4,5,7,8,10,11,12}:
        cv2.rectangle(keyboard, (int(ksx/15*i + ksx/27 ), 0), (int(ksx/15*(i+1) + ksx/33),int(ksy/2)), (0, 0, 0), -1)



#各種パラメータ用スライダーの設定
sl=np.array([0,150,100,50,0,0,0,0])
slName = np.array(['Wave_type',
                   'Attack',
                   'Release',
                   'Lowpass_freq',
                   'FM_amp',
                   'FM_freq',
                   'Delay_time',
                   'Delay_feedback'])


def changeBar(val):
    global sl
    for i in range(8):
        sl[i] = cv2.getTrackbarPos(slName[i], "keyboard")
cv2.namedWindow("keyboard", cv2.WINDOW_NORMAL)
cv2.createTrackbar(slName[0], "keyboard", 0, 4, changeBar)
cv2.createTrackbar(slName[1], "keyboard", 0, 255, changeBar)
cv2.createTrackbar(slName[2], "keyboard", 0, 255, changeBar)
cv2.createTrackbar(slName[3], "keyboard", 0, 255, changeBar) 
cv2.createTrackbar(slName[4], "keyboard", 0, 255, changeBar) 
cv2.createTrackbar(slName[5], "keyboard", 0, 11, changeBar)
cv2.createTrackbar(slName[6], "keyboard", 0, 255, changeBar) 
cv2.createTrackbar(slName[7], "keyboard", 0, 255, changeBar)  

cv2.setTrackbarPos(slName[0], "keyboard", 0)
cv2.setTrackbarPos(slName[1], "keyboard", 150)
cv2.setTrackbarPos(slName[2], "keyboard", 100)
cv2.setTrackbarPos(slName[3], "keyboard", 50)
cv2.setTrackbarPos(slName[4], "keyboard", 0)
cv2.setTrackbarPos(slName[5], "keyboard", 0)
cv2.setTrackbarPos(slName[6], "keyboard", 0)
cv2.setTrackbarPos(slName[7], "keyboard", 0)


#マウス位置による鍵盤選択
keyon = 0
pre_keyon = 0
pitch = 440
velosity = 0.0
keyon2 = 0
pre_keyon2 = 0
pitch2 = 440
velosity2 = 0.0
pre_pitch = 440
pre_pitch2 = 440
#keys = np.array([0,2,4,5,7,9,11,12,12])
#keys2 = np.array([12,14,16,17,19,21,23,24,24])
keys = np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,12])
#keys = np.array([12,13,14,15,16,17,18,19,20,21,22,23,24,24])
keys2 = np.array([12,13,14,15,16,17,18,19,20,21,22,23,24,24])
#keys2 = np.array([-12,-10,-8,-7,-5,-3,-1,0,2])
#keys2 = np.array([0,2,4,5,7,9,11,12,14])
bure = [0.10, 0.30, 0.50, 0.80,1.0,1.3,1.5,1.8,2.0,2.3,2.5,2.8,3.0,3.2]
burange = 0.05
bureflag = 0
bureflag2 = 0
curbure = 0
curbure2 = 0
def touch_event():
    global keyon,pre_keyon,pitch,velosity, keyon2, pre_keyon2, pitch2, velosity2, pre_pitch, pre_pitch2, bureflag, bureflag2,curbure,curbure2
    touchpos = kairo.poscal()
    #print(touchpos[0])
    #print(touchpos[1])
    position1 = int(touchpos[0] * 10)
    position2 = int(touchpos[1] * 10)
    #print(position1)
    #print(position2)
    #print(bureflag)
    
    if curbure-burange < touchpos[0] and touchpos[0] < curbure+burange and bureflag == 1:
        pitch = pre_pitch
        print(pitch)
    elif bureflag == 1 and not(curbure-burange < touchpos[0] and touchpos[0] < curbure+burange):
        bureflag = 0
        
    if curbure2-burange < touchpos[1] and touchpos[1] < curbure2+burange and bureflag2 == 1:
        pitch2 = pre_pitch2
        print(pitch2)
    elif bureflag2 == 1 and not(curbure2-burange < touchpos[1] and touchpos[1] < curbure2+burange):
        bureflag2 = 0

    if bureflag == 0:
        if position1 != 0 and position1 < 32:
            keyon = 1
            note = keys[int((position1/32)*(len(keys)-1))]
            #print(note)
            pitch = 440*(np.power(2,(note-9)/12))
            pre_pitch = pitch
        else:
            keyon = 0
            bureflag = 0
            #pre_keyon = 0
    if pre_keyon ==0 and keyon ==1:
        velosity = 0.0
    pre_keyon = keyon
	
    if bureflag2 == 0:
        if position2 != 0 and position2 < 32:
            keyon2 = 1
            note2 = keys2[int((position2/32)*(len(keys2)-1))]
            #print(note2)
            pitch2 = 440*(np.power(2,(note2-9)/12))
            pre_pitch2 = pitch2
        else:
            keyon2 = 0
            bureflag2 = 0
            #pre_keyon2 = 0
    if pre_keyon2 ==0 and keyon2 ==1:
        velosity2 = 0.0
    pre_keyon2 = keyon2
    
    for b in range(len(bure)):
        if bure[b]-burange < touchpos[0] and touchpos[0] < bure[b]+burange and bureflag == 0:
            bureflag = 1
            curbure = bure[b]
        if bure[b]-burange < touchpos[1] and touchpos[1] < bure[b]+burange and bureflag2 == 0:
            bureflag2 = 1 
            curbure2 =  bure[b]
    


#ローパスフィルター
lpfbuf=np.zeros(4)
outwave=np.zeros(bufsize)
def lowpass(wave):
    global lpfbuf,outwave
    w0 = 2.0*np.pi*(200+(sl[3]/255.0)**2*20000)/RATE;
    Q = 1.0
    alpha = np.sin(w0)/(2.0*Q)
    a0 =   (1 + alpha)
    a1 =  -2*np.cos(w0)/a0
    a2 =   (1 - alpha)/a0
    b0 =  (1 - np.cos(w0))/2/a0
    b1 =   (1 - np.cos(w0))/a0
    b2 =  (1 - np.cos(w0))/2/a0
    for i in range(bufsize):
        outwave[i] = b0*wave[i]+b1*lpfbuf[1]+b2*lpfbuf[0]-a1*lpfbuf[3]-a2*lpfbuf[2]
        lpfbuf[0] = lpfbuf[1]
        lpfbuf[1] = wave[i]
        lpfbuf[2] = lpfbuf[3]
        lpfbuf[3] = outwave[i]
    return outwave


#ローパスフィルター
lpfbuf2=np.zeros(4)
outwave2=np.zeros(bufsize)
def lowpass(wave):
    global lpfbuf2,outwave2
    w0 = 2.0*np.pi*(200+(sl[3]/255.0)**2*20000)/RATE;
    Q = 1.0
    alpha = np.sin(w0)/(2.0*Q)
    a0 =   (1 + alpha)
    a1 =  -2*np.cos(w0)/a0
    a2 =   (1 - alpha)/a0
    b0 =  (1 - np.cos(w0))/2/a0
    b1 =   (1 - np.cos(w0))/a0
    b2 =  (1 - np.cos(w0))/2/a0
    for i in range(bufsize):
        outwave2[i] = b0*wave[i]+b1*lpfbuf2[1]+b2*lpfbuf2[0]-a1*lpfbuf2[3]-a2*lpfbuf2[2]
        lpfbuf2[0] = lpfbuf2[1]
        lpfbuf2[1] = wave[i]
        lpfbuf2[2] = lpfbuf2[3]
        lpfbuf2[3] = outwave2[i]
    return outwave2

#ディレイ
ringbuf = np.zeros(50000)#最大ディレイタイムは50000/RATE秒
def delay(wave):
    global ringbuf
    delaytime = sl[6]/255.0 * 1.0
    feedback = sl[7]/255.0 * 0.7
    dryandwet = feedback/2.0
    writepoint = int(delaytime*RATE)
    ringbuf = np.roll(ringbuf,-bufsize)
    ringbuf[writepoint:writepoint+bufsize] = wave + feedback * ringbuf[:bufsize]
    outwave = (1-dryandwet) * wave + dryandwet * ringbuf[:bufsize]
    return outwave

#ディレイ
ringbuf2 = np.zeros(50000)#最大ディレイタイムは50000/RATE秒
def delay2(wave):
    global ringbuf2
    delaytime = sl[6]/255.0 * 1.0
    feedback = sl[7]/255.0 * 0.7
    dryandwet = feedback/2.0
    writepoint = int(delaytime*RATE)
    ringbuf2 = np.roll(ringbuf2,-bufsize)
    ringbuf2[writepoint:writepoint+bufsize] = wave + feedback * ringbuf2[:bufsize]
    outwave = (1-dryandwet) * wave + dryandwet * ringbuf2[:bufsize]
    return outwave



#波形生成
x=np.arange(bufsize)
pos = 0
def synthesize():
    global pos,velosity

    #位相計算
    t = pitch * (x+pos) / RATE
    t = t - np.trunc(t)
    pos += bufsize

    #基本波形選択
    if sl[0]==1:#のこぎり波
        wave = t*2.0-1.0
    elif sl[0]==2:#矩形波
        wave = np.zeros(bufsize);wave[t<=0.5]=-1;wave[t>0.5]=1;
    elif sl[0]==3:#三角波
        wave = np.abs(t*2.0-1.0)*2.0-1.0
    elif sl[0]==4:#FM変調
        wave = np.sin(2.0*np.pi*t + sl[4]/100.0 * np.sin(2.0*np.pi*t*sl[5]))
    else:#サイン波
        wave = np.sin(2.0*np.pi*t)

    #エンベロープ設定
    if keyon == 1:
        vels = velosity + x * ((sl[1]/1000)**3+0.00001)
        vels[vels>0.6] = 0.6
    else:
        vels = velosity - x * ((sl[2]/1000)**3+0.00001)
        vels[vels<0.0] = 0.0
    velosity = vels[-1]    
    wave = vels * wave

    #ローパスフィルター
    #wave = lowpass(wave)

    return wave

#波形生成
x2=np.arange(bufsize)
pos2 = 0
def synthesize2():
    global pos2,velosity2

    #位相計算
    t = pitch2 * (x2+pos2) / RATE
    t = t - np.trunc(t)
    pos2 += bufsize

    #基本波形選択
    if sl[0]==1:#のこぎり波
        wave = t*2.0-1.0
    elif sl[0]==2:#矩形波
        wave = np.zeros(bufsize);wave[t<=0.5]=-1;wave[t>0.5]=1;
    elif sl[0]==3:#三角波
        wave = np.abs(t*2.0-1.0)*2.0-1.0
    elif sl[0]==4:#FM変調
        wave = np.sin(2.0*np.pi*t + sl[4]/100.0 * np.sin(2.0*np.pi*t*sl[5]))
    else:#サイン波
        wave = np.sin(2.0*np.pi*t)

    #エンベロープ設定
    if keyon2 == 1:
        vels = velosity2 + x2 * ((sl[1]/1000)**3+0.00001)
        vels[vels>0.6] = 0.6
    else:
        vels = velosity2 - x2 * ((sl[2]/1000)**3+0.00001)
        vels[vels<0.0] = 0.0
    velosity2 = vels[-1]    
    wave = vels * wave

    #ローパスフィルター
    #wave = lowpass(wave)

    return wave

def play_sound1():
	buf1 = synthesize()
	buf1 = delay(buf1)
	buf1 = (buf1 * 32768.0).astype(np.int16)#16ビット整数に変換
	buf1 = struct.pack("h" * len(buf1), *buf1)
	stream.write(buf1)
	
def play_sound2():
	buf2 = synthesize()
	buf2 = delay(buf2)
	buf2 = (buf2 * 32768.0).astype(np.int16)#16ビット整数に変換
	buf2 = struct.pack("h" * len(buf2), *buf2)
	stream.write(buf2)	
	

#波形再生
playing = 1
def audioplay():
    print ("Start Streaming")
    p=pyaudio.PyAudio()
    stream=p.open(format = pyaudio.paInt16,
            channels = 2,
            rate = RATE,
            frames_per_buffer = bufsize,
            output = True)
    while stream.is_active():
        touch_event()
        '''
        buf1 = synthesize()
        buf1 = delay(buf1)
        buf1 = (buf1 * 32768.0).astype(np.int16)#16ビット整数に変換
        buf1 = struct.pack("h" * len(buf1), *buf1)
        stream.write(buf1)
        '''
        '''
        buf2 = synthesize2()
        buf2 = delay2(buf2)
        buf2 = (buf2 * 32768.0).astype(np.int16)#16ビット整数に変換
        buf2 = struct.pack("h" * len(buf2), *buf2)
        stream.write(buf2)
        '''
        
        buf1 = synthesize()
        buf1 = delay(buf1)
        buf1 = (buf1 * 32768.0).astype(np.int16)#16ビット整数に変換
        buf2 = synthesize2()
        buf2 = delay2(buf2)
        buf2 = (buf2 * 32768.0).astype(np.int16)#16ビット整数に変換
        interleaved = np.column_stack((buf1, buf2)).ravel()
        packed_data = struct.pack("h" * len(interleaved), *interleaved)
        stream.write(packed_data)
        #stream.write(buf1)
        if playing == 0:
            break
    stream.stop_stream()
    stream.close()
    p.terminate()
    print ("Stop Streaming")



#波形とスペクトル画像生成
def waveformAndSpectrum():
    sampleN = 1024
    t0 = pitch * np.arange(sampleN) / RATE
    t = t0 - np.trunc(t0)
    #基本波形選択
    if sl[0]==1:#のこぎり波
        wave = t*2.0-1.0
    elif sl[0]==2:#矩形波
        wave = np.zeros(bufsize);wave[t<=0.5]=-1;wave[t>0.5]=1;
    elif sl[0]==3:#三角波
        wave = np.abs(t*2.0-1.0)*2.0-1.0
    elif sl[0]==4:#FM変調
        wave = np.sin(2.0*np.pi*t + sl[4]/100.0 * np.sin(2.0*np.pi*t*sl[5]))
    else:#サイン波
        wave = np.sin(2.0*np.pi*t)

    if sl[3] < 250:#ローパスフィルター
        outwave=np.zeros(sampleN)
        w0 = 2.0*np.pi*(200+(sl[3]/255.0)**2*20000)/RATE;
        Q = 1.0
        alpha = np.sin(w0)/(2.0*Q)
        a0 =   (1 + alpha)
        a1 =  -2*np.cos(w0)/a0
        a2 =   (1 - alpha)/a0
        b0 =  (1 - np.cos(w0))/2/a0
        b1 =   (1 - np.cos(w0))/a0
        b2 =  (1 - np.cos(w0))/2/a0
        lpfbuf2=np.zeros(4)
        for i in range(sampleN):
            outwave[i] = b0*wave[i]+b1*lpfbuf2[1]+b2*lpfbuf2[0]-a1*lpfbuf2[3]-a2*lpfbuf2[2]
            lpfbuf2[0] = lpfbuf2[1]
            lpfbuf2[1] = wave[i]
            lpfbuf2[2] = lpfbuf2[3]
            lpfbuf2[3] = outwave[i]
    else:
        outwave = wave

    Spectrum = abs(np.fft.fft(outwave))
    frq = np.fft.fftfreq(sampleN,1.0 / RATE)

    plt.clf()
    plt.subplot(2,1,1)
    plt.title("Waveform")
    plt.plot(t0,outwave)
    plt.xlim([0,pitch * sampleN / RATE])
    plt.ylim([-1.5, 1.5])  
    plt.subplot(2,1,2)
    plt.title("Spectrum")
    plt.yscale("log")
    plt.plot(frq[:int(sampleN/2)],Spectrum[:int(sampleN/2)])
    plt.xlim([0,10000])
    plt.pause(1)

#画面描画
if __name__ == "__main__": 
    thread = threading.Thread(target=audioplay)
    thread.start()
    while (True):
        cv2.imshow("keyboard", keyboard) 
        k = cv2.waitKey(100) & 0xFF
        if k == ord('q'):
            playing = 0
            break
        if k == ord('s'):
            waveformAndSpectrum()

    cv2.destroyAllWindows()
