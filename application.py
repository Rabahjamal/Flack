import os

from flask import Flask, request, render_template, redirect, url_for, flash
from flask_socketio import SocketIO, emit, send
from flask_session import Session
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
    return render_template("channel.html", channel_name=channel_name)

@app.route("/new_channel", methods=["POST"])
def new_channel():
    channel_name = request.form.get("channel_name")

    if channel_name in channels:
        flash("This channel is already exist!")
        return redirect(url_for("home"))
    else:
        channels[channel_name] = Message(None, None, None)
        return redirect(url_for("home"))

@socketio.on('new message')
def handle_message(data):
    message = data["message_text"]
    print(message)
    emit("messages", message, broadcast=True)
    #print('Message: ' + data)
    #send(data, broadcast=True)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
    #socketio.run(app)
