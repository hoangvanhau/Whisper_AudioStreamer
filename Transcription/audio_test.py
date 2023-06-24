import pyaudio
import wave
from app import myClient

client = myClient(url="http://localhost:7860/", api_name="/predict")

def print_result(idx, au):
    print(f"Submited file: \n {idx}  audio: {au}")
    stream.stop_stream()
    stream.close()
    p.terminate()

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 10
COUNT = 0
# WAVE_OUTPUT_FILENAME = f"output_{COUNT}.wav"
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                input_device_index = 2,
                frames_per_buffer=CHUNK)

while stream.is_active() and COUNT < 6:
    # print("* recording")
    frames = []
    WAVE_OUTPUT_FILENAME = f"output_{COUNT}.wav"
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    # print("* done recording")
    
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    client.submit(str(COUNT), WAVE_OUTPUT_FILENAME, callback_fn=print_result)
    COUNT += 1

stream.stop_stream()
stream.close()
p.terminate()

