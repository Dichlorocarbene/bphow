import requests as r
import constants as c

# group message


def send_group_message(group_id: int, content: str):
    link = c.group_msg + "group_id=" + str(group_id) + "&message=" + content
    print(link)
    t = r.post(url=link)
    return t


def send_private_message(user_id: int, content: str):
    link = c.private_msg + "user_id=" + str(user_id) + "&message=" + content
    print(link)
    t = r.post(url=link)
    return t
