<template>
  <span
    ><button :style="{ backgroundColor: color }"><slot></slot></button
  ></span>
</template>

<script>
export default {
  props: ["color"],
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
  font-size: 10px;
  min-width: 4rem;
  min-height: 4rem;
  border: none;
  color: white;
}
</style>
