#!flask/bin/python
import os
import sys
import pyhdb
from flask import Flask, jsonify, request, json

app = Flask(__name__)
port = int(os.getenv("PORT", 8181))

tasks = [
    {
        'id': 0,
        'title': u'Create GET function',
        'description': u'This function shows list of todo items.\n And this item is already done :)',
        'link': '/api/v1.0/task',
        'done': True
    },
    {
        'id': 1,
        'title': u'Create POST function',
        'description': u'POST function is located on /api/v1.0/save',
        'url': '/api/v1.0/save',
        'done': True
    },
    {
        'id': 2,
        'title': u'Create connection to DB',
        'description': u'Create binding from this API to HANA DB in Cloud foundry environment.',
        'url': '/api/v2.0/db',
        'done': True
    },
    {
        'id': 3,
        'title': u'Insert values into table',
        'description': u'SQL script will be executed by cursor from pyhdb library.',
        'url': '/api/v2.0/db',
        'done': True
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

def save_data(data):
    with open('.//API_data.txt', 'a') as f:
        f.write(data+'\n')

#def printer(message):
#    return message

@app.route('/api/v2.0/db', methods = ['POST'])
def save_to_HANA():
    # Get posted json data.
    if request.headers['Content-Type'] == 'application/json' or request.headers['Content-Type'].lower() == 'application/json; charset=utf-8':# or request.headers['Content-Type'] == 'multipart/form-data':
        json_hana = json.loads(json.dumps(request.json))
        host = json_hana['host']
        port = json_hana['port']
        user = json_hana['user']
        password = json_hana['password']

        if "schema" in json_hana:
            schema = json_hana["schema"]
        else:
            schema = None

        data = json_hana['data']


        data_dict = eval(data)

        text = data_dict["text"]
        price = data_dict["price"]

        info_conn = '|info| Connection to {}:{} .'.format(host, port)

        save_connDB(host, port, user, password, schema, text, price)

        response_stH = 'All data is posted: ' + '\n' + str(data)
        return info_conn + '\n' + response_stH


def save_connDB(host_, port_, user_, password_, schema_, text_, price_):
    connection = pyhdb.connect(
        host = host_,
        port = port_,
        user = user_,
        password = password_)

    create = "CREATE TABLE TEST(text varchar(255), price float);"
    insert = "INSERT INTO TEST_TABLE (text, price) VALUES ({}, {});".format('\''+text_+'\'', price_)
    
    cursor = connection.cursor()

    try:
        cursor.execute(create)
        cursor.execute(insert)
    except:
        cursor.execute(insert)

    connection.commit()
    connection.close()

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = port, debug=True)
