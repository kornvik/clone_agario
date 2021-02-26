<template>
  <span
    ><button
      :style="[
        skin
          ? { backgroundColor: skin, 'border-style': 'none', color: 'white' }
          : { 'border-style': 'dashed' },
      ]"
    >
      Skin
    </button></span
  >
</template>

<script>
export default {
  props: ["skin"],
  date() {
    return {};
  },
};
</script>

<style scoped>
button {
  padding: 20px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  margin: 4px 6px;
  cursor: pointer;
  border-radius: 50%;
  /* border-style: dashed; */
  display: inline-block;
  font-size: 10px;
  text-align: center;
  padding: 3px;
  min-width: 2rem;
  min-height: 2rem;
}
</style>
