<template>
  <HomeMenu v-if="gameNotStart" :name="user.name" :skin="user.skin"></HomeMenu>
  <Game v-else v-bind="user" @end="goMenu"></Game>
</template>

<script>
import HomeMenu from "./components/HomeMenu.vue";
import Game from "./components/Game.vue";
export default {
  data() {
    return {
      user: { name: "", skin: "" },
      gameNotStart: true,
    };
  },
  components: {
    HomeMenu,
    Game,
  },
  methods: {
    play(name, skin) {
      this.user.name = name;
      this.user.skin = skin;
      // const user = {
      //   name: name,
      //   skin: skin,
      // };
      //console.log(user);
      this.gameNotStart = false;
    },
    goMenu() {
      this.gameNotStart = true;
    },
  },
  provide() {
    return {
      play: this.play,
    };
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
body {
  margin: 0;
}
</style>
