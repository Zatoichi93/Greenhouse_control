from pygame import mixer
import os


class Music:

    _songs = []

    def __init__(self, directory):
        print directory
        freq = 44100  # audio CD quality
        bitsize = -16  # unsigned 16 bit
        channels = 1  # 1 is mono, 2 is stereo
        buffer = 2048  # number of samples (experiment to get right sound)
        mixer.init(freq, bitsize, channels, buffer)
        for dirpath, _, filenames in os.walk(directory):
            for f in filenames:
                self._songs.append(os.path.abspath(os.path.join(dirpath, f)))

    def play(self):
        while True:
            if not mixer.music.get_busy():
                mixer.music.load(self._songs[0])
                mixer.music.play()
                self._songs = self._songs[1:] + [self._songs[0]]  # move current song to the back of the list
