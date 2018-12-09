<template>
  <div v-if="chatroom" id="chatview">
    <div id="profile"
    v-bind:style="'background-image: url('+chatroom.user_image+')'">
      <div id="close" v-on:click="backHome">
        <i class="material-icons">close</i>
      </div>
      <div id="user">{{chatroom.user_label}}</div>
    </div>
    <div id="chat-messages" ref="chatmessages">
      <div is="MsgItem" v-for="msg in chats"
           v-bind:user="user"
           v-bind:msg="msg"
           v-bind:now="now">
      </div>
    </div>

    <div id="sendmessage">
      <input type="text" ref="message" placeholder="Send message..."
             @keyup.enter="sendMessage"/>
      <div id="send">
        <button id="sendButton" @click="sendMessage"
                class="mdl-button mdl-js-button mdl-button--fab mdl-js-ripple-effect mdl-button--colored">
          <i class="material-icons">send</i>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
  import PageBase from '@/components/pages/Page'
  import MsgItem from '@/components/sub-components/Msg-item'
  import {authMixin} from '@/auth/authMixin.js'
  import axios from 'axios'

  export default {
    name: 'chat',
    extends: PageBase,
    mixins: [authMixin],
    components: {MsgItem},
    data () {
      return {
        displaySearch: true,
        displayBack: true,
        displayHeader: false,
        chats: [],
        now: Date.now()
      }
    },
    mounted: function () {
      let vm = this
      setInterval(function () {
        vm.$data.now = Date.now()
      }, 1000)
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
        vm.$nextTick(vm.scrollDown())
      }
    },
    methods: {
      backHome: function () {
        this.$router.push({name: 'Home'})
      },
      scrollDown: function () {
        let vm = this
        vm.$nextTick(function () {
          let messages = vm.$refs['chatmessages']
          if (messages) {
            messages.scrollTop = messages.scrollHeight
          }
        })
      },
      sendMessage: function (evt) {
        let vm = this
        let msg = vm.$refs['message']
        if (msg.value && msg.value.length > 0) {
          vm.chats.push({
            origin: 1,
            text: msg.value,
            date: new Date()
          })
          vm.$nextTick(vm.tryGetResponse(msg.value))
          msg.value = ''
          msg.focus()
          vm.$nextTick(vm.scrollDown())
        }
      },
      tryGetResponse (msg) {
        let vm = this
        vm.errors = []
        console.log('send message')
        axios.post('api/chatterbot/', {text: msg}, vm.authHeader())
          .then(function (response) {
            console.log('received response')
            // handle success
            if (response.data.text && response.data.text.length > 0) {
              vm.chats.push({
                origin: 0,
                text: response.data.text,
                date: new Date()
              })
            }
          })
          .catch(function (error) {
            // handle error
            console.log(error)
          })
          .then(function () {
            vm.$nextTick(vm.scrollDown())
          })
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

  #close > i:hover {
    opacity: 1;
  }

  #close > i {
    opacity: 0.8;
    background-color: rgba(55, 55, 55, 0.3);
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
    height: 65vh;
    margin-top: 1vh;
    overflow-y: scroll;
    overflow-x: hidden;
    padding-right: 20px;
  }

  #sendmessage {
    height: 9vh;
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
    height: 100%;
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
    height: 100%;
  }

  .mdl-button--fab {
    max-width: 56px;
    max-height: 56px;
    width: 8vh;
    height: 8vh;
    min-width: 8vh;
    min-height: 8vh;
    position: fixed;
    bottom: 2vh;
    right: 2vw;
  }

  @media screen and (min-height: 640px) {
    .mdl-button--fab {
      min-width: 56px;
      min-height: 56px;
    }
  }

  #send button {
    cursor: pointer;
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
