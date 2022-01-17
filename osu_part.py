# rubbish bin
import matplotlib.pyplot as plt
import requests as r
import json
import constants as c
import os
import datetime as d
from matplotlib import pyplot
import numpy as np
import msg_part as m

# maps content
with open(c.mapping_dic_path, "r") as fp:
    mapping_dic = json.load(fp)


# def get_map(map_set_id: int = None, map_id: int = None, limit: int = 500) -> dict:
#     if map_set_id is None:
#         if map_id is None:
#             raise Exception("? why not input an id")
#         else:
#             param = {
#                 "k": c.api_key,
#                 "b": map_id,
#             }
#     else:
#         param = {
#             "k": c.api_key,
#             "s": map_set_id,
#         }
#     return param


def get_user_best(user_id: int or str, limit: int = 100) -> dict or int:
    param = {
        "k": c.api_key,
        "u": user_id,
        "limit": limit
    }
    bpp = r.get(c.bp_base_url, params=param)
    bp = json.loads(bpp.text)
    if not bp:
        return 0
    else:
        return bp


def get_user_personinfo(user_id: int or str, event_days: int = 1) -> str:
    param = {
        "k": c.api_key,
        "u": user_id,
        "event_days": event_days
    }
    pi = r.get(c.info_base_url, params=param)
    pii = json.loads(pi.text)
    if not pii:
        return "查不到捏"
    else:
        info = pii[0]

        # 好像会限制字符个数诶
        # res = info['username'] \
        #       + "\nTotal pp -- " + info['pp_raw'] \
        #       + "\nAccuracy -- " + info['accuracy'][0:5] \
        #       + "\nGlobal rank -- " + info['pp_rank'] \
        #       + "\n" + info['country'] + " %23" + info['pp_country_rank'] \
        #       + "\nPlay count --" + info['playcount']

        res = info['username'] \
              + "\n" + info['pp_raw'] + "pp" \
              + "(" + info['accuracy'][0:5] + "%25)" \
              + "\n" + "%23" + info['pp_rank'] \
              + "(" + info['country'] + "%20%23" + info['pp_country_rank'] + ")" \
              + "\n" + info['playcount'] + "pc"

        return res


def get_user_recent(user_id: int or str, num: int = 1):
    param = {
        "k": c.api_key,
        "u": user_id,
        "limit": num,
    }
    pi = r.get(c.re_base_url, params=param)
    pii = json.loads(pi.text)
    if not pii:
        return "快去打"
    elif len(pii) < num:
        return "你没打那么多"
    else:
        inquiry = pii[num-1]
        res = "还没写完呢查不出来的hhhhh"

    return res


def curve(user_id: int or str):
    param = {
        "k": c.api_key,
        "u": user_id,
    }
    pi = r.get(c.info_base_url, params=param)
    pii = json.loads(pi.text)
    if not pii:
        return "查不到捏"
    else:
        username = pii[0]['username']
        bp = get_user_best(username)
        now_time = d.datetime.now()
        bpp = bplist(bp, now_time)
        name_path = bpp.draw_bar(username)
        return m.cq_pic(name_path)


def find_beatmap(filepath: str, beatmap_id):
    pass


class bplist(object):
    def __init__(self, bpdict, time_now):
        self.only_time = d.datetime.strftime(time_now, '%Y-%m-%d %H:%M:%S')
        self.name = d.datetime.strftime(time_now, '%Y-%m-%d-%H-%M-%S')
        self.count = len(bpdict)
        self.pp_list = [float(i["pp"]) for i in bpdict]
        self.weight_pp = [self.pp_list[i] * c.weight_list[i] for i in range(self.count)]
        self.accuracy = [accuracy(int(i["count300"]), int(i["count100"]), int(i["count50"]), int(i["countmiss"])) for i in bpdict]
        self.isin24h = [d.datetime.strptime(i["date"], '%Y-%m-%d %H:%M:%S') + d.timedelta(hours=8) + d.timedelta(days=1) >= time_now for i in bpdict]

    def draw_bar(self, username):
        fig, ax1 = plt.subplots(figsize=(14, 9), dpi=80)
        labels = [i+1 for i in range(self.count)]
        delta_pp = [self.pp_list[i] - self.weight_pp[i] for i in range(self.count)]
        delta_pp_color = ["yellow" if i else "palegreen" for i in self.isin24h]
        weight_pp_color = ["blue" if i else "cyan" for i in self.isin24h]
        ax1.bar(labels, self.weight_pp, color=weight_pp_color, width=0.4)
        ax1.bar(labels, delta_pp, color=delta_pp_color, width=0.4, bottom=self.weight_pp)
        ax1.set_ylabel("Performance Point")
        ax1.set_ylim(0, max(self.pp_list) + 1)

        ax2 = ax1.twinx()
        ax2.plot(labels, self.accuracy, color='red', label="Accuracy")
        ax2.set_ylabel("Accuracy")
        ax2.set_ylim(0.7, 1.0)

        fig.legend()
        plt.xlim(0, 100.5)
        plt.title(username + "'s bp(new bp) -- " + self.only_time + "(UTC+8)")
        file_path = c.bp_check_pic_path + username + "-" + self.name + ".jpg"
        plt.savefig(file_path)
        return file_path


def accuracy(num_of_300: int, num_of_100: int, num_of_50: int, num_of_miss: int) -> float:
    acc = (50 * num_of_50 + 100 * num_of_100 + 300 * num_of_300) / (300 * (num_of_300 + num_of_100 + num_of_50 + num_of_miss))
    return np.round(acc, 4)


if __name__ == '__main__':
    mapp = get_user_best("lukazi")
    t = d.datetime.now()
    crove = bplist(mapp, t)
    crove.draw_bar("lukazi")
