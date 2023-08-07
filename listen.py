import pyaudio
import queue
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
        self.slice_frames = 0
        self.slice_duration = 10  # in seconds
        self.frames_per_slice = self.slice_duration * self.RATE // self.CHUNK

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
            self.slice_frames += 1
            if self.slice_frames == self.frames_per_slice:
                yield b''.join(self.frames)
                self.frames = []
                self.slice_frames = 0
            if not self.recording:
                self.stream.stop_stream()
                self.stream.close()
                self.audio.terminate()
                if self.frames:
                    yield b''.join(self.frames)
                break

    def stop_recording(self):
        self.recording = False

def on_release(key, recorder):
    try:  # Used try to avoid AttributeError when a modifier key is released
        if key.char == 'q':  # Stop recording when 'q' is released
            recorder.stop_recording()
            return False  # Stop the listener
    except AttributeError:
        pass

def record_audio(ch, recorder):
    on_release_lambda = lambda key: on_release(key, recorder)
    listener = keyboard.Listener(on_release=on_release_lambda)
    listener.start()

    audio_slices_generator = recorder.start_recording()

    for audio_slice in audio_slices_generator:
        ch.put(audio_slice)

    listener.join()

    ch.put(None)
