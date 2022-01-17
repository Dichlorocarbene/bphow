import requests as r
import constants as c
import warnings as w
# group message


def send_group_message(group_id: int, content: str):
    link = c.group_msg + "group_id=" + str(group_id) + "&message=" + content
    print(link)
    __len_check(link)
    t = r.post(url=link)
    return t


def send_private_message(user_id: int, content: str):
    link = c.private_msg + "user_id=" + str(user_id) + "&message=" + content
    print(link)
    __len_check(link)
    t = r.post(url=link)
    return t


def __len_check(st):
    if len(st) > 1000:
        w.warn("sent message too long")


def cq_pic(filepath):
    pic = "[CQ:image,file=" + c.working_path + filepath + "]"
    return pic
