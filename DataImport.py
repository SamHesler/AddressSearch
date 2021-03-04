import json

'''
Success:
    au
    ro
    vg
    es (10000 rows)
    no (10000 rows)
Fail:
    ch
    is
    lv
'''


jsonList = []

with open('no.geojson') as f:
    count = 0
    for line in f:
         jsonList.append(json.loads(line)['properties'])
         count = count + 1
         if (count == 10000):
             break
    print("it worked")

with open('no.csv', 'w') as f:
    count = 0
    for key in jsonList[0].keys():
        if (count != 0):
            f.write(",")
        f.write("%s"%(key))
        count = count + 1
    f.write("\n")
    for line in jsonList:
        count = 0
        for value in line.values():
            if (count != 0):
                f.write(",")
            f.write("%s"%(value))
            count = count+1
        f.write("\n")
        