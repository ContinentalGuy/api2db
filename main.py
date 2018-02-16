#!flask/bin/python
import os
import pyhdb
from flask import Flask, jsonify, request, json

app = Flask(__name__)
port = int(os.getenv("PORT", 8181))

tasks = [
    {
        'id': 0,
        'title': u'Create GET function',
        'description': u'This function shows list of todo items.\n And this item is already done :)',
        'done': True
    },
    {
        'id': 1,
        'title': u'Create POST function',
        'description': u'POST function is located on /api/v1.0/save',
        'done': True
    },
    {
        'id': 2,
        'title': u'Create connection to DB',
        'description': u'Create binding from this API to HANA DB in Cloud foundry environment.',
        'done': False
    }
]

@app.route('/api/v1.0/task', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@app.route('/api/v1.0/save', methods=['POST'])
def post_tasks():
    if request.headers['Content-Type'] == 'application/json' or request.headers['Content-Type'].lower() == 'application/json; charset=utf-8':

        json_string = json.loads(json.dumps(request.json))
        pt_resp = jsonify({'data' : json_string})
        save_data(str(json_string))
        return(pt_resp)

    else:
        return bad_request()

@app.errorhandler(404)
def bad_request():
    br_err = {
        'message' : 'Bad request.',
        'alternative' : 'Problems with headers.'
        }
    br_resp = jsonify(br_err)
    return br_resp

@save_to_HANA
def save_data(data):
    with open('.//API_data.txt', 'a') as f:
        f.write(data+'\n')

class save_to_HANA(object):
    def __init__(self, arg0):
        self.arg0 = arg0
        print('Inside __init__()\nself.arg0 = {}'.format(arg0))

    def __call__(self, decorated_function):
        print('Inside __call__()\nRun function "save_2_DB".')
        decorated_function(self.arg0)
        self.save_2_DB(self.arg0)

    def save_2_DB(self, data):
        connection = pyhdb.connect(python decorators use numerous arguments
            host = "<CloudFoundry_productive_account_host>",
            port = 30015,
            user = "CloudFoundry_productive_account_user",
            password = "CloudFoundry_productive_account_password")

        cursor = connection.cursor()
        cursor.execute("INSERT INTO ELPIS_TABLE VALUES {}".format(data))
        cursor.fetchone()
        connection.close()

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = port, debug=True)
