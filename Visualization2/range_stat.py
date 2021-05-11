from datetime import datetime
import pandas as pd
from mytool import progress_bar

# filename = "data/Subway_20190301_top100000.txt"
filename = "data/Subway_20180301.txt"
res = {}
df = pd.read_csv(filename)


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
    minutes = round(delta.seconds / 60)
    res[minutes] = res.get(minutes, 0) + 1
    pb.progress(_)


res = sorted(res.items(), key=lambda x: x[0])
pd.DataFrame(res, columns=['耗时（分钟）', '人数']).to_csv(
    "./out/PeopleInSubwayTime.csv", index=False)
