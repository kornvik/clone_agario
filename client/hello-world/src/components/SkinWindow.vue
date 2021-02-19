<template>
  <div></div>
  <dialog open>
    <!-- <h2>Hello</h2> -->
    <header>
      <h2>Available Skins</h2>
    </header>
    <button @click="finish" id="close">x</button>
    <section>
      <circle-button
        v-for="color in colorList"
        @click="updateSkin(color)"
        :color="color"
        :key="color"
      >
      </circle-button>
    </section>
  </dialog>
</template>

<script>
export default {
  props: ["skin", "colorList"],
  emits: ["closeWindow"],
  methods: {
    finish() {
      this.$emit("closeWindow", this.inputSkin);
    },
    updateSkin(skin) {
      this.inputSkin = skin;
      this.finish();
    },
  },
  data() {
    return {
      inputSkin: this.skin,
    };
  },
};
</script>

<style scoped>
div {
  position: fixed;
  top: 0;
  left: 0;
  height: 100%;
  width: 100%;
  background-color: rgba(0, 0, 0, 0.75);
  z-index: 10;
}

dialog {
  position: fixed;
  top: 50%;
  left: 50%;
  width: 80%;
  z-index: 100;
  border-radius: 12px;
  border: none;
  /* box-shadow: 0 2px 8px rgba(0, 0, 0, 0.26); */
  padding: 0;
  margin: 0;
  overflow: hidden;
  /* transform: translate(-50%, -50%); */
  min-width: 25rem;
}

header {
  color: black;
  width: 100%;
  padding: 1rem 1rem 0 1rem;
  text-align: left;
  display: inline-block;
}

header h2 {
  margin: 0;
}

section {
  padding: 1rem;
  display: flex;
  justify-content: space-evenly;
}

/* menu {
  padding: 1rem;
  display: flex;
  justify-content: flex-end;
  margin: 0;
} */

@media (min-width: 768px) {
  dialog {
    left: calc(50% - 20rem);
    width: 40rem;
  }
}

#close {
  position: absolute;
  top: 5%;
  left: 95%;
  font-size: 20px;
  /* padding: 0.75rem 1.5rem; */
  font-family: inherit;
  color: black;
  background: white;
  cursor: pointer;
  border: none;
}
</style>