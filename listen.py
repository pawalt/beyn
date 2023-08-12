import pyaudio
import threading
import wave
from pynput import keyboard
import time

RECORDING_FILE = "recording.wav"

class Recorder:
    def __init__(self):
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000
        self.CHUNK = 1024
        self.audio = pyaudio.PyAudio()
        self.frames = []

        self.stream = self.audio.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK
        )
        
        self.recording = False

    def start_recording(self):
        print("press q to stop recording")
        self.recording = True
        self.frames = []

        while self.recording:
            data = self.stream.read(self.CHUNK)
            self.frames.append(data)
            if not self.recording:
                self.stream.stop_stream()
                self.stream.close()
                self.audio.terminate()
                break

    def stop_recording(self):
        print("recording stopped")
        self.recording = False
        
        waveFile = wave.open(RECORDING_FILE, 'wb')
        waveFile.setnchannels(self.CHANNELS)
        waveFile.setsampwidth(self.audio.get_sample_size(self.FORMAT))
        waveFile.setframerate(self.RATE)
        waveFile.writeframes(b''.join(self.frames))
        waveFile.close()

def on_release(key, recorder):
    try:  # Used try to avoid AttributeError when a modifier key is released
        if key.char == 'q':  # Stop recording when 'q' is released
            recorder.stop_recording()
            return False  # Stop the listener
    except AttributeError:
        pass

def record_audio():
    recorder = Recorder()

    on_release_lambda = lambda key: on_release(key, recorder)

    listener = keyboard.Listener(on_release=on_release_lambda)  # Keep a reference to the listener
    listener.start()  # Start the listener

    record_thread = threading.Thread(target=recorder.start_recording)
    record_thread.start()

    while record_thread.is_alive():  # Loop while recording thread is alive
        time.sleep(0.5)
