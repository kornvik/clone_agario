import uuid
import json
import math
import numpy as np

# Dimension of the board
X_MIN = -1000
Y_MIN = -1000
X_MAX = 1000
Y_MAX = 1000

DIM = 500

V = 12
A = 3

MOUSE_FORCE = 10

NUM_MAX_FOOD = 100
PROB_FOOD = 0.3

MIN_SCORE_TO_DIVIDE = 100

# Skin available
SKIN_COLORS = ["#f5da42", "#42c2f5", "#f54242", "#cef542", "#f59b42"]
NUM_SKIN_COLORS = len(SKIN_COLORS)


"""
Blob class

Methods:
- update       : update blobs position
- follow       : change the stir so it aligns with the current mouse position
- pull         : make the blob be pull to a certain point
- stop_pulling : stop pulling
- start_pulling: start pulling
- get_radius   : get the radius of the blob based on the score
- get_drag     : calculate the drag index
- divide       : divide itself into 2 blobs (half its own score and return the other blob)     
- get_distance : get the distance from a blob
- is_colliding : return true if the this blob is colliding with the specified blob, otherwise return False
- apply_acc    : apply an acceleration to the blob
- repel        : apply a repulsive force to the blob (when colliding with another blob from the same parent)

Notes:
- So far here it is ok
"""

class Blob:
    def __init__(self,init_pos,buid,score=10,puid="",init_vel=np.array([0,0])):
        self.puid = puid 
        self.buid = buid
        self.pos  = init_pos
        self.vel  = init_vel
        self.score = score
        self.stir = np.array([0,0])        # unitary vector that stirs the blob (calculate from the mouse position)
        self.acc_attract = np.array([0,0])
        self.acc_repel = np.array([0,0])   # repel between blobs
        self.isPull = False

    def update(self):
        self.vel = (1-self.get_drag())*self.vel + MOUSE_FORCE*self.stir + self.acc_repel  #+ self.acc_attract 
        self.acc_repel = np.array([0,0])
        self.acc_attract = np.array([0,0])
        self.pos = self.pos + self.vel
        r = self.get_radius()
        if self.pos[0] < X_MIN + r:
            self.pos[0] = X_MIN + r
        elif self.pos[0] > X_MAX - r:
            self.pos[0] = X_MAX - r
        if self.pos[1] < Y_MIN + r:
            self.pos[1] = Y_MIN + r
        elif self.pos[1] > Y_MAX - r:
            self.pos[1] = Y_MAX - r
        
    def follow(self,mouse_pos):
        dr = mouse_pos - self.pos
        d = (dr.dot(dr))**0.5
        if d:
            dr = dr/d
        self.stir = dr
    
    def pull(self,cm):
        if self.isPull:
            dr = cm - self.pos
            d = dr.dot(dr) ** 0.5
            if d:
                dr = dr/d
            r = self.get_radius()
            if d < 1.1*r:
                dr = dr*1
            self.acc_attract = dr*A

    def stop_pulling(self):
        self.isPull = False

    def start_pulling(self):
        self.isPull = True
    
    def get_radius(self):
        return 10 + 8.5*math.log(self.score + 5)/math.log(10)

    def get_drag(self):
        return 0.8 + self.score/1000
    
    def divide(self):
        if self.score < MIN_SCORE_TO_DIVIDE:
            return None
        s = self.score
        s1 = s//2
        s2 = s - s1
        self.score = s2
        r = 5*self.get_radius()
        b = Blob(self.pos + r*self.stir,str(uuid.uuid4()),score=s1,puid=self.puid,init_vel=self.stir*50)
        return b

    def get_distance(self,b):
        d = self.pos - b.pos
        return (d.dot(d))**0.5

    def is_colliding(self,b):
        r1 = b.get_radius()
        r2 = self.get_radius()
        d = self.get_distance(b)
        return d<r1 or d<r2

    def apply_acc(self,acc):
        self.acc_repel = acc
    
    def repel(self,b):
        r1 = b.get_radius()
        r2 = self.get_radius()
        dr = self.pos - b.pos
        d = dr.dot(dr) ** 0.5
        if d:
            dr = dr/d
        h = 1.2*(r1 + r2) - d
        if h>0:
            self.apply_acc(dr*h*2)
            b.apply_acc(-dr*h*2)
        else:
            self.apply_acc(np.array([0,0]))
            b.apply_acc(np.array([0,0]))
"""
Food Class

Overriden method:
- get_radius  : food radius will always be 10 

"""
class Food(Blob):
    def __init__(self):
        pos = 3.9*DIM*(np.random.random(2) - 0.5)
        Blob.__init__(self,pos,str(uuid.uuid4()),score=10)
    def get_radius(self):
        return 10

"""
Player class

Methods:
- get_score        : calcule player's score adding all its blob's score
- add_blob         : add a new blob to the main blob's array
- get_com          : get center of mass of the player's blobs
- update_mouse_pos : update the mouse position of the player and also update the velocity direction of the blobs
- update_blobs     : update the blobs position

Notes:
So far it is ok, but I have some concerns about update_mouse_pos method (maybe some problems in syncronization with the clien) since we are calculate the center of mass as the reference.
"""

class Player:
    def __init__(self,uid,uname,skin,mouse_pos=np.array([0,0])):
        self.uid = uid
        self.uname = uname
        self.skin = skin
        self.alive = True
        self.mouse_pos = mouse_pos
        self.blobs = {}
        self.center_pos = mouse_pos
    
    def get_score(self):
        s = 0
        for b in self.blobs:
            s += self.blobs[b].score
        return s

    def add_blob(self,b):
        self.blobs[b.buid] = b

    def get_com(self):
        if len(self.blobs) == 0:
            return self.center_pos
        self.center_pos = np.array([0.0,0.0])
        for b in self.blobs:
            self.center_pos = self.center_pos + self.blobs[b].pos
        self.center_pos = self.center_pos / len(self.blobs)
        return self.center_pos
    
    def update_mouse_pos(self,rel_mouse_pos):
        self.get_com()
        self.mouse_pos = self.center_pos + rel_mouse_pos
        for b in self.blobs:
            self.blobs[b].follow(self.mouse_pos)
    
    def update_blobs(self):
        cm = self.get_com()
        for b in self.blobs:
            self.blobs[b].update()
            self.blobs[b].pull(cm)
        
    
"""
AgarGame class

Methods:
- add_new_player      : add new player to the game
- update_player       : update an specific player's mouse position 
- update              : update all player's blobs, check collisions and return the list of food ids that must be eliminated in the client side
- get_collisions      : get an array of the elements that were collisionated and neet to be delete
- delete_blob         : delete a blob from the game and return true if that blob was food 
- delete_player       : delete a player from the game
- get_leader_board    : get leader board (based on the score of all users)
- get_snapshot        : get a 'snapshot' of the game at the current time
- create_food         : create food if the number of good in the game hasnt reached the NUM_MAX_FOOD, this will be excecuted according to a probability (it was set to 0.1 for now)
"""

class AgarGame:
    def __init__(self):
        self.players = {}
        self.blobs = {}
        self.food = {}
        self.num_food = 0

    def add_new_player(self,uname,skin,pos):
        # Creating the player object
        puid = str(uuid.uuid4())
        self.players[puid] = Player(puid,uname,skin,mouse_pos=pos)

        # Creating player's blob
        buid = str(uuid.uuid4()) 
        b = Blob(pos,buid,puid=puid)
        self.blobs[buid] = b
        self.players[puid].add_blob(b)
        
        # Returning id of the player object
        return puid

    def update_player(self,puid,new_pos,action):
        # Update the direction to follow
        self.players[puid].update_mouse_pos(new_pos)

        # Divide if it is commanded
        if action:
            blobs = list(self.players[puid].blobs.keys())
            for i in blobs:
                b = self.players[puid].blobs[i].divide()
                if b is None:
                    continue
                self.blobs[b.buid] = b
                self.players[puid].add_blob(b)
                b.start_pulling()
                self.players[puid].blobs[i].start_pulling()
    
    def update(self):
        # Update players blobs positions
        for i in self.players:
            self.players[i].update_blobs()
        c = self.get_collisions()
        food_id = []
        for i in c:
            if self.delete_blob(i):
                food_id.append(i)
        return food_id
        
    def get_collisions(self):
        collisioned = []
        k = list(self.blobs.keys())
        n = len(k)
        for i in range(n):
            for j in range(i+1,n):
                u = self.blobs[k[i]]
                v = self.blobs[k[j]]
                if u.puid != v.puid:
                    if not u.is_colliding(v):
                        continue
                    if u.get_radius() < v.get_radius():
                        collisioned.append(k[i])
                        v.score += u.score
                    elif u.get_radius() > v.get_radius():
                        collisioned.append(k[j])
                        u.score += v.score
                else:
                    v.repel(u)
                        
        return collisioned

    def delete_blob(self,buid):
        if not buid in self.blobs:
            return False
        b = self.blobs[buid]
        is_food_id = False
        if b.puid != "":
            del self.players[b.puid].blobs[buid]
            if len(self.players[b.puid].blobs) == 0:
                self.players[b.puid].alive = False
        else:
            is_food_id = True
            del self.food[buid]
            self.num_food -= 1
        
        del self.blobs[buid]
        return is_food_id

    def delete_player(self,puid):
        del self.players[puid]
    
    def get_leader_board(self):
        o = []
        for i in self.players:
            if self.players[i].alive:
                o.append({"name":self.players[i].uname,"score":self.players[i].get_score()})    
        return sorted(o,key = lambda x : x["score"],reverse=True)

    def get_snapshot(self):
        info = {}
        for p in self.players:
            player = self.players[p]
            refx, refy = player.get_com()
            blobs = []
            uscore = 0
            for i in player.blobs:
                b = player.blobs[i]
                blobs.append({"xpos":1.0*b.pos[0],"ypos":1.0*b.pos[1],"radius":b.get_radius(),"skin":player.skin,"name":player.uname})
                uscore += b.score
            info[p] = {"xpos":refx,"ypos":refy,"blobs":blobs,"score":uscore,"alive":player.alive}
        return info

    def create_food(self,prob=True):
        if np.random.random() > PROB_FOOD and prob:
            return {}
        n = NUM_MAX_FOOD - self.num_food
        out = {}
        for i in range(n):
            b = Food()
            self.blobs[b.buid] = b
            self.food[b.buid] = {"xpos":b.pos[0],"ypos":b.pos[1],"skin":SKIN_COLORS[int(np.random.random()*NUM_SKIN_COLORS)]}
            out[b.buid] = self.food[b.buid]
        self.num_food = NUM_MAX_FOOD
        return out
