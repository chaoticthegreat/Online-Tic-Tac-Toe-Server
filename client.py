from flask import Flask,request
from threading import Thread
import time, random, requests


r = requests.get("https://Online-Tic-Tac-Toe-Server.proryan.repl.co/Ryan")


print(r.json())
r2 = requests.get("https://Online-Tic-Tac-Toe-Server.proryan.repl.co/match/"+str(r.json()["match_id"])).json()["match_found"]
while r2 == False:
  r2 = requests.get("https://Online-Tic-Tac-Toe-Server.proryan.repl.co/match/"+str(r.json()["match_id"])).json()["match_found"]
r3 = requests.post("https://Online-Tic-Tac-Toe-Server.proryan.repl.co/server/", json={"match_id":r.json()["match_id"], "X":True, "input":"1 2"})
print(r3.json())

  

