<template>
  <div id="message" v-bind:class="{ 'right': msg.origin===1, 'left': msg.origin!==1}">
    <img v-if="msg.origin===1" alt="me" v-bind:src="user.avatar_image"/>
    <img v-if="msg.origin!==1" alt="you" src="https://s3-us-west-2.amazonaws.com/s.cdpn.io/245657/1_copy.jpg"/>
    <div class="bubble">
      {{msg.text}}
    </div>
    <div class="time">{{ago}}</div>
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
    padding: 0 0 5px 58px;
    clear: both;
    margin-bottom: 0.5vh;
    text-align: left;
    max-width: 75%;
  }

  #message.right {
    float: right;
    padding: 0 58px 5px 0;
    margin-right: -19px;
    margin-left: 19px;
  }

  #message img {
    bottom: 1vh;
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
    width: max-content;
    background: #dbe3f9;
    font-size: 13px;
    font-weight: 600;
    padding: 12px 13px;
    border-radius: 5px 5px 5px 0px;
    color: #2e3c58;
    position: relative;
    float: left;
  }

  #message .bubble:after {
    content: '';
    position: absolute;
    top: 100%;
    width: 0;
    height: 0;
    border: 7px solid transparent;
    border-bottom: 0;
    margin-top: -7px;

  }

  #message.left .bubble:after {
    left: 0;
    border-right-color: #dbe3f9;
    border-left: 0;
    margin-left: -7px;
  }

  #message.right .bubble {
    float: right;
    border-radius: 5px 5px 0px 5px;
  }

  #message.right .bubble:after {
    right: 0;
    border-left-color: #dbe3f9;
    border-right: 0;
    margin-right: -7px;
  }

  #message > .time {
    clear: both;
    color: #aab8c2;
    font-size: 12px;
    position: relative;
    bottom: -0.5vh;
    width: max-content;
  }

  #message.left > .time {
    left: 0;
  }

  #message.right > .time {
    right: 0;
  }
</style>
