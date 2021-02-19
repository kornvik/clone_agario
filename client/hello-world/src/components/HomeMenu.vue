<template>
  <div id="menupage" class="middle">
    <skin-window
      v-if="openDialog"
      :skin="skin"
      :colorList="colorList"
      @closeWindow="updateSkin"
    ></skin-window>
    <base-block class="middle">
      <button id="setting"></button>
      <h2>Corona.io</h2>
      <skin-choose @click="openWindow" :skin="inputSkin"></skin-choose>
      <input type="text" v-model="name" placeholder="Nick" />

      <button id="play" @click="play(name, inputSkin)">Play</button>
    </base-block>
  </div>
</template>

<script>
import SkinChoose from "./SkinChoose.vue";
import SkinWindow from "./SkinWindow.vue";
export default {
  components: {
    "skin-window": SkinWindow,
    "skin-choose": SkinChoose,
  },
  props: ["name", "skin"],
  data() {
    return {
      // name: "",
      // skin: "",
      openDialog: false,
      colorList: ["#f5da42", "#42c2f5", "#f54242", "#cef542", "#f59b42"],
      inputSkin: this.skin,
    };
  },
  inject: ["play"],
  methods: {
    updateSkin(skin) {
      this.inputSkin = skin;
      this.openDialog = false;
    },
    openWindow() {
      this.openDialog = true;
      //console.log("click");
    },
  },
};
</script>

<style scoped>
div .middle {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
}
div #menupage {
  padding: 10px;
  height: 100%;
  width: 100%;
  background-image: url("../assets/background.png");
  background-position: center;
  background-repeat: no-repeat;
  background-size: cover;
}
input {
  display: inline-block;
  width: 100%;
  margin: 2px;
  height: 20px;
  width: 100%;
  max-width: 10rem;
  margin: 2px 0px 2px 5px;
  box-sizing: border-box;
}
button {
  padding: 20px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  margin: 4px 6px;
  cursor: pointer;
}
span button {
  border-radius: 50%;
  border-style: dashed;
  display: inline-block;
  font-size: 10px;
  text-align: center;
  padding: 3px;
  width: 2rem;
  height: 2rem;
  color: grey;
}
#play {
  width: 90%;
  background-color: #20c420;
  color: white;
  max-width: 15rem;
  font-size: 16px;
  padding: 5px 20px;
  border: none;
}
#setting {
  position: absolute;
  display: block;
  border-radius: 100%;
  border: none;
  padding: 10px;
  background-image: url("../assets/button.jpg");
  background-repeat: no-repeat;
  background-size: 25px 25px;
  background-position: center;
}
h2 {
  display: block;
  margin: 20px auto 3px auto;
}
</style>
