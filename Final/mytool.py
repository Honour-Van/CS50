class progress_bar():
    def __init__(self, workload, length=100) -> None:
        self._workload = workload
        self.stage_d = int(workload/length)
        self.stage_c = 0
        self.stage_n = 0
        self.length = length

    def progress(self, cur):
        if cur > self.stage_c:
            self.stage_c += self.stage_d
            self.stage_n += 1
        print('\r' + "[" + (self.stage_n *
              'o').ljust(self.length) + "]" + f"({cur}/" + f"{self._workload})"+ "loaded...", end='')

