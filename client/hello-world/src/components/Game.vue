<template>
  <canvas id="canvas"></canvas>
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
  <button id="exit" @click="end">X</button>
</template>

<script>
export default {
  props: ["name", "skin"],
  emits: ["end"],
  data() {
    return {
      score: 10,
      leader: [
        {
          name: "John",
          score: 500000,
        },
        {
          name: "PP",
          score: 50000,
        },
        {
          name: "KK",
          score: 10000,
        },
        {
          name: "Hello",
          score: 1000,
        },
        {
          name: "Moo",
          score: 100,
        },
      ],
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
    };
  },
  created() {
    console.log("Starting connection to WebSocket Server");
    this.connection = new WebSocket("wss://6e7199a27e3d.ngrok.io/ws/game/");
    // this.connection = new WebSocket("wss://echo.websocket.org");
    this.connection.onmessage = (event) => {
      //   if (this.canvas) console.log(event);
      //   else {
      //     console.log("non");
      //   }
      //console.log(event.data);
      //   if (event.data) {

      //   } else {
      //     console.log("no idea");
      //   }

      var t0 = performance.now();
      if (this.timer != 0) {
        console.log(
          "Interval between on message " + (t0 - this.timer) + " milliseconds."
        );
      }
      var data = JSON.parse(event.data);
      if (data.cmd == "players") {
        this.draw(data.info);
      } else if (data.cmd == "food-add") {
        this.addFood(data.info);
        console.log("food-coming!");
        console.log(this.foods);
      } else if (data.cmd == "food-del") {
        this.delFood(data.info);
      } else {
        console.log("no cmd matching! " + data.cmd);
      }
      var t1 = performance.now();
      console.log("Call to draw took " + (t1 - t0) + " milliseconds.");
      this.timer = t0;
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
      window.onmousemove = (e) => {
        this.mouse_x = e.pageX - this.screen_x;
        this.mouse_y = e.pageY - this.screen_y;
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
        this.sendUser(mouse);
        if (this.action) {
          this.action = false;
        }
        // console.log(user);
      }, 150);
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
    sendUser(message) {
      //   console.log(JSON.stringify(message));
      this.connection.send(JSON.stringify(message));
    },
    end() {
      clearInterval(this.interval);
      this.interval = null;
      this.score = 10;
      this.connection.close();
      this.connection = null;
      this.$emit("end");
    },
    draw(data) {
      //   const obj = JSON.parse(data);
      //   this.ctx.globalCompositeOpertion = "source-in";
      // this.fix_dpi();
      this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
      var me = data.me;
      if (!me.alive) {
        this.end();
      }
      this.foods.forEach((value) => {
        // console.log("plotting food" + value);
        this.plotBlob(
          this.screen_x + value.xpos - me.ave_xpos,
          this.screen_y + value.ypos - me.ave_ypos,
          value.skin
        );
      });

      this.score = me.score;
      for (const blob in me.blobs) {
        this.plotBlob(
          this.screen_x + me.blobs[blob].xpos - me.ave_xpos,
          this.screen_y + me.blobs[blob].ypos - me.ave_ypos,
          this.skin,
          me.blobs[blob].radius,
          this.name
        );
        // console.log(me.blobs[blob].ypos + " " + me.ave_ypos);
      }

      for (const blob in data.blobs) {
        // console.log(data.blobs[blob]);
        // console.log(this.screen_x + " " + this.screen_y);
        this.plotBlob(
          this.screen_x + data.blobs[blob].xpos - me.ave_xpos,
          this.screen_y + data.blobs[blob].ypos - me.ave_ypos,
          data.blobs[blob].skin,
          data.blobs[blob].radius,
          data.blobs[blob].name
        );
      }
    },
    addFood(data) {
      // console.log("food" + data.foods);
      data.foods.forEach((obj) => {
        // console.log("food " + obj);
        this.foods.set(obj.id, {
          xpos: obj.xpos,
          ypos: obj.ypos,
          skin: obj.skin,
        });
      });
    },
    delFood(data) {
      data.foodsId.forEach((id) => {
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
  background-image: url("../assets/grid.png");
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
</style>