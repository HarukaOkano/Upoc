import pyaudio
p = pyaudio.PyAudio()
for i in range(p.get_device_count()):
    data = p.get_device_info_by_index(i)
    print(data)
    #if data['name'] == "USB PnP Sound Device: Audio (hw:1,0)":
    #    print(data['index'])
