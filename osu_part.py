# rubbish bin

import requests as r
import json
import constants as c


def get_map(map_set_id: int = None, map_id: int = None, limit: int = 500) -> dict:
    if map_set_id is None:
        if map_id is None:
            raise Exception("? why not input an id")
        else:
            param = {
                "k": c.api_key,
                "b": map_id,
            }
    else:
        param = {
            "k": c.api_key,
            "s": map_set_id,
        }
    return param


def get_user_best(user_id: int or str, limit: int = 100, id_type: str = "name") -> dict:
    param = {
        "k": c.api_key,
        "u": user_id,
        "limit": limit
    }
    return param


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


"http://127.0.0.1:5700/send_private_msg?user_id=&message="

"http://127.0.0.1:5700/send_group_msg?group_id=624253429&message=233333"

if __name__ == '__main__':
    t = r.get(c.bp_base_url, params=get_user_best("crove0301"))

    maps = json.loads(t.text)
