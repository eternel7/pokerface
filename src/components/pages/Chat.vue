<template>
  <div v-if="chatroom" id="chatview">
    <div id="profile">
      <div id="close" v-on:click="backHome">
        <i class="material-icons">close</i>
      </div>
      <div id="user">{{chatroom.user_label}}</div>
    </div>
    <div id="chat-messages" ref="chatmessages">
      <div class="message">
        <img src="https://s3-us-west-2.amazonaws.com/s.cdpn.io/245657/1_copy.jpg"/>
        <div class="bubble">
          Really cool stuff!
          <div class="corner"></div>
          <span>3 min</span>
        </div>
      </div>
      <div class="message right">
        <img v-bind:src="user.avatar_image"/>
        <div class="bubble">
          Can you share a link for the tutorial?
          <div class="corner"></div>
          <span>1 min</span>
        </div>
      </div>

      <div class="message">
        <img src="https://s3-us-west-2.amazonaws.com/s.cdpn.io/245657/1_copy.jpg"/>
        <div class="bubble">
          Yeah, hold on
          <div class="corner"></div>
          <span>Now</span>
        </div>
      </div>

      <div class="message right">
        <img v-bind:src="user.avatar_image"/>
        <div class="bubble">
          Can you share a link for the tutorial?
          <div class="corner"></div>
          <span>1 min</span>
        </div>
      </div>

      <div class="message">
        <img src="https://s3-us-west-2.amazonaws.com/s.cdpn.io/245657/1_copy.jpg"/>
        <div class="bubble">
          Yeah, hold on
          <div class="corner"></div>
          <span>Now</span>
        </div>
      </div>
      <div class="message">
        <img src="https://s3-us-west-2.amazonaws.com/s.cdpn.io/245657/1_copy.jpg"/>
        <div class="bubble">
          Really cool stuff!
          <div class="corner"></div>
          <span>3 min</span>
        </div>
      </div>
      <div class="message right">
        <img v-bind:src="user.avatar_image"/>
        <div class="bubble">
          Can you share a link for the tutorial?
          <div class="corner"></div>
          <span>1 min</span>
        </div>
      </div>

      <div class="message">
        <img src="https://s3-us-west-2.amazonaws.com/s.cdpn.io/245657/1_copy.jpg"/>
        <div class="bubble">
          Yeah, hold on
          <div class="corner"></div>
          <span>Now</span>
        </div>
      </div>

      <div class="message right">
        <img v-bind:src="user.avatar_image"/>
        <div class="bubble">
          Can you share a link for the tutorial?
          <div class="corner"></div>
          <span>1 min</span>
        </div>
      </div>

      <div class="message">
        <img src="https://s3-us-west-2.amazonaws.com/s.cdpn.io/245657/1_copy.jpg"/>
        <div class="bubble">
          Yeah, hold on
          <div class="corner"></div>
          <span>Now</span>
        </div>
      </div>

    </div>

    <div id="sendmessage">
      <input type="text" placeholder="Send message..."/>
      <div id="send">
        <button class="mdl-button mdl-js-button mdl-button--fab mdl-js-ripple-effect mdl-button--colored">
          <i class="material-icons">send</i>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
  import PageBase from '@/components/pages/Page'

  export default {
    name: 'chat',
    extends: PageBase,
    data () {
      return {
        displaySearch: true,
        displayBack: true,
        displayHeader: false
      }
    },
    computed: {
      chatroom: function () {
        return this.$root.chatrooms[this.$route.params.id]
      },
      user: function () {
        return this.$root.user
      }
    },
    created () {
      if (!this.chatroom || this.chatroom.length < 1) {
        this.$router.push({name: 'Home'})
      } else {
        let vm = this
        vm.$nextTick(function () {
          let messages = vm.$refs['chatmessages']
          if (messages) {
            messages.scrollTop = messages.scrollHeight
          }
        })
      }
    },
    methods: {
      backHome: function () {
        this.$router.push({name: 'Home'})
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->


<style scoped>
  #chatview {
    position: fixed;
    top: 0;
    bottom: 0;
    left: 50%;
    -webkit-transform: translateX(-50%); /* Chrome 4+, Op 15+, Saf 3.1, iOS Saf 3.2+ */
    -moz-transform: translateX(-50%); /* Fx 3.5-15 */
    -ms-transform: translateX(-50%); /* IE 9 */
    -o-transform: translateX(-50%); /* Op 10.5-12 */
    transform: translateX(-50%); /* Fx 16+, IE 10+ */
    margin-left: auto;
    margin-right: auto;
    background: #fff;
    height: 100%;
    width: 100%;
    max-width: 700px;
  }

  #profile {
    position: relative;
    padding: 0;
    margin: 0;
    height: 25vh;
    overflow: hidden;
    text-align: center;
    background-color: #e4e4e4;
    background-image: url('https://s3-us-west-2.amazonaws.com/s.cdpn.io/245657/1_copy.jpg');
    background-size: cover;
    background-repeat: no-repeat;
    color: #fff;
  }

  #user {
    position: absolute;
    bottom: 0;
    padding: 0;
    margin: 0;
    vertical-align: middle;
    width: 100%;
    height: 6vh;
    min-height: 6vh;
    line-height: 6vh;
    background-color: rgba(88, 88, 88, 0.34);
    font-weight: 600;
    font-size: 3vh;
  }

  #close {
    position: absolute;
    top: 8px;
    right: 10px;
    width: 20px;
    height: 20px;
    cursor: pointer;
  }

  #close:hover > i {
    opacity: 1;
  }

  #close>i:hover {
    opacity: 1;
  }

  #close>i {
    opacity: 0.8;
    -webkit-animation: myrotate 3s forwards; /* Safari 4.0 - 8.0 */
    animation: myrotate 3s forwards;
  }

  /* Safari 4.0 - 8.0 */
  @-webkit-keyframes myrotate {
    from {
      -webkit-transform: rotate(0deg) scale(0); /* Chrome 4+, Op 15+, Saf 3.1, iOS Saf 3.2+ */
      -moz-transform: rotate(0deg) scale(0); /* Fx 3.5-15 */
      -ms-transform: rotate(0deg) scale(0); /* IE 9 */
      -o-transform: rotate(0deg) scale(0); /* Op 10.5-12 */
      transform: rotate(0deg) scale(0); /* Fx 16+, IE 10+ */
      opacity: 0;
    }
    to {
      -webkit-transform: rotate(360deg) scale(1); /* Chrome 4+, Op 15+, Saf 3.1, iOS Saf 3.2+ */
      -moz-transform: rotate(360deg) scale(1); /* Fx 3.5-15 */
      -ms-transform: rotate(360deg) scale(1); /* IE 9 */
      -o-transform: rotate(360deg) scale(1); /* Op 10.5-12 */
      transform: rotate(360deg) scale(1); /* Fx 16+, IE 10+ */
    }
  }

  @keyframes myrotate {
    from {
      -webkit-transform: rotate(0deg) scale(0); /* Chrome 4+, Op 15+, Saf 3.1, iOS Saf 3.2+ */
      -moz-transform: rotate(0deg) scale(0); /* Fx 3.5-15 */
      -ms-transform: rotate(0deg) scale(0); /* IE 9 */
      -o-transform: rotate(0deg) scale(0); /* Op 10.5-12 */
      transform: rotate(0deg) scale(0); /* Fx 16+, IE 10+ */
      opacity: 0;
    }
    to {
      -webkit-transform: rotate(360deg) scale(1); /* Chrome 4+, Op 15+, Saf 3.1, iOS Saf 3.2+ */
      -moz-transform: rotate(360deg) scale(1); /* Fx 3.5-15 */
      -ms-transform: rotate(360deg) scale(1); /* IE 9 */
      -o-transform: rotate(360deg) scale(1); /* Op 10.5-12 */
      transform: rotate(360deg) scale(1); /* Fx 16+, IE 10+ */
    }
  }


  #chat-messages {
    height: calc(100% - 35vh);
    margin-top: 1vh;
    overflow-y: scroll;
    overflow-x: hidden;
    padding-right: 20px;
  }

  #chat-messages label {
    color: #aab8c2;
    font-weight: 600;
    font-size: 12px;
    text-align: center;
    margin: 15px 0;
    width: 290px;
    display: block;
  }

  #chat-messages div.message {
    padding: 0 0 30px 58px;
    clear: both;
    margin-bottom: 45px;
  }

  #chat-messages div.message.right {
    padding: 0 58px 30px 0;
    margin-right: -19px;
    margin-left: 19px;
  }

  #chat-messages .message img {
    float: left;
    margin-left: -38px;
    border-radius: 50%;
    width: 30px;
    margin-top: 12px;
  }

  #chat-messages div.message.right img {
    float: right;
    margin-left: 0;
    margin-right: -38px;
  }

  .message .bubble {
    background: #f0f4f7;
    font-size: 13px;
    font-weight: 600;
    padding: 12px 13px;
    border-radius: 5px 5px 5px 0px;
    color: #8495a3;
    position: relative;
    float: left;
  }

  #chat-messages div.message.right .bubble {
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

  div.message.right .corner {
    background: url("https://s3-us-west-2.amazonaws.com/s.cdpn.io/245657/bubble-cornerR.png") 0 0 no-repeat;
    left: auto;
    right: -5px;
  }

  .bubble span {
    color: #aab8c2;
    font-size: 11px;
    position: absolute;
    right: 0;
    bottom: -22px;
  }

  #send:hover {
    cursor: pointer;
  }

  #sendmessage {
    height: 7vh;
    position: relative;
    bottom: 0;
  }

  #sendmessage input {
    background: #fff;
    position: absolute;
    top: 0;
    left: 2vh;
    margin: 0;
    width: 80%;
    height: 6vh;
    border: none;
    padding: 0;
    font-size: 13px;
    font-family: "Open Sans", sans-serif;
    font-weight: 400;
    color: #585858;
  }

  #sendmessage input:focus {
    outline: 0;
  }

  #send {
    position: absolute;
    bottom: 0;
    right: 0;
    width: 20%;
  }

  .mdl-button--fab {
    max-width: 56px;
    max-height: 56px;
    width: 9vh;
    height: 9vh;
    min-width: 8vh;
    min-height: 8vh;
  }

  @media screen and (min-height: 640px) {
    .mdl-button--fab {
      min-width: 56px;
      min-height: 56px;
    }
  }

  #send button {
    -webkit-transition: all 500ms ease-out;
    -moz-transition: all 500ms ease-out;
    -ms-transition: all 500ms ease-out;
    -o-transition: all 500ms ease-out;
    transition: all 500ms ease-out;
  }

  #send button > i {
    -webkit-transition: all 500ms ease-out;
    -moz-transition: all 500ms ease-out;
    -ms-transition: all 500ms ease-out;
    -o-transition: all 500ms ease-out;
    transition: all 500ms ease-out;
  }

  #send:hover button {
    transform: rotate(-45deg);
  }

  #send:hover button > i {
    transform: translateY(-50%) translateX(-40%);
  }
</style>
