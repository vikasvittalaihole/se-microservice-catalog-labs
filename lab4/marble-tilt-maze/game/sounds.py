import math
import array
import pygame


class Sounds:
    def __init__(self):
        self.ok = False
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            self.rate, fmt, self.channels = pygame.mixer.get_init()
            if fmt != -16:
                raise ValueError("unsupported audio format")
            self.wall = self._make([220], 70)
            self.goal = self._make([523, 659, 784], 130)
            self.timeout = self._make([392, 311, 233], 220)
            self.ok = True
        except Exception:
            self.ok = False  # no audio device: game runs silently

    def _make(self, freqs, ms_each, volume=0.4):
        buf = array.array("h")
        for f in freqs:
            n = int(self.rate * ms_each / 1000)
            for i in range(n):
                fade = 1 - i / n
                v = int(32767 * volume * fade * math.sin(2 * math.pi * f * i / self.rate))
                for _ in range(self.channels):
                    buf.append(v)
        return pygame.mixer.Sound(buffer=buf.tobytes())

    def play(self, name):
        if not self.ok:
            return
        try:
            getattr(self, name).play()
        except Exception:
            pass
