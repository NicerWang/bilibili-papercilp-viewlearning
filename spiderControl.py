import requests
import json
import csv


def getComments(BV:str, Jquery:str):
    headers = {
        'accept': "*/*",
        'accept-encoding': 'utf-8',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': "_uuid=8FCB6A33-1D00-E4B2-04BC-9BB8ADD6C0C699802infoc; buvid3=23512E12-863D-4B7F-BA3C-15521680E7FB34760infoc; fingerprint=7165e5c90188738a0fa6ae7be4e9b95a; buvid_fp=23512E12-863D-4B7F-BA3C-15521680E7FB34760infoc; buvid_fp_plain=5D53A3AC-3404-45F4-94ED-A2A71F91A1B053929infoc; SESSDATA=8564f720%2C1635758426%2C9ae55%2A51; bili_jct=73b1d2cdff250a3a6d99ca248a20a03f; DedeUserID=194669852; DedeUserID__ckMd5=724cd3f66f41d8a2; sid=575900k6; CURRENT_FNVAL=80; blackside_state=1; rpdid=|(u||)l~k~uu0J'uYk|k|YRlR; CURRENT_QUALITY=80; bp_t_offset_194669852=542849377631687666; PVID=2; bp_video_offset_194669852=543531637479779236; bfe_id=61a513175dc1ae8854a560f6b82b37af",
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
        Jquery,
        headers=headers)
    print(t.encoding)
    print(t.apparent_encoding)
    with open('TestJson.json', 'w', encoding='utf-8') as fw:
        idx = t.text.find("{")
        fw.write(t.text[idx:-1])


def writeCSV():
    with open("TestJson.json", "r", encoding="utf-8") as f:
        data = json.loads(f.read())
    comments = data['data']['replies']
    text = []
    for i in comments:
        text.append(i['content']['message'])
        if i['replies'] is not None:
            for j in i['replies']:
                text.append(j['content']['message'])
    with open("comments_append.csv", "a", encoding="utf-8") as f:
        csvwriter = csv.writer(f, dialect="excel")
        for singe in text:
            idx = 0
            if singe.startswith("回复"):
                idx = singe.find(':') + 1
            singe = singe.replace("\n", "")[idx:]
            if len(singe) >= 5:
                csvwriter.writerow([singe])

if __name__ == "__main__":
    while True:
        bv = " "
        jq = input("JQuery:")
        getComments(bv,jq)
        writeCSV()



