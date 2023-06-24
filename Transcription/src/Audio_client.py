import pyaudio
import wave
from gradio_client import Client

class myClient:
    def __init__(self, url, api_name):
        self.url = url
        self.api_name = api_name
        self.client = Client(self.url)
    def submit(self, index_token, audio, callback_fn):
        text = self.client.submit(index_token, audio, api_name=self.api_name, result_callbacks=callback_fn)
        return text

class Audio_streamer:
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    DEVICE_INDEX=2
    RECORD_SECONDS = 10
    COUNT = 0
    # TODO: create tmp dir and clean this dir before runing new
    TMP_DIR = "tmp"
    def __init__(self, server_url, api_name):
        self.index_tokens = []
        self.transcripts = []
        self.text = ""
        self.server_url = server_url
        self.server_api = api_name
        self.p = pyaudio.PyAudio()
    def __syndata(self):
        sorted_text = [transcript for _,transcript in sorted(zip(self.index_tokens, self.transcripts))]
        self.text = ''.join(sorted_text)
    def response(self, index_token, transcript):
        self.index_tokens.append(int(index_token))
        self.transcripts.append(transcript)
    def start(self):
        self.on_flag = True
        self.client = myClient(self.server_url, self.server_api)
        self.stream = self.p.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            input_device_index=self.DEVICE_INDEX,
            frames_per_buffer=self.CHUNK
        )
        while self.stream.is_active() and self.on_flag:
            frames = []
            WAVE_OUTPUT_FILENAME = f"output_{self.COUNT}.wav"
            for i in range(0, int(self.RATE / self.CHUNK * self.RECORD_SECONDS)):
                data = self.stream.read(self.CHUNK)
                frames.append(data)

            wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)
            wf.writeframes(b''.join(frames))
            wf.close()
            # submit to server
            self.client.submit(str(self.COUNT), WAVE_OUTPUT_FILENAME, callback_fn=self.response)
            self.COUNT +=1
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
    def stop(self):
        self.on_flag = False