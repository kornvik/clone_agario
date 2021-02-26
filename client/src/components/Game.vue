<template>
  <canvas id="canvas"></canvas>
  <die-window v-if="die" :score="max_score" @closeWindow="replay"></die-window>
  <base-block id="leaderboard">
    <h3>Leaderboard</h3>
    <ol>
      <li v-for="user in leader" :key="user.name">
        <span class="left">{{ user.name }}</span>
        <span class="right">{{ user.score }}</span>
      </li>
      <!-- <p>
        <span class="left">{{ name }}</span>
        <span class="right">{{ score }}</span>
      </p> -->
    </ol>
  </base-block>
  <base-block id="score"> Score : {{ score }}</base-block>
  <button id="exit" @click="ends">X</button>
</template>

<script>
import DieWindow from "./DieWindow.vue";
export default {
  components: {
    "die-window": DieWindow,
  },
  props: ["name", "skin"],
  emits: ["end"],
  data() {
    return {
      score: 10,
      leader: [],
      connection: null,
      interval: null,
      mouse_x: 0,
      mouse_y: 0,
      action: false,
      id: null,
      canvas: null,
      ctx: null,
      dpi: null,
      screen_x: 0,
      screen_y: 0,
      alive: true,
      timer: 0,
      foods: new Map(),
      theta: 0,
      prev_x: -999,
      prev_y: -999,
      step: 3,
      step_size: 2,
      step_interval: 10,
      px: 0,
      py: 0,
      die: false,
      max_score: 10,
      border : [
        {
          x : -1000,
          y : -1000,
        },
        {
          x : 1000,
          y : 1000,
        }
      ]
    };
  },
  created() {
    //8296db7f0724.ngrok.io/agar
    console.log("Starting connection to WebSocket Server");
      this.connection = new WebSocket("wss://b1ed91c80ddc.ngrok.io/agar");
      // this.connection = new WebSocket("wss://echo.websocket.org");
      this.connection.onmessage = (event) => {
        var data = JSON.parse(event.data);
        this.perForm(data);
      };
      this.connection.onopen = (event) => {
        //console.log(event);
        console.log("Successfully connected to the echo websocket server...");
        //this.connection.send(this.user);

        const user = {
          cmd: "join_room",
          info: {
            name: this.name,
            skin: this.skin,
            room: "test",
          },
        };
        this.sendUser(user);

      // console.log("send log-in data");
      window.onmousemove = (e) => {
        this.mouse_x = e.pageX - this.screen_x;
        this.mouse_y = e.pageY - this.screen_y;
        this.theta = Math.atan2(this.mouse_y, this.mouse_x);
      };
      window.onresize = (e) => {
        this.screen_x = Math.floor(window.innerWidth / 2);
        this.screen_y = Math.floor(window.innerHeight / 2);
        console.log(this.screen_x * 2);
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
      };
      window.onresize();
      window.onkeydown = (e) => {
        if (e.keyCode == 32) {
          this.action = true;
        }
      };
      this.interval = setInterval(() => {
        // console.log("(" + this.mouse_x + "," + this.mouse_y + ")");
        const mouse = {
          cmd: "blob_move",
          info: {
            xpos: this.mouse_x,
            ypos: -this.mouse_y,
            action: this.action,
          },
        };
        // console.log(mouse.info);
        this.sendUser(mouse);
        if (this.action) {
          this.action = false;
        }
        // console.log(user);
      }, 150);
    };
    this.connection.onclose = (event) => {
        console.log("closing");
    };
  },
  mounted() {
    this.canvas = document.getElementById("canvas");
    // this.canvas.width = window.innerWidth;
    // this.canvas.height = window.innerHeight;
    this.ctx = this.canvas.getContext("2d");
    this.dpi = window.devicePixelRatio;
  },
  methods: {
    startGame(){
      console.log("Starting connection to WebSocket Server");
      this.connection = new WebSocket("wss://b1ed91c80ddc.ngrok.io/agar");
      // this.connection = new WebSocket("wss://echo.websocket.org");
      this.connection.onmessage = (event) => {
        var data = JSON.parse(event.data);
        this.perForm(data);
      };
      this.connection.onopen = (event) => {
        //console.log(event);
        console.log("Successfully connected to the echo websocket server...");
        //this.connection.send(this.user);

        const user = {
          cmd: "join_room",
          info: {
            name: this.name,
            skin: this.skin,
            room: "test",
          },
        };
        this.sendUser(user);
        // console.log("send log-in data");
        window.onmousemove = (e) => {
          this.mouse_x = e.pageX - this.screen_x;
          this.mouse_y = e.pageY - this.screen_y;
          this.theta = Math.atan2(this.mouse_y, this.mouse_x);
        };
        window.onresize = (e) => {
          this.screen_x = Math.floor(window.innerWidth / 2);
          this.screen_y = Math.floor(window.innerHeight / 2);
          console.log(this.screen_x * 2);
          this.canvas.width = window.innerWidth;
          this.canvas.height = window.innerHeight;
        };
        window.onresize();
        window.onkeydown = (e) => {
          if (e.keyCode == 32) {
            this.action = true;
          }
        };
        this.interval = setInterval(() => {
          // console.log("(" + this.mouse_x + "," + this.mouse_y + ")");
          const mouse = {
            cmd: "blob_move",
            info: {
              xpos: this.mouse_x,
              ypos: -this.mouse_y,
              action: this.action,
            },
          };
          // console.log(mouse.info);
          this.sendUser(mouse);
          if (this.action) {
            this.action = false;
          }
          // console.log(user);
        }, 150);
      };
      this.connection.onclose = (event) => {
          console.log("closing");
      };
    },
    perForm(data){
        var t0 = performance.now();
        if (this.timer != 0) {
          // console.log(
          //   "Interval between on message " + (t0 - this.timer) + " milliseconds."
          // );
        }
        
        if (data.cmd == "players") {
          if (this.prev_y != -999) {
            this.px = (data.info.me.xpos - this.prev_x) / this.step;
            this.py = (data.info.me.ypos - this.prev_y) / this.step;
          }
          // this.prev_x = data.info.me.xpos;
          // this.prev_y = data.info.me.ypos;
          this.updateBoard(data.info.leader_board);
          this.addFood(data.info.food_add);
          this.delFood(data.info.food_del);
          this.draw(data.info, 0);
          this.updateHighScore(this.score);
        } else if (data.cmd == "init_info") {
          this.addFood(data.info.food);
          this.updateBorder(data.info.border);
          console.log("food-coming!");
          console.log(this.foods);
        } else {
          console.log("no cmd matching! " + data.cmd);
        }
        var t1 = performance.now();
        // console.log("Call to draw took " + (t1 - t0) + " milliseconds.");
        this.timer = t0;
    },
    sendUser(message) {
      //   console.log(JSON.stringify(message));
      this.connection.send(JSON.stringify(message));
    },
    ends() {
      clearInterval(this.interval);
      this.interval = null;
      this.score = 10;
      if (this.connection != null) {
        this.connection.close();
        this.connection = null;
      }
      this.$emit("end");
    },
    replay(playAgain) {
      this.die=false;
      if (playAgain) {
        clearInterval(this.interval);
        this.interval = null;
        this.score = 10;
        this.max_score = 10;
        this.foods.clear();
        this.alive = true;
        if (this.connection != null) {
          this.connection.close();
          this.connection = null;
        }
        this.startGame();
      } else {
        this.ends();
      }
    },
    updateBoard(data) {
      for (var i = 0, len = data.length; i < 5; i++) {
        if (i < len) {
          this.leader.splice(i,1,data[i]);
        } else {
          this.leader.splice(i,4-i+1);
          break;
        }
      }
      // this.leader_board = data;
    },
    draw(data, num) {
      //   const obj = JSON.parse(data);
      //   this.ctx.globalCompositeOpertion = "source-in";
      // this.fix_dpi();
      // console.log(data.blobs)
      this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
      // var me = data.me;
      if (!data.me.alive && this.die==false) {
        clearInterval(this.interval);
        this.interval = null;
        this.die = true;
        // this.end();
      }
      this.foods.forEach((value) => {
        // console.log("plotting food" + value);
        this.plotBlob(
          this.screen_x + value.xpos - data.me.xpos,
          this.screen_y - (value.ypos - data.me.ypos),
          value.skin
        );
      });
      // console.log("----------me-----------");
      // console.log(data.me.blobs);
      this.score = data.me.score;
      for (const blob in data.me.blobs) {
        this.plotBlob(
          this.screen_x + data.me.blobs[blob].xpos - data.me.xpos,
          this.screen_y - (data.me.blobs[blob].ypos - data.me.ypos),
          this.skin,
          data.me.blobs[blob].radius,
          this.name
        );
        // console.log(me.blobs[blob].ypos + " " + me.ave_ypos);
      }
      // console.log("xpos : " + data.me.xpos);
      // console.log("ypos : " + data.me.ypos);
      // console.log("screen " + this.screen_x + " " + this.screen_y);
      this.plotWall(data.me.xpos,data.me.ypos);

      for (const blob in data.blobs) {
        // console.log(dat a.blobs[blob]);
        // console.log(this.screen_x + " " + this.screen_y);
        this.plotBlob(
          this.screen_x + data.blobs[blob].xpos - data.me.xpos,
          this.screen_y - (data.blobs[blob].ypos - data.me.ypos),
          data.blobs[blob].skin,
          data.blobs[blob].radius,
          data.blobs[blob].name
        );
      }

      // console.log("drawing")
      if (num < this.step && data.me.alive) {
        const theta = Math.atan2(-this.mouse_y, this.mouse_x);
        const px = this.step_size * Math.cos(theta);
        const py = this.step_size * Math.sin(theta);
        // const px = step * Math.cos(theta);
        // const py = step * Math.sin(theta);

        var ave_xpos = 0;
        var ave_ypos = 0;
        var num_me = 0;
        for (const blob in data.me.blobs) {
          data.me.blobs[blob].xpos += px;
          data.me.blobs[blob].ypos += py;
          ave_xpos += data.me.blobs[blob].xpos;
          ave_ypos += data.me.blobs[blob].ypos;
          num_me += 1;
          // console.log(me.blobs[blob].ypos + " " + me.ave_ypos);
        }
        data.me.xpos = ave_xpos / num_me;
        data.me.ypos = ave_ypos / num_me;
        setTimeout(this.draw(data, num + 1), this.step_interval);
      }
    },
    addFood(data) {
      // console.log("food" + data);
      for (var key in data) {
        // console.log("food " + obj);
        this.foods.set(key, {
          xpos: data[key].xpos,
          ypos: data[key].ypos,
          skin: data[key].skin,
        });
      }
    },
    delFood(data) {
      data.forEach((id) => {
        this.foods.delete(id);
      });
    },
    plotBlob(x, y, skin, radius = "5", name = "") {
      // console.log("plotting blob" + x + " " + y);
      this.ctx.beginPath();
      // score += data.blobs[blob].score;
      // console.log(data.blobs[blob].xpos + "," + data.blobs[blob].ypos);
      this.ctx.arc(x, y, radius, 0, Math.PI * 2, false);
      this.ctx.font = "16px Helvetica";
      this.ctx.textAlign = "center";
      this.ctx.textBaseLine = "middle";
      this.ctx.fillStyle = skin;
      // this.ctx.strokeStyle = skin;
      // this.ctx.stroke();
      this.ctx.fill();
      this.ctx.beginPath();
      this.ctx.fillStyle = "#ffffff";
      this.ctx.fillText(name, x, y + 3);
      this.ctx.fill();
    },
    plotWall(x, y) {
      // console.log("blob" + x + " " + y);
      // console.log("plot wall above " + y+this.screen_y + parseFloat(this.border[1].y));
      // console.log(parseFloat(this.border[1].y));

      if(y+this.screen_y>this.border[1].y){
        // console.log("-------------------------");
        this.ctx.beginPath();
        this.ctx.rect(0,0,window.innerWidth,y+this.screen_y-this.border[1].y)
        this.ctx.fillStyle = "#ffffff";
        this.ctx.fill();
      }
      if(x+this.screen_x>this.border[1].x){
        this.ctx.beginPath();
        this.ctx.rect(window.innerWidth-(x+this.screen_x-this.border[1].x),0,window.innerWidth,window.innerHeight);
        this.ctx.fillStyle = "#ffffff";
        this.ctx.fill();
      }
      if(x-this.screen_x<this.border[0].x){
        this.ctx.beginPath();
        this.ctx.rect(0,0,this.border[0].x-(x-this.screen_x),window.innerHeight)
        this.ctx.fillStyle = "#ffffff";
        this.ctx.fill();
      }
      if(y-this.screen_y<this.border[0].y){
        this.ctx.beginPath();
        this.ctx.rect(0,window.innerHeight-(this.border[0].y-(y-this.screen_y)),window.innerWidth,window.innerHeight)
        this.ctx.fillStyle = "#ffffff";
        this.ctx.fill();
      }
    },
    updateHighScore(score) {
      if(score > this.max_score) this.max_score = score;
    },
    updateBorder(data){
      console.log(data)
      for(var i=0, len = data.length;i<len;i++){
        this.border.splice(i,1,data[i]);
      }
    }
  },
  // beforeDestroy() {
  //   this.end();
  // },
};
</script>

<style scoped>
#canvas {
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  width: 100%;
  background-color: rgb(72, 72, 80);
  /* background-image: url("../assets/grid.png"); */
  background-position: center;
  background-repeat: repeat-x;
  background-size: cover;
  z-index: -1;
}
#leaderboard {
  position: absolute;
  top: 3%;
  right: 3%;
  background-color: white;
  /* box-sizing: border-box; */
  margin: 0 0 auto auto;
  opacity: 0.6;
  padding: 1rem;
  min-height: 3rem;
  min-width: 15rem;
}
#score {
  position: absolute;
  bottom: 3%;
  left: 3%;
  background-color: white;
  /* box-sizing: border-box; */
  margin: auto auto 0 0;
  opacity: 0.6;
  max-height: 2rem;
  max-width: 7rem;
}
ol {
  padding-left: 2rem;
}
li,
p {
  text-align: left;
  font: inherit;
  font-style: bold;
  font-size: 20px;
}
p {
  padding: 0;
  margin: 0;
}
.left {
  float: left;
}
.right {
  float: right;
}
.left,
.right {
  display: inline-block;
  /* width: 50%; */
}
button {
  min-width: 5rem;
  min-height: 3rem;
  cursor: pointer;
  z-index: 10;
}
#exit {
  position: absolute;
  top: 2%;
  left: 2%;
  background-color: white;
  opacity: 0.6;
  color: grey;
  /* box-sizing: border-box; */
  min-width: 2rem;
  min-height: 2rem;
  padding: 4px;
}
.top {
  z-index: 100;
}
</style>