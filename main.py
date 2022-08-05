from flask import Flask,request
from threading import Thread
import time, random,sys

app = Flask(__name__)
clients = {}
servercount = 0
servers = {}
runningserver = {}

@app.route("/")
def hello_world():
  return "Hello World"
@app.route("/<username>/")
def matchmaker(username):
  global servercount, clients, servers, runningserver
  while True:
    if len(servers.keys()) >= 1:
      runningserver[list(servers.keys())[0]] = {
        "Username": [servers[list(servers.keys())[0]]["Username"], username],
      "X": [],
      "O": [],
      "Empty": ["1", "2", "3", "4", "5", "6","7", "8", "9"],
      "Win":None}
      del servers[list(servers.keys())[0]]
      return {"match_id": list(runningserver.keys())[0], "base_storage": runningserver[list(runningserver.keys())[0]], "match_found": True}
    else:
      match_id = random.randint(1000000, 9999999)
      if match_id not in servers.keys():
        servers[match_id] = {
          "Username": username,
          "X": [],
          "O": [],
          "Empty": ["1", "2", "3", "4", "5", "6","7", "8", "9"],
          "Win":None}
      return {"match_id": match_id, "match_found": False}
@app.route("/match/<int:match_id>/")
def matchcheck(match_id):
  if match_id in runningserver.keys():
    return {"match_found":True}
  else:
    return {"match_found":False}
@app.route("/server/", methods=["GET", "POST"])
def server():
  global runningserver
  if request.method == "GET":
    jsondata = request.json
    try:
      return runningserver[int(jsondata["match_id"])]
    except KeyError:
      return {"kicked":True}
  elif request.method =="POST":
    jsondata = request.json
    if jsondata["X"] == True:
      runningserver[int(jsondata["match_id"])]["X"].append(jsondata["input"])
      try:
        runningserver[int(jsondata["match_id"])]["Empty"].remove(jsondata["input"])
      except ValueError: 
        print(runningserver[int(jsondata["match_id"])])
        print(jsondata["input"])
    else:
      runningserver[int(jsondata["match_id"])]["O"].append(jsondata["input"])
      runningserver[int(jsondata["match_id"])]["Empty"].remove(jsondata["input"])
    theBoard=runningserver[int(jsondata["match_id"])]
    if len(theBoard["X"])+len(theBoard["O"]) >= 5:
      if all(x in theBoard["X"] for x in ['7', '8',"9"]) or all(x in theBoard["O"] for x in ['7', '8',"9"]): # across the top
        if jsondata["X"]==True:runningserver[int(jsondata["match_id"])]["Win"]="X"
        else: runningserver[int(jsondata["match_id"])]["Win"]="O"
      elif all(x in theBoard["X"] for x in ['4', '5',"6"]) or all(x in theBoard["O"] for x in ['4', '5',"6"]): # across the middle
        if jsondata["X"]==True:runningserver[int(jsondata["match_id"])]["Win"]="X"
        else: runningserver[int(jsondata["match_id"])]["Win"]="O"
      elif all(x in theBoard["X"] for x in ['1', '2',"3"]) or all(x in theBoard["O"] for x in ['1', '2',"3"]): # across the bottom
        if jsondata["X"]==True:runningserver[int(jsondata["match_id"])]["Win"]="X"
        else: runningserver[int(jsondata["match_id"])]["Win"]="O"
      elif all(x in theBoard["X"] for x in ['1', '4',"7"]) or all(x in theBoard["O"] for x in ['1','4','7']): # down the left side
        if jsondata["X"]==True:runningserver[int(jsondata["match_id"])]["Win"]="X"
        else: runningserver[int(jsondata["match_id"])]["Win"]="O"
      elif all(x in theBoard["X"] for x in ['2', '5',"8"]) or all(x in theBoard["O"] for x in ['2', '5',"8"]): # down the middle
        if jsondata["X"]==True:runningserver[int(jsondata["match_id"])]["Win"]="X"
        else: runningserver[int(jsondata["match_id"])]["Win"]="O"
      elif all(x in theBoard["X"] for x in ['2', '5',"8"]) or all(x in theBoard["O"] for x in ['2', '5',"8"]): # down the right side
        if jsondata["X"]==True:runningserver[int(jsondata["match_id"])]["Win"]="X"
        else: runningserver[int(jsondata["match_id"])]["Win"]="O"
      elif all(x in theBoard["X"] for x in ['3', '5',"7"]) or all(x in theBoard["O"] for x in ['3', '5',"7"]): # diagonal
        if jsondata["X"]==True:runningserver[int(jsondata["match_id"])]["Win"]="X"
        else: runningserver[int(jsondata["match_id"])]["Win"]="O"
      elif all(x in theBoard["X"] for x in ['1', '5',"9"]) or all(x in theBoard["O"] for x in ['1', '5',"9"]): # diagonal
        if jsondata["X"]==True:runningserver[int(jsondata["match_id"])]["Win"]="X"
        else: runningserver[int(jsondata["match_id"])]["Win"]="O"
    return runningserver[int(jsondata["match_id"])]

@app.route("/check/", methods = ["POST"])
def check():
  global clients
  username = request.json["username"]
  checking=request.json["checking"]
  
  if username in clients.keys() and checking==True:
    return {"Username":False, "Kick":False}
  if username not in clients.keys():
    clients[username] = {"Alive":True, "Kick":False}
    return {"Username":True, "Kick":False}
  clients[username]["Alive"] = True
  if clients[username]["Kick"] == True:
    return {"Username": True, "Kick":True}
  print("Verified,", username)
  return {"Username":True, "Kick":False}
def heartbeat():
  global clients, servers, runningserver
  while True:
    time.sleep(7.5)
    for client in list(clients):
      if clients[client]["Alive"] == False:
        print("Removing", client)
        del clients[client]
        for id in list(servers):
          if client in servers[id]["Username"]:
            del servers[id]
        for id in list(runningserver):
          if client in runningserver[id]["Username"]:
            runningserver[id]["Username"].remove(client)
            clients[runningserver[id]["Username"][0]]["Kick"] = True
            del runningserver[id]
      else:
        clients[client]["Alive"] = False

def run():
  app.run(host = '0.0.0.0', port = 3000, debug = False)

Thread(target = heartbeat).start()
Thread(target = run).start()