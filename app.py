from flask import Flask, request

import system_info

app = Flask(__name__)


@app.route('/get-info', methods=['POST'])
def get_items_info():
    form = request.form
    host = form.get('host')
    port = form.get('port')
    username = form.get('username')
    password = form.get('password')
    storage_name = form.get('storage')
    database = form.get('database')
    table = form.get('table')
    return {'status': 200}


@app.route('/ping', methods=['POST'])
def ping():
    return {'status': 200}


@app.route('/info', methods=['POST'])
def info():
    return system_info.get_system_info()


if __name__ == '__main__':
    app.run()
