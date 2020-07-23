from flask import Flask, request, Response
from config import get_config
from json import dumps as json_dumps
from app_log import MyLog

my_log = MyLog()
app = Flask(__name__)


@app.template_filter('format_time')
def format_time_filter(s):
    import time
    from datetime import datetime
    try:
        ts = time.mktime(datetime.strptime(s.split('.')[0], "%Y-%m-%dT%H:%M:%S").timetuple()) + 3600 * 8
        return datetime.fromtimestamp(int(ts)).strftime('%Y-%m-%d %H:%M:%S')
    except Exception as error:
        return str(error)


@app.route('/health')
def health_check():
    return 'I am healthy!'


@app.route('/webhook', methods=['POST'])
def web_hook():
    from ding import send_ding_message, alertmanager_json_to_markdown
    config_data = get_config()
    robot = request.args.get('robot')
    robot_info = config_data["robot"].get(robot)
    response_data = {
        "code": 200,
        "message": None
    }
    if not robot_info:
        response_data['code'] = 400
        response_data['message'] = "Failed send message, robot config not found!"
    data = request.get_json()
    my_log.log_to_file_logger.info(json_dumps(data))
    ret = send_ding_message(webhook=robot_info.get('webhook'),
                            secret=robot_info.get('secret'),
                            text=alertmanager_json_to_markdown(data))

    if not ret:
        response_data['message'] = 'Send successful'
    else:
        response_data['message'] = ret
        response_data['code'] = 400
    my_log.console_log_logger.info("robot: %s, response: %s" % (robot, json_dumps(response_data)))
    my_log.log_to_file_logger.info("robot: %s, response: %s" % (robot, json_dumps(response_data)))
    return Response(json_dumps(response_data), status=response_data['code'], mimetype='application/json')


if __name__ == '__main__':
    app.run()
