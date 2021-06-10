import json
from mytool import progress_bar
date_list = []
with open('./data/date.json', 'r', encoding='utf-8') as f:
    date_list = json.load(f)

l = len(date_list)


pb = progress_bar(l)
for i in range(l-1):
    y = date_list[i]['year']
    m = str(int(date_list[i]['month'])+1)
    d = str(date_list[i]['day']+1)
    day_sentences = []
    for h in range(24):
        hour_sentences = []
        try:
            with open(f'./out/wuhan_raw/{y}-{m}-{d}-{h}.txt', 'r', encoding='utf-8') as f:
                while True:
                    line = f.readline()
                    if line == '':
                        break
                    line = line.strip()
                    if line == '':
                        continue
                    elif "展开全文" in line:
                        continue
                    else:
                        if line not in hour_sentences:
                            hour_sentences.append(line)
                        if line not in day_sentences:
                            day_sentences.append(line)
        finally:
            with open(f'./out/wuhan_hour/{y}-{m}-{d}-{h}.txt', 'w', encoding='utf-8') as fh:
                for line in hour_sentences:
                    print(line, file=fh)
    pb.progress(i)

    with open(f'./out/wuhan_day/{y}-{m}-{d}.txt', 'w', encoding='utf-8') as f:
        for line in day_sentences:
            print(line, file=f)
