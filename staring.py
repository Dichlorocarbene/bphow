from flask import Flask, request
import rules

bphow = Flask(__name__)


@bphow.route('/', methods=["POST"])
def post_data():
    '下面的request.get_json().get......是用来获取关键字的值用的，关键字参考上面代码段的数据格式'
    if request.get_json().get('message_type') == 'private':  # 如果是私聊信息
        uid = request.get_json().get('sender').get('user_id')  # 获取信息发送者的 QQ号码
        message = request.get_json().get('raw_message')  # 获取原始信息
        print(request.get_json())
        rules.commands(message, uid)
    # api.keyword(message, uid)  # 将 Q号和原始信息传到我们的后台

    if request.get_json().get('message_type') == 'group':  # 如果是群聊信息
        gid = request.get_json().get('group_id')  # 获取群号
        uid = request.get_json().get('sender').get('user_id')  # 获取信息发送者的 QQ号码
        message = request.get_json().get('raw_message')  # 获取原始信息
        # print("[" + uid + " from " + gid + "]" + message)
        print(request.get_json())
        rules.commands(message, uid, gid)  # 将 Q号和原始信息传到我们的后台

    return 'OK'


if __name__ == '__main__':
    bphow.run(debug=True, host='127.0.0.1', port=5701)  # 此处的 host和 port对应上面 yml文件的设置
