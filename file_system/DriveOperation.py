from file_system import FileSystem
from flask import Flask, request, render_template, send_from_directory

app = Flask(__name__)
filesystem = FileSystem()
@app.route('/')
def home():
    return render_template()("FileOperation.html")

@app.route("/create", methods = ["POST", "PUT", "GET"])
def create():
    dir = request.args.get("directory")
    filename = request.args.get("filename")
    filetype = request.args.get("filetype")
    filesystem.create("Drive",filename,dir)

@app.route("/delete", methods = ["DELETE", "GET"])
def delete():
    dir = request.args.get("directory")
    filesystem.delete(dir)

@app.route("/move", methods = ["POST", "PUT", "GET"])
def move():
    dir = request.args.get("directory")
    destination_path = request.args.get("destination_path")
    filesystem.move(dir,destination_path)

@app.route("/write",methods = ["POST", "PUT", "GET"])
def write():
    dir = request.args.get("directory")
    content = request.args.get("content")
    filesystem.wirteToFile(dir,content)

@app.route("/list", methods = ["GET", "PUT","POST"])
def list():
    dir = request.args.get("directory")
    filesystem.getEntityFromPath(dir)