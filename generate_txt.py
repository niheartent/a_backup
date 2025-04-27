from ebooklib import epub
from dataclasses import dataclass
import json
import argparse
import os


@dataclass
class Reply:
    id: str
    content: str
    time: str
    user_id: str


def get_first_content(input_path):
    with open(input_path, "r", encoding="utf-8") as f:
        fdata = json.loads(f.readline()).get("result", {})
        # print(fdata)
        return Reply(
            fdata.get("id"),
            fdata.get("content"),
            fdata.get("now"),
            fdata.get("userid"),
        )


def get_reply(input_path):
    reply_list = []
    with open(input_path, "r", encoding="utf-8") as f:
        for line in f:
            data = json.loads(line)
            # 提取result.replys内容（假设字段存在）
            replys = data.get("result", {}).get("replys", {})
            if replys:
                for reply in replys:
                    reply_list.append(
                        Reply(
                            str(reply.get("id")),
                            str(reply.get("content")),
                            str(reply.get("now")),
                            str(reply.get("userid")),
                        )
                    )
    return reply_list


def html_to_txt(html_content):
    # 替换HTML标签为适合TXT的格式
    txt_content = html_content.replace("<br />", "").replace("&gt;", ">")

    return txt_content.strip()


def get_reply_string(reply):
    txt_content = f"No.{reply.id} {reply.time} {reply.user_id}\n"
    txt_content += html_to_txt(reply.content)
    txt_content += "\n\n\n"
    return txt_content


def create_txt(first_content, replys, name, output_path):
    file_path = os.path.join(output_path, f"{name}.txt")
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(get_reply_string(first_content))
        for reply in replys:
            f.write(get_reply_string(reply))


if __name__ == "__main__":
    with open("./config/backup_txt.json", "r", encoding="utf-8") as f:
        backup_data = json.loads(f.read())
        data_list = backup_data.get("json_list")
        path = os.path.dirname(os.path.abspath(__file__))
        output_path = backup_data.get("output_path")
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        for name, input_path in data_list.items():
            input_path = f"{path}/{input_path}"
            first_content = get_first_content(input_path)
            replys = get_reply(input_path)
            create_txt(first_content, replys, name, output_path)
