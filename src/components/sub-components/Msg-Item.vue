<template>
  <div id="message" v-bind:class="{ 'right': msg.origin===1, 'left': msg.origin!==1}">
    <div class="img-and-bubble">
      <img v-if="msg.origin===1" alt="Me" v-bind:src="user.avatar_image"/>
      <img v-else-if="msg.origin===0" alt="Me" v-bind:src="chatroom.portrait"/>
      <img v-else-if="msg.origin.portrait" v-bind:alt="msg.origin.username" v-bind:src="msg.origin.portrait"/>
      <div class="bubble">
        {{msg.message}}
      </div>
      <div v-if="msg.origin===1" class="link mdl-badge mdl-badge--overlap"
           v-bind:class="{ 'is-it-a-question': !msg.question}"
           v-bind:data-badge="(msg.question) ? msg.post_id : '?' " @click="$emit('changeQuestion')">
      </div>
    </div>
    <div v-if="!msg.origin.portrait" class="time">
      {{msg.date.toLocaleTimeString()}}
    </div>
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
  .is-it-a-question:after {
    color: #ffffff;
    background-color: #4CAF50;
  }

  #message {
    display: flex;
    flex-direction: column;
    padding: 0 0 5px 58px;
    clear: both;
    text-align: left;
    max-width: 60%;
  }

  #message.right {
    float: right;
    padding: 0 58px 5px 0;
    margin-right: -19px;
    margin-left: 19px;
  }

  #message div.img-and-bubble {
    position: relative;
  }

  #message img {
    position: absolute;
    bottom: 0;
    left: -38px;
    border-radius: 50%;
    width: 30px;
    margin-top: 12px;
  }

  #message.right img {
    right: -38px;
    left: auto;
  }

  #message .bubble {
    position: relative;
    float: left;
    background: #dbe3f9;
    font-size: 13px;
    font-weight: 600;
    padding: 12px 13px;
    border-radius: 5px 5px 5px 0px;
    color: #365dad;
    width: max-content;
    max-width: 100%; /* do not oversize message width*/
  }

  #message.right .bubble {
    float: right;
    border-radius: 5px 5px 0px 5px;
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
    bottom: 0;
    margin-bottom: 0.5em;
    width: max-content;
  }

  #message.left > .time {
    margin-left: 0;
    margin-right: auto;
  }

  #message.right > .time {
    margin-left: auto;
    margin-right: 0;
  }
</style>
