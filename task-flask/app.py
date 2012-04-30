from subprocess import call

from flask import Flask, request
from twilio import twiml
from twilio.rest import TwilioRestClient

import config

app = Flask(__name__)
client = TwilioRestClient(config.TWILIO_ACCOUNT, config.TWILIO_TOKEN)


@app.route("/", methods=["POST"])
def hello():
    def message(msg):
        client.sms.messages.create(to=request.form.get('From'), from_=request.form.get('To'), body=msg)
        return str(twiml.Response())

    if request.form.get('From') != config.MY_PHONE_NUMBER or request.form.get('To') != config.MY_TWILIO_NUMBER:
        return message('go away')

    task = request.form.get('Body')
    if not task:
        return message('specify task')

    code = call(['/usr/local/bin/task', 'add', task])
    return message('ok' if code == 0 else 'oh no!')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9000)
