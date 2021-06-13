import json
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

def get_date(starttime=[], endtime=[], datefile = "./data/date.json", hourfile = "./data/hour.json"):
    hour_list = []
    date_list = []
    if len(starttime) != 2 or len(endtime) != 2:
        raise Exception("time illegal, please don't use default param")
    
    y = starttime[0]
    if starttime[0] == endtime[0]:
        me = endtime[1]
    else:
        me = 12
    feb_day = 29 if y % 4 == 0 and y % 100 or y % 400 == 0 else 28
    for m in range(starttime[1]-1, me):
        monthday = 31
        if m == 2-1:
            monthday = feb_day
        elif m == 4-1 or m == 6-1 or m == 9-1 or m == 11-1:
            monthday = 30
        for d in range(monthday):
            date_list.append({'year':str(y), 'month':str(m), 'day':d})
            for h in range(24):
                hour_list.append({'year':str(y), 'month':str(m), 'day':d, 'hour':str(h)})
    if starttime[0] == endtime[0]:
        return
    
    for y in range(starttime[0]+1, endtime[0]):
        feb_day = 29 if y % 4 == 0 and y % 100 or y % 400 == 0 else 28
        for m in range(12):
            monthday = 31
            if m == 2-1:
                monthday = feb_day
            elif m == 4-1 or m == 6-1 or m == 9-1 or m == 11-1:
                monthday = 30
            for d in range(monthday):
                date_list.append({'year':str(y), 'month':str(m), 'day':d})
                for h in range(24):
                    hour_list.append({'year':str(y), 'month':str(m), 'day':d, 'hour':str(h)})
    
    y = endtime[0]
    feb_day = 29 if y % 4 == 0 and y % 100 or y % 400 == 0 else 28
    for m in range(endtime[1]):
        monthday = 31
        if m == 2-1:
            monthday = feb_day
        elif m == 4-1 or m == 6-1 or m == 9-1 or m == 11-1:
            monthday = 30
        for d in range(monthday):
            date_list.append({'year':str(y), 'month':str(m), 'day':d})
            for h in range(24):
                hour_list.append({'year':str(y), 'month':str(m), 'day':d, 'hour':str(h)})
    
    with open(hourfile, 'w', encoding='utf-8') as hour_file:
        json.dump(hour_list, hour_file)
    with open(datefile, 'w', encoding='utf-8') as date_file:
        json.dump(date_list, date_file)
