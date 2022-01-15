import random as rd
import json
import msg_part as m
import constants as c
import re
import osu_part as o


def commands(message, uid, gid=None):
    if gid is not None:
        if re.match("^(!|！)roll ?-?\d*$", message):
            num = message[5:].strip()
            if num == "":
                m.send_group_message(group_id=gid, content=roll())
            else:
                m.send_group_message(group_id=gid, content=roll(int(num)))

        if re.match("^(!|！)pi ?[\w\-\[\]]*$", message):
            osu_id = message[3:].strip()
            if osu_id == "":
                m.send_group_message(group_id=gid, content=o.get_user_personinfo(c.qq_dict[uid]))
            else:
                m.send_group_message(group_id=gid, content=o.get_user_personinfo(osu_id))

    else:
        if re.match("^(!|！)roll ?-?\d*$", message):
            num = message[5:].strip()
            if num == "":
                m.send_private_message(user_id=uid, content=roll())
            else:
                m.send_private_message(user_id=uid, content=roll(int(num)))
    # if message == "呃":
    #     m.send_group_message(group_id=gid, content="不许呃")
    # elif re.match("^！roll ?-?\d*$", message):
    #     m.send_group_message(group_id=gid, content="请使用半角")


def roll(maxnum: int = 100) -> str:
    if maxnum > 1000:
        res = rd.randint(1, 1000)
        return str(res) + "（随机数有上限哦~"
    elif maxnum <= 0:
        return "嗯？"
    else:
        res = rd.randint(1, maxnum)
        return str(res)

