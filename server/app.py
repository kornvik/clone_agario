import time
from flask import Flask, render_template, request
from ngrok_utils import start_ngrok
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
import json
from MyAgar import *
import threading
import numpy as np

app = Flask(__name__)

players = {}
game = None
stop_game = False

PORT = 6500

class GameThread(threading.Thread):
    def __init__(self,game_env=None):
        threading.Thread.__init__(self)
        self.game_env = game_env
        self.game_env.create_food(prob=False)
    
    def run(self):
        global stop_game
        global players
        global game

        stop_game = False
        while not stop_game:
            
            food_del = self.game_env.update()
            snapshot = self.game_env.get_snapshot()
            food_add = self.game_env.create_food()
            leader_board = self.game_env.get_leader_board()
            
            ## Send the snapshot to everybody in players ##
            for p in list(players.keys()):
                me = snapshot[p]
                refx,refy = me["xpos"],me["ypos"]
                blobs = []
                
                for u in snapshot:
                    if u!=p:
                        tmp = snapshot[u]["blobs"]
                        for b in tmp:
                            blobs.append({"xpos":b["xpos"],"ypos":b["ypos"],"radius":b["radius"],"skin":b["skin"],"name":b["name"]})

                info = {"food_add":food_add,"food_del":food_del,"blobs":blobs,"me":{"xpos":refx,"ypos":refy,"alive":me["alive"],"score":me["score"],"blobs":snapshot[p]["blobs"]},"leader_board":leader_board}
                
                response = {"cmd" : "players","info":info}

                if p in players:
                    players[p].send(json.dumps(response))
                        
            time.sleep(0.03)

        print("Game finished")

@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/agar")
def agar():
    global game
    global stop_game
    global players

    ws = request.environ.get("wsgi.websocket")
    myuid = ""

    if ws:
        while True:
            time.sleep(0.05)

            msg = ws.receive()
            if msg is None:
                break
            print(msg)
            msg = json.loads(msg)

            if msg["cmd"] == "join_room":
                info = msg["info"]
                if len(players) == 0:
                    game = AgarGame()
                    game_thread = GameThread(game_env=game)
                    game_thread.start()
                myuid = game.add_new_player(info["name"],info["skin"],np.array([0,0]))
                players[myuid] = ws
                food_info = game.food
                response = {"cmd":"init_info","info":{"food" : game.food, "border":[{"x":X_MIN,"y":Y_MIN},{"x":X_MAX,"y":Y_MAX}]}}
                ws.send(json.dumps(response))
            
            elif msg["cmd"] == "blob_move":
                info = msg["info"]
                pos = np.array([info["xpos"],info["ypos"]])
                game.update_player(myuid,pos,info["action"])

        if myuid in players:
            del players[myuid]
            game.delete_player(myuid)
        
        if len(players) == 0:
            stop_game = True
        
    return "finish game"

if __name__ == "__main__":
    start_ngrok(PORT)
    server = WSGIServer(("127.0.0.1",PORT),app,handler_class=WebSocketHandler)
    server.serve_forever()
