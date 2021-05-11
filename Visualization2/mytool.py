from datetime import datetime


class progress_bar():
    def __init__(self, workload, length) -> None:
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
              'o').ljust(self.length) + "]" + "loading...", end='')


def time_group(etime: datetime.time) -> int:
    return etime.hour * 6 + (etime.minute // 10)


def group2time(group_num: int) -> str:
    hour = group_num // 6
    dec_min = group_num % 6
    return str(hour).rjust(2, '0') + ":" + str(dec_min * 10).rjust(2, '0') + '-' + str(hour).rjust(2, '0') + ":" + str(dec_min * 10 + 9).rjust(2, '0')


def csv2js():
    import pandas as pd
    import json
    df = pd.read_csv("./out/PeopleInSubwayTime.csv")
    data = [df.iloc[:, 0].tolist(), df.iloc[:, 1].tolist()]
    with open("./out/myData.js", 'a', encoding="utf-8") as f:
        json.dump(data,f)
    df = pd.read_csv("./out/PeopleInSubwayCount.csv")
    data = [df.iloc[:, 0].tolist(), df.iloc[:, 1].tolist()]
    with open("./out/myData.js", 'a', encoding="utf-8") as f:
        json.dump(data,f)