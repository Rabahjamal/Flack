import os

from flask import Flask, request, render_template, redirect, url_for, flash, abort
from flask_socketio import SocketIO, emit, send
from flask_session import Session
import jsons
from message import *

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
#app.config["SESSION_PERMANENT"] = False
#app.config["SESSION_TYPE"] = "filesystem"
#Session(app)
socketio = SocketIO(app)

#channels = [Channel("atary", 1), Channel("alaa", 2)]
channels = dict()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/home")
def home():
    return render_template("home.html", channels=channels)

@app.route("/channel/<string:channel_name>")
def channel(channel_name):
    if channel_name in channels:
        return render_template("channel.html", channel_name=channel_name)
    else:
        return abort(404)

@app.route("/new_channel", methods=["POST"])
def new_channel():
    channel_name = request.form.get("channel_name")

    if channel_name in channels:
        flash("This channel is already exist!")
        return redirect(url_for("home"))
    else:
        channels[channel_name] = [jsons.dump(Message(None, None, None, None))]
        return redirect(url_for("home"))

@socketio.on('new message')
def handle_message(data):
    message = data["message_text"]
    sender = data["sender"]
    channel_name = data["channel_name"]
    #channels[channel_name].append(Message(sender, message, None))
    channels[channel_name].append(jsons.dump(Message(sender, message, None, channel_name)))
    if len(channels[channel_name]) == 101:
        del channels[channel_name][1]
    print(message + ': ' + sender + ', ' + channel_name)
    emit("messages", jsons.dump(Message(sender, message, None, channel_name)), broadcast=True)
    #print('Message: ' + data)
    #send(data, broadcast=True)

@socketio.on('new connection')
def handle_connection(data):
    channel_name = data["channel_name"];
    emit("connection", channels[channel_name], broadcast=False)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
    #socketio.run(app)
