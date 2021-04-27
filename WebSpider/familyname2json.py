import json
d1 = {}
with open("./assets/family_name.txt", 'r', encoding='utf-8') as f:
    for line in f.readlines():
        list1 = line.split()
        for item in list1:
            d1[item[-1]] = 0
with open("assets/family_name.json", 'w', encoding='utf-8') as f:
    json.dump(d1, f)
