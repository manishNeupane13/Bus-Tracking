
from flask import Flask, render_template
import socket
import time
from database_conn import realtime_db_connection
app = Flask(__name__)
# host device name
hostname = socket.gethostname()
# get ip address
ip_address = socket.gethostbyname(hostname)
port = 9000


@app.route('/<string:fareamount>', methods=['POST', 'GET'])
def home(fareamount):
    return render_template('demo.html', amount=float(fareamount), tranid=f'fare{time.time()}')


if __name__ == '__main__':

    app.run(host=ip_address, port=port, debug=True)
