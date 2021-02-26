<template>
  <div class="block">
    <slot> </slot>
  </div>
</template>

<script>
export default {};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.block {
  margin: auto;
  max-width: 15rem;
  max-height: 14rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.26);
  padding: 0.5rem;
  background-color: rgb(252, 252, 252);
  box-sizing: border-box;
}
</style>
