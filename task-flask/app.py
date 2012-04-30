from subprocess import call

from flask import Flask, request
from twilio import twiml
from twilio.rest import TwilioRestClient

import config

app = Flask(__name__)
client = TwilioRestClient(config.TWILIO_ACCOUNT, config.TWILIO_TOKEN)


@app.route("/", methods=["POST"])
def hello():
    message = lambda msg: client.sms.messages.create(to=request.form.get('From'), from_=request.form.get('To'), body=msg)

    task = request.form.get('Body')
    if task:
        code = call(['/usr/local/bin/task', 'add', task])
        message('ok' if code == 0 else 'oh no!')
    else:
        message('specify task')

    return str(twiml.Response())


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9000)
