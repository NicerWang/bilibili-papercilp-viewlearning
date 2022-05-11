import requests
import json
import csv


def getComments(jquery: str):
    headers = {
        'accept': "*/*",
        'accept-encoding': 'utf-8',
        'accept-language': 'zh-CN,zh;q=0.9',
        # 此处cookie需要替换
        'cookie': "",
        'dnt': "1",
        'referer': 'https://www.bilibili.com/video/',
        'sec-ch-ua': '" Not;A Brand";v="99", "Microsoft Edge";v="91", "Chromium";v="91"',
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-dest': 'script',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.64'
    }
    t = requests.get(
        jquery,
        headers=headers)
    print(t.encoding)
    print(t.apparent_encoding)
    with open('archive/spider.json', 'w', encoding='utf-8') as fw:
        idx = t.text.find("{")
        fw.write(t.text[idx:-1])


def writeCSV(date: str):
    with open("archive/spider.json", "r", encoding="utf-8") as f:
        data = json.loads(f.read())
    comments = data['data']['replies']
    text = []
    for i in comments:
        text.append(i['content']['message'])
        if i['replies'] is not None:
            for j in i['replies']:
                text.append(j['content']['message'])
    with open("archive/comments_append.csv", "a", encoding="utf-8") as f:
        writer = csv.writer(f, dialect="excel")
        for singe in text:
            # 如果提及链接或BV号，则跳过
            if singe[0].find("https://") != -1:
                continue
            if singe[0].find("BV") != -1:
                continue
            if singe[0].find("http://") != -1:
                continue
            idx = 0
            if singe.startswith("回复"):
                idx = singe.find(':') + 1
            singe = singe.replace("\n", "")[idx:]
            if len(singe) >= 5:
                writer.writerow([date, singe])


if __name__ == "__main__":
    while True:
        # 每次请求评论，都有一个JQuery(xxxx)，需要输入这串字符
        jq = input("Input Video JQuery:")
        time = input("Input Video Time:")
        getComments(jq)
        writeCSV(time)
