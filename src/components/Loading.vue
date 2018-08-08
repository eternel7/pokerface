<template>
  <div v-if="visible" id="full_page_overlay">
    <div id="loading_in_progress" class="mdl-color--accent"></div>
  </div>
</template>

<script>
  export default {
    name: 'Loading',
    computed: {
      visible: function () {
        return !!this.$root.loading
      }
    }
  }
</script>

<style scoped>
  #loading_in_progress {
    position: absolute;
    left: 50%;
    top: 50%;
    margin: -20px 0 0 -20px;
    height: 40px;
    width: 40px;
    border-radius: 50%;
    opacity: 1;

    animation: pulsate 1s ease-out;
    animation-iteration-count: infinite;
  }

  @keyframes pulsate {
    0% {
      transform: perspective(120px) rotateX(0deg) rotateY(0deg);
    }
    50% {
      transform: perspective(120px) rotateX(-180deg) rotateY(0deg);
    }
    100% {
      transform: perspective(120px) rotateX(-180deg) rotateY(-180deg);
    }
  }

  #full_page_overlay {
    background: rgba(0,0,0, 0.5);
    position: absolute;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    z-index: 9999;
  }
</style>
