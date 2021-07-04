import csv


with open("comments_append.csv","r",encoding="utf-8") as inf:
    with open("comments_append_new.csv","w",encoding="utf-8") as f:
        reader = csv.reader(inf,dialect="excel")
        writer = csv.writer(f,dialect="excel")
        for i in reader:
            if len(i) == 0:
                continue
            if i[0].find("https://") != -1:
                continue
            if i[0].find("BV") != -1:
                continue
            if i[0].find("http://") != -1:
                continue
            writer.writerow(i + [1])

