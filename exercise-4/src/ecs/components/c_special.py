class CSpecial:
    def __init__(self, cooldown: float) -> None:
        self.cooldown = cooldown
        self.time_left: float = 0
        self.denied_time: float = 0
        self.ready_flash_time: float = 0
        self.elapsed: float = 0

    @property
    def is_ready(self):
        return self.time_left <= 0

    @property
    def charge(self):
        return 1 - self.time_left / self.cooldown
