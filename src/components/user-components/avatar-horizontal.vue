<template>
  <div class="player-holder">
    <div class="player-thumb" v-bind:style="{ 'background-image': 'url(' + image + ')' }"></div>
  </div>
</template>

<script>
  export default {
    name: 'avatar-horizontal',
    props: {
      image: '/static/img/icons/apple-touch-icon-76x76.png'
    }
  }
</script>

<style scoped>
  .player-holder {
    height: 350px;
    max-width: 650px;
    background: blue;
    text-align: center;
  }

  .player-thumb {
    width: 350px;
    height: 350px;
    display: inline-block;
    border-radius: 50%;
    background-image: url(http://www.whatcar.com/car-leasing/images/vehicles/medium/100895.jpg);
    background-size: cover;
    background-position: center;
  }
</style>
