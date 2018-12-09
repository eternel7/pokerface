<template>
  <div id="message" v-bind:class="{ 'right': msg.origin===1, 'left': msg.origin!==1}">
    <img v-if="msg.origin===1" alt="me" v-bind:src="user.avatar_image"/>
    <img v-if="msg.origin!==1" alt="you" src="https://s3-us-west-2.amazonaws.com/s.cdpn.io/245657/1_copy.jpg"/>
    <div class="bubble">
      {{msg.text}}
      <div class="corner"></div>
      <span>{{ago}}</span>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'msg-item',
    props: ['msg', 'user', 'now'],
    computed: {
      ago: function () {
        if (!this.msg || !this.now) return ''
        let now = new Date(this.now)
        let secondsDiff = (now.getTime() - this.msg.date.getTime()) / 1000
        let minutes = Math.floor(secondsDiff / 60)
        let seconds = secondsDiff - minutes * 60
        let dateFormat = this.msg.date.toLocaleTimeString() + ' - '
        dateFormat += (minutes > 0) ? minutes.toFixed(0) + 'm' : ''
        dateFormat += seconds.toFixed(0) + 's ago'
        return dateFormat
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  #message {
    margin-top: 1vh;
    padding: 0 0 30px 58px;
    clear: both;
    margin-bottom: 45px;
    text-align: left;
    max-width: 75%;
  }

  #message.right {
    float: right;
    padding: 0 58px 30px 0;
    margin-right: -19px;
    margin-left: 19px;
  }

  #message img {
    float: left;
    margin-left: -38px;
    border-radius: 50%;
    width: 30px;
    margin-top: 12px;
  }

  #message.right img {
    float: right;
    margin-left: 0;
    margin-right: -38px;
  }

  #message .bubble {
    background: #f0f4f7;
    font-size: 13px;
    font-weight: 600;
    padding: 12px 13px;
    border-radius: 5px 5px 5px 0px;
    color: #8495a3;
    position: relative;
    float: left;
  }

  #message.right .bubble {
    float: right;
    border-radius: 5px 5px 0px 5px;
  }

  .bubble .corner {
    background: url("https://s3-us-west-2.amazonaws.com/s.cdpn.io/245657/bubble-corner.png") 0 0 no-repeat;
    position: absolute;
    width: 7px;
    height: 7px;
    left: -5px;
    bottom: 0;
  }

  #message.right .corner {
    background: url("https://s3-us-west-2.amazonaws.com/s.cdpn.io/245657/bubble-cornerR.png") 0 0 no-repeat;
    left: auto;
    right: -5px;
  }

  #message > .bubble span {
    color: #aab8c2;
    font-size: 11px;
    position: absolute;
    bottom: -2vh;
    width: max-content;
  }

  #message.left > .bubble span {
    left: 0;
  }

  #message.right > .bubble span {
    right: 0;
  }
</style>
