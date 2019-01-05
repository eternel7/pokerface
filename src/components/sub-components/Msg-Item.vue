<template>
  <div id="message" v-bind:class="{ 'right': msg.origin===1, 'left': msg.origin!==1}">
    <img v-if="msg.origin===1" alt="Me" v-bind:src="user.avatar_image"/>
    <img v-if="msg.origin.portrait" v-bind:alt="msg.origin.username" v-bind:src="msg.origin.portrait"/>
    <div class="img" v-if="msg.origin===0" alt="Bot"
         v-bind:style="'background-image: url(' + chatroom.portrait + ')'"></div>
    <div class="bubble">
      {{msg.message}}
    </div>
    <div v-if="!msg.origin.portrait" class="time">{{msg.date.toLocaleTimeString()}}</div>
    <div v-else class="time">{{msg.date.toLocaleTimeString() + ' - ' + msg.origin.username}}</div>
  </div>
</template>

<script>
  export default {
    name: 'msg-item',
    props: ['msg', 'user', 'chatroom', 'now']
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  #message {
    padding: 0 0 5px 58px;
    clear: both;
    margin-bottom: 0.5vh;
    text-align: left;
    max-width: 60%;
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

  #message div.img {
    bottom: 1vh;
    float: left;
    margin-left: -38px;
    border-radius: 50%;
    width: 30px;
    height: 30px;
    margin-top: 12px;
  }

  #message.right div.img {
    float: right;
    margin-left: 0;
    margin-right: -38px;
  }

  #message .bubble {
    background: #dbe3f9;
    font-size: 13px;
    font-weight: 600;
    padding: 12px 13px;
    border-radius: 5px 5px 5px 0px;
    color: #365dad;
    position: relative;
    float: left;
    width: max-content;
    max-width: 100%; /* do not oversize message width*/
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
    color: #8eace8;
    font-size: 0.8em;
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
