# a_backup
a岛数据备份脚本，目前可以根据串号下载为json，但是由于存在反爬机制，可能会出现断联，建议调大爬取时间间隔，如果下载中断再次启动会从中断位置继续。

# 使用说明
## 登录信息
阿苇岛需要图片验证，暂未实现自动登录，需要手动注入cookie 登录阿苇岛，F12获取cookie信息填入config文件cookies中，以chrome浏览器为例，所有信息复制过去
![image](https://github.com/user-attachments/assets/496d0591-0400-4751-90c7-6101b5212663)


## 爬取数据
config文件 all list中以“串号:描述”格式写入

## 生成txt

现在可以将json生成txt了

## backup
存放已爬取文件

