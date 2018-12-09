<template>
  <div>
    <div id="fab" class="mdl-color--accent mdl-color-text--white">
      <img id="icon" src="/static/img/chat-icon_white.png" width="45"/>
    </div>
    <div v-if="userTitle" class="mdl-card__title">
      <h2 class="card__title mdl-card__title-text">
        {{$t(userTitle)}}
      </h2>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'cardfabtitle',
    props: {
      'userTitle': {
        default: 'user.Login',
        type: String
      }
    }
  }
</script>

<style scoped>
  .card__title {
    text-align: center;
    font-weight: 600;
    font-size: 32px;
    line-height: 40px;
    margin: auto;
  }

  #fab {
    border-radius: 50%;
    height: 56px;
    margin: auto;
    min-width: 56px;
    width: 56px;
    overflow: hidden;
    background: rgba(158, 158, 158, .2);
    box-shadow: 0 1px 1.5px 0 rgba(0, 0, 0, .12), 0 1px 1px 0 rgba(0, 0, 0, .24);
    position: absolute;
    top: -30px;
    text-align: center;
    left: 0;
    right: 0;
  }

  #icon {
    margin-top: 5px;
  }
</style>
