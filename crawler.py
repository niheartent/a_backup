import random
from time import sleep
import requests
import json
import os


class Chuan:
    is_po: str
    page: int
    name: str
    path: str

    def __init__(self, id, name, path, page=1, is_po="false"):
        self.id = id
        self.name = name
        self.page = page
        self.is_po = is_po
        self.path = path

    def get_url(self):
        return f"https://aweidao1.com/api/v1/thread?id={self.id}&page={self.page}&po={self.is_po}&newest=false"


def test_connect(session, chuan: Chuan):
    # 对第一页尝试发送请求
    response = session.get(chuan.get_url(), cookies=cookies)

    data = response.json()
    errcode = data["errcode"]
    if errcode == 0:
        print("请求成功")
    else:
        print(f"请求失败: errcode = {errcode}")


def get_start_page(chuan: Chuan):
    try:
        with open(
            f"{chuan.path}/{chuan.id}{chuan.name}.jsonl", "r", encoding="utf-8"
        ) as f:
            chuan.page = sum(1 for _ in f) + 1
            print(f"读入旧文件, 从{chuan.page }行开始")
    except FileNotFoundError:
        chuan.page = 1
        print(f"创建新文件, 从{chuan.page }行开始")


def progress_bar(current, total, description="", bar_length=50):
    fraction = current / total
    if fraction >= 1.0:
        fraction = 1.0
    arrow = int(fraction * bar_length - 1) * "=" + ">"
    padding = (bar_length - len(arrow)) * " "
    print(f"\r{description} [{arrow}{padding}] {int(fraction*100)}%", end="")


def save_data(session, chuan: Chuan, time_interval_min=1, time_interval_max=5):
    print(f"***************开始爬取 {chuan.name} 的数据***************")
    get_start_page(chuan)
    response = session.get(chuan.get_url())
    page_count = (
        response.json()["result"]["replyCount"] // response.json()["result"]["pageSize"]
    )
    with open(f"{chuan.path}/{chuan.id}{chuan.name}.jsonl", "a", encoding="utf-8") as f:
        while True:
            response = session.get(chuan.get_url())
            data = response.json()
            errcode = data["errcode"]
            if errcode != 0:
                print(f"请求失败: errcode = {errcode}")
                break
            if not data["result"]["replys"]:
                print(f"爬取完数据, 共爬取{chuan.page}页")
                break
            f.write(json.dumps(data, ensure_ascii=False) + "\n")
            progress_bar(chuan.page, page_count, description="Processing")
            chuan.page += 1
            sleep(random.uniform(time_interval_min, time_interval_max))
    print(f"保存到 {chuan.id}{chuan.name}.jsonl")


if __name__ == "__main__":

    with open("./config/backup_json.json", "r", encoding="utf-8") as f:
        config = json.load(f)
        cookies = config["cookies"]
        all_list = config["all_list"]
        time_interval_min = config["time_interval_min"]
        time_interval_max = config["time_interval_max"]
        output_path = config["output_path"]

        session = requests.Session()
        session.cookies.update(cookies)

        path = os.path.dirname(os.path.abspath(__file__))
        backup_path = f"{path}/{output_path}"
        if not os.path.exists(backup_path):
            os.makedirs(backup_path)

        for id, name in all_list.items():
            chuan = Chuan(id, name, backup_path)
            print(f"正在爬取 {name} 的数据")
            test_connect(session, chuan)
            save_data(session, chuan, time_interval_min, time_interval_max)
