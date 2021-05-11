from datetime import datetime, time
import pandas as pd
from mytool import progress_bar, time_group, group2time

# filename = "test/test.txt"
# filename = "data/Subway_20190301_Top100000.txt"
filename = "data/Subway_20180301.txt"

df = pd.read_csv(filename)
res = {}

pb = progress_bar(df.shape[0], 100)

for _, line in df.iterrows():
    starttime = datetime.strptime(str(line["UpTime"]), "%Y%m%d%H%M%S")
    endtime = datetime.strptime(str(line["DownTime"]), "%Y%m%d%H%M%S")
    if starttime.day != 1 or endtime.day != 1:
        continue
    delta = endtime - starttime
    if delta.days < 0:
        continue
    if delta.seconds > 7200:
        continue
    tg = time_group(starttime)
    res[tg] = res.get(tg, 0) + 1
    tg = time_group(endtime)
    res[tg] = res.get(tg, 0) - 1
    pb.progress(_)

for i in range(143):
    res[i+1] = res.get(i+1, 0) + res.get(i, 0)

res = sorted(res.items(), key=lambda x: x[0])
res = [(group2time(x[0]),x[1]) for x in res]
pd.DataFrame(res, columns=['时间组', '人数']).to_csv(
    "./out/PeopleInSubwayCount.csv",index=False)