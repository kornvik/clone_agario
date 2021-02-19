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
    };
  },
  created() {
    console.log("Starting connection to WebSocket Server");
    this.connection = new WebSocket("wss://8209e93cf5d4.ngrok.io/ws/game/");
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
      this.draw(JSON.parse(event.data));
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
            ypos: this.mouse_y,
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
      this.fix_dpi();
      this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
      for (const blob in data.blobs) {
        // console.log(data.blobs[blob]);
        // console.log(this.screen_x + " " + this.screen_y);
        this.ctx.beginPath();
        // score += data.blobs[blob].score;
        // console.log(data.blobs[blob].xpos + this.screen_x);
        this.ctx.arc(
          this.screen_x + data.blobs[blob].xpos,
          this.screen_y + data.blobs[blob].ypos,
          data.blobs[blob].radius,
          0,
          Math.PI * 2,
          false
        );
        this.ctx.font = "15px Helvetica";
        this.ctx.textAlign = "center";
        this.ctx.textBaseLine = "middle";
        this.ctx.fillText(
          data.blobs[blob].name,
          this.screen_x + data.blobs[blob].xpos,
          this.screen_y + data.blobs[blob].ypos
        );
        this.ctx.fillStyle = data.blobs[blob].skin;
        this.ctx.fill();
        this.ctx.strokeStyle = data.blobs[blob].skin;
        this.ctx.stroke();
      }
      this.score = data.score;
      if (!data.alive) {
        this.end();
      }
    },
    fix_dpi() {
      let style = {
        height() {
          return +getComputedStyle(document.getElementById("canvas"))
            .getPropertyValue("height")
            .slice(0, -2);
        },
        width() {
          return +getComputedStyle(document.getElementById("canvas"))
            .getPropertyValue("width")
            .slice(0, -2);
        },
      };
      this.canvas.setAttribute("width", style.width() * this.dpi);
      this.canvas.setAttribute("height", style.height() * this.dpi);
    },
  },
};
</script>

<style scoped>
#canvas {
  position: absolute;
  top: 0;
  left: 0;
  height: 100vh;
  width: 100vh;
  background-image: url("../assets/grid.png");
  background-position: center;
  background-repeat: no-repeat;
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