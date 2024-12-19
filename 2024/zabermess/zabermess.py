import communication as zm
from mido import MidiFile
import scipy.io.wavfile as sio
import scipy.signal as sig
import time
import numpy as np

serial_port = "/dev/tty.usbserial-AC01ZNBL"

midi_file = MidiFile("2024/zabermess/JingleBellsTest.mid")

sampl_freq, y = sio.read("2024/zabermess/jingle-bells.wav")
y = (y[:, 0] + y[:, 1]) / 2

# Init Zaber device
axis = zm.XLSMA(zm.Interface(serial_port), 1)
direction = 1
axis.home()
axis.move_to(0.05)


def play_tone(tone: float, direction: int):
    axis.move_const(speed=direction * (0.005 / 1661 * (440 * 2 ** ((tone - 69) / 12))))


def play_freq(freq, direction):
    # Possible freq ranges from axis
    if freq <= 8500 and freq >= 10:
        # the axis plays a 1661 Hz tone with a speed of 0.005
        axis.move_const(speed=direction * (0.005 / 1661 * (freq)))


def play_midi():
    """Play music from midi midi"""
    global direction
    for msg in midi_file:
        # Play pauses:
        if msg.type == "note_off":
            time.sleep(msg.time)
        elif msg.type == "note_on":
            direction = direction * (-1)
            play_tone(msg.note, direction)
            time.sleep(msg.time)


def play_wav():
    global direction
    f, t, spec = sig.spectrogram(y, sampl_freq, nperseg=4096 * 2, noverlap=256)
    prev_freq = 0
    for freq in spec.T:
        current_freq = int(f[np.argmax(freq)])
        if abs(prev_freq - current_freq) >= 25:
            play_freq(current_freq, direction)
            prev_freq = current_freq
            direction = direction * (-1)

        time.sleep(0.046 * 4)
    axis.stop()


play_wav()
