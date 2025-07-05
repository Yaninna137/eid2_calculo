from dataclasses import dataclass

@dataclass
class GPU:
    f: float
    k: int

    def amdahl(self):
        return 1 / ((1 - self.f) + self.f / self.k)

    def amdahl_max(self):
        return 1 / (1 - self.f)
