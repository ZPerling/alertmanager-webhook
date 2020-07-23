from dingtalkchatbot.chatbot import DingtalkChatbot
from flask import render_template
from json import loads as json_loads
from app import app
from app_log import MyLog

my_log = MyLog()


def send_ding_message(webhook, text, title="新消息", secret=None, is_at_all=False, at_mobiles=[]):
    try:
        Ding = DingtalkChatbot(webhook=webhook, secret=secret)
        ret = Ding.send_markdown(title=title, text=text, at_mobiles=at_mobiles, is_at_all=is_at_all)
        if ret['errcode'] == 0:
            my_log.console_log_logger.info("send ding success")
            return None
        else:
            my_log.console_log_logger.info("send ding failed, %s" % ret['message'])
            return ret['message']
    except Exception as error:
        my_log.console_log_logger.info("send ding failed, %s" % str(error))
        return str(error)


def alertmanager_json_to_markdown(alert_data):
    with app.app_context():
        if isinstance(alert_data, str):
            context = json_loads(alert_data)
        else:
            context = alert_data
        render = render_template('ding.html', **context)
        return render
