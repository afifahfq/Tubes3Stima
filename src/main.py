'''ini program utama'''

from flask import Flask, url_for, render_template, request,  redirect
from flask_socketio import SocketIO
from MainRegex import *


app = Flask(__name__)
socketio = SocketIO(app)
#gatau ini apaan, tapi perlu ada secret key
app.config['SECRET_KEY'] = "ini_rahasia_kita"
username = ""

#ini buat ngerender halaman awal
@app.route('/')
def appearance():
    #Halaman awal bisa diliat di Home.html
    return render_template("Home.html")

#ini buat konfirmasi botnya sudah keconnect sama user apa belum
@socketio.on('bot_arrive')
def handle_bot_arrive(data):
    message = getBotArrivalMessage()
    socketio.emit("bot_arrive_message",{"username": data['username'], "message":message, "alert": "Butler-san is on your service" })

#ini buat nampilin inputan message user ke chat wall
@socketio.on('send_message')
def handle_send_message(data):
    socketio.emit('post_user_message', data)

#ini buat ngambil message dari bot terus oper fungsi buat nampilin message
@socketio.on('get_bot_message')
def handle_get_bot_message(data):
    print(data)
    bot_message = getBotMessage(data['user_message'])
    print(bot_message)
    socketio.emit('post_bot_message', {"bot_message":bot_message})

#ini buat render setelah user masukin nama
@app.route('/chat')
def chat():
    username = request.args.get("username")
    print(username)
    if(username):
        return render_template("chat.html", username = username)
    else:
        return redirect(url_for('appearance'))

#ini gatau wkwkwk, tapi buat mulai Flask
if __name__ == '__main__':
    socketio.run(app, debug=True)