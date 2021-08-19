from flask import Flask
import datetime
import requests
import json
import config_app
import sys
app = Flask(__name__)
config = config_app
url = config.url

@app.route('/')
def index():
    return "<h1>Root!!</h1>"

@app.route('/kekaLogin')
def login():
    kekaLoginLogout(True)
    return 'Login Work!!'

@app.route('/kekaLogout')
def logout():
    kekaLoginLogout(False)
    return 'Logout Work!!'

def kekaLoginLogout(isClockIn):
    payload = json.dumps({
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "attendanceLogSource": 1,
        "locationAddress": {
            "longitude": config.longitude,
            "latitude": config.latitude,
            "zip": config.zip,
            "countryCode": config.countryCode,
            "state": config.state,
            "city": config.city,
            "addressLine1": config.addressLine1,
            "addressLine2": config.addressLine2
        },
        "manualClockinType": 3,
        "note": "",
        "originalPunchStatus": isClockIn if 0 else 1
    })
    headers = {
        'Cookie': config.cookie,
        'Authorization': config.authorization,
        'Content-Type': 'application/json'
    }
    try:
        response = requests.post(url, data=payload, headers=headers)
        print(response.status_code)
        responseData = json.loads(response.text)
        if len(responseData['request']['timeEntries']) > 0 :
            if isClockIn:
                slackNotification('HR Said Login Succeeded!!!!')
            else: slackNotification('HR Said Logout Succeeded!!!!')
        else: slackNotification(response.text)
    except requests.exceptions.HTTPError as e:
        print(e.response.text)
        slackNotification(e.response.text)

def slackNotification(message):
    url = config.Webhook_URL
    message = message
    title = (f"New Incoming Message :zap:")
    slack_data = {
        "username": "Skyboybadal Notification bot",
        "icon_emoji": ":satellite:",
        #"channel" : "#somerandomcahnnel",
        "attachments": [
            {
                "color": "#9733EE",
                "fields": [
                    {
                        "title": title,
                        "value": message,
                        "short": "false",
                    }
                ]
            }
        ]
    }
    byte_length = str(sys.getsizeof(slack_data))
    headers = {'Content-Type': "application/json", 'Content-Length': byte_length}
    response = requests.post(url, data=json.dumps(slack_data), headers=headers)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)