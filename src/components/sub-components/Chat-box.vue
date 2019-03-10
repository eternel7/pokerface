<template>
  <div v-if="chatroom" id="chatboxview">
    <div id="chat-messages" ref="chatmessages">
      <div is="MsgItem" v-for="msg in chats" :key="chats.indexOf(msg)"
           v-bind:user="user"
           v-bind:chatroom="chatroom"
           v-bind:msg="msg"
           v-bind:questions="questions">
      </div>
    </div>
    <div id="sendmessage">
      <textarea type="text" ref="message" placeholder="Send message..."
                @keyup.ctrl.enter="sendMessage"></textarea>
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
  import ReconnectingWebSocket from 'reconnecting-websocket'
  import axios from 'axios'
  import Animate from '@/assets/animate-utils.js'

  export default {
    name: 'chatBox',
    extends: PageBase,
    mixins: [authMixin],
    components: {MsgItem},
    data () {
      return {
        sessionStarted: false,
        displaySearch: true,
        displayBack: true,
        displayHeader: false,
        chats: [],
        nextId: 1,
        users: [],
        pgNum: 0,
        pgSize: 3,
        chatSocket: undefined
      }
    },
    computed: {
      chatroom: function () {
        let vm = this
        return vm.$root.chatrooms.filter(function (row) {
          return row.id === vm.$route.params.id
        })[0]
      },
      user: function () {
        return this.$root.user
      },
      connectedUsers: function () {
        let vm = this
        return vm.users.slice(vm.pgNum * vm.pgSize, (vm.pgNum + 1) * vm.pgSize)
      },
      questions: function () {
        let vm = this
        if (vm.$root.questions instanceof Object) {
          return (vm.$root.questions[vm.$route.params.id]) ? vm.$root.questions[vm.$route.params.id] : []
        }
        return []
      }
    },
    created () {
      if (!this.chatroom || this.chatroom.length < 1) {
        this.$router.push({name: 'Home'})
      } else {
        let vm = this
        vm.tryGetChatroomQuestion()
        vm.startChatSession()
      }
    },
    beforeDestroy: function () {
      if (this.chatSocket) {
        this.chatSocket.close()
      }
    },
    methods: {
      tryGetChatroomQuestion (evt) {
        let vm = this
        vm.errors = []
        vm.$root.loading = true
        let roomId = vm.$route.params.id
        axios.get('/api/chatroomquestions/' + roomId, vm.authHeader())
          .then(function (response) {
            vm.$root.loading = false
            // handle success
            if (response.data.questions) {
              vm.$set(vm.$root.questions, roomId, response.data.questions)
            } else {
              vm.errors = []
              vm.errors.push({message: response.data.message})
            }
          })
          .catch(function (error) {
            // handle error
            console.log(error)
            vm.$root.loading = false
            vm.errors = []
            vm.errors.push(error)
          })
          .then(function () {
            // always executed
            vm.$root.loading = false
          })
      },
      addChat: function (msg, user) {
        let vm = this
        if (msg && !user) {
          vm.chats.push({
            identifier: vm.nextId++,
            origin: 0,
            message: msg,
            date: new Date()
          })
        } else if (msg) {
          vm.chats.push({
            identifier: vm.nextId++,
            origin: user,
            message: msg,
            date: new Date(),
            question: false
          })
        }
        vm.$nextTick(vm.scrollDown())
      },
      addUserToRoom: function (username, allConnected) {
        console.log('connection of', username, allConnected)
        this.users = allConnected
      },
      removeUserFromRoom: function (username, allConnected) {
        console.log('disconnection of', username, allConnected)
        this.users = allConnected
      },
      manageMessage: function (msg) {
        let vm = this
        let msgJson = JSON.parse(msg.data)
        if (msgJson.text || msgJson.username === 0) {
          // Bot message
          vm.addChat(msgJson.text || msgJson.message)
        } else {
          if (msgJson.msg_type === 4) {
            vm.addUserToRoom(msgJson.username, msgJson.all_users)
          }
          if (msgJson.msg_type === 5) {
            vm.removeUserFromRoom(msgJson.username, msgJson.all_users)
          }
          if (msgJson.username !== vm.user.username) {
            if (msgJson.msg_type === 0) {
              vm.addChat(msgJson.message, {
                username: msgJson.username,
                portrait: msgJson.portrait
              })
            }
          }
        }
      },
      startChatSession () {
        let vm = this
        if (vm.$route.params.id) {
          vm.sessionStarted = true
          let wsScheme = window.location.protocol === 'https:' ? 'wss' : 'ws'
          vm.chatSocket = new ReconnectingWebSocket(wsScheme + '://' + window.location.host + '/ws/chat/' + vm.$route.params.id + '/')
          vm.chatSocket.onmessage = function (message) {
            vm.manageMessage(message)
          }
        }
      },
      scrollDown: function () {
        let vm = this
        vm.$nextTick(function () {
          let chat = vm.$refs['chatmessages']
          let bubblesBottoms = [].slice.call(document.querySelectorAll('.left > .time'))
          if (bubblesBottoms) {
            let timeDIVHeight = 20
            let nextY = bubblesBottoms.reduce(function (max, val) {
              let pos = Math.ceil(val.offsetTop)
              return (max > pos) ? max : pos
            }, 0)
            nextY = nextY - chat.offsetTop - chat.offsetHeight + timeDIVHeight
            if (nextY > 0) {
              Animate.scrollToPos(chat, nextY, 600)
            }
          }
        })
      },
      sendMessage: function (evt) {
        let vm = this
        let msg = vm.$refs['message']
        if (msg.value && msg.value.length > 0) {
          let txt = msg.value
          txt = txt.trim()
          vm.chats.push({
            identifier: vm.nextId++,
            origin: 1,
            command: 'send',
            message: txt,
            date: new Date(),
            question: false
          })
          vm.$nextTick(vm.tryGetResponse({
            origin: 1,
            command: 'send',
            message: txt,
            date: new Date()
          }))
          msg.value = ''
          msg.focus()
        }
      },
      tryGetResponse (msg) {
        let vm = this
        vm.errors = []
        if (vm.chatSocket) {
          vm.chatSocket.send(JSON.stringify(msg))
        }
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->


<style scoped>
  #chatboxview {
    position: relative;
    height: calc(92vh - 49px);
    left: 50%;
    -webkit-transform: translateX(-50%); /* Chrome 4+, Op 15+, Saf 3.1, iOS Saf 3.2+ */
    -moz-transform: translateX(-50%); /* Fx 3.5-15 */
    -ms-transform: translateX(-50%); /* IE 9 */
    -o-transform: translateX(-50%); /* Op 10.5-12 */
    transform: translateX(-50%); /* Fx 16+, IE 10+ */
    margin-left: auto;
    margin-right: auto;
    background: #fff;
    width: 100%;
    max-width: 700px;
  }

  #chat-messages {
    position: relative;
    height: 80%;
    overflow-y: scroll;
    overflow-x: hidden;
    padding-right: 20px;
    border-bottom: solid 1px #e4e4e4;
  }

  #sendmessage {
    position: relative;
    height: 20%;
    position: relative;
    bottom: 0;
  }

  #sendmessage textarea {
    background: #fff;
    position: absolute;
    top: 5%;
    left: 2vh;
    margin: 0;
    width: 80%;
    height: 90%;
    border: none;
    padding: 0;
    font-size: 13px;
    font-family: "Roboto", "Open Sans", sans-serif;
    font-weight: 400;
    color: #403f3e;
  }

  #sendmessage textarea:focus {
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
    bottom: calc(8vh - 12px);
    right: 3vw;
  }

  @media screen and (min-height: 640px) {
    .mdl-button--fab {
      min-width: 56px;
      min-height: 56px;
    }
  }

  @media screen and (max-height: 640px) {
    .mdl-button--fab {
      bottom: 24px;
      right: 2vw;
    }

    .mdl-button--fab > i {
      font-size: 20px;
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
