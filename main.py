#!/usr/local/bin/python2.7

import sys
import os
from pprint import pprint
import datetime
import base64
from crontab import CronTab

from flask import Flask, render_template, request, redirect


# load flask app
# keep at the top
app = Flask(__name__, instance_relative_config=True)
app.config['APPLICATION_ROOT'] = '/cron'

def get_auth_user():
    try:
        b = request.headers.get('Authorization')
        user = base64.b64decode(b.replace('Basic ', '')).split(':')[0]
    except:
        user = 'unknown'
    return user

@app.route('/', methods=['GET'])
def list_crontabs():
    crons=CronTab(user=True)

    return render_template('list_crons.html', crons=crons)


@app.route('/change', methods=['POST'])
def save_changes():
    hour = request.form['hour']
    minute = request.form['minute']
    command = request.form['command']

    crons = CronTab(user=True)
    for i in range(len(crons)):
        if crons[i].command  == command:
            request.headers.get('User-Agent')
            print "DEBUG: Updating cron for %s with hour %s and minute %s" % (command, hour, minute)
            crons[i].hour.on(hour)
            crons[i].minute.on(minute)
            crons[i].set_comment('Updated by %s on %s' % (get_auth_user(),
                datetime.datetime.now().isoformat()))

    crons.write_to_user( user=True )
    return 'changes saved'

@app.route('/debug', methods=['GET'])
def list_h():
    return request.headers.get('Authorization')

if __name__ == '__main__':
    app.run(debug=True, port=4500, host='0.0.0.0')

# vim: ts=4 expandtab noai

