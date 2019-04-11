<template>
  <div v-if="chatroom" id="chatboxview">
    <div id="chat-messages" ref="chatmessages">
      <div is="MsgItem" v-for="msg in chats" :key="chats.indexOf(msg)"
           v-bind:user="user"
           v-bind:chatroom="chatroom"
           v-bind:msg="msg"
           v-bind:chats="chats"
           v-bind:now="now"
           v-bind:questions="questions">
      </div>
    </div>
    <div id="sendmessage">
      <textarea type="text" ref="message" required placeholder="Send message..."
                @keyup.ctrl.enter="sendMessage"></textarea>
      <div id="send" @click="sendMessage">
        <button id="sendButton"
                class="mdl-button mdl-button--colored">
          <i class="material-icons">send</i>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
  import ReconnectingWebSocket from 'reconnecting-websocket'
  import MsgItem from '@/components/sub-components/Msg-item'
  import {authMixin} from '@/auth/authMixin.js'
  import Animate from '@/assets/animate-utils.js'

  export default {
    name: 'chatBox',
    mixins: [authMixin],
    components: {MsgItem},
    props: ['chatroom', 'chats', 'user', 'chatSocket'],
    data () {
      return {
        scrolling: false,
        lastScrollTop: 0,
        now: Date.now()
      }
    },
    computed: {
      questions: function () {
        let vm = this
        if (vm.$root.questions instanceof Object) {
          return (vm.$root.questions[vm.$route.params.id]) ? vm.$root.questions[vm.$route.params.id] : []
        }
        return []
      }
    },
    created () {
      let vm = this
      if (!vm.chatroom || vm.chatroom.length < 1) {
        vm.$router.push({name: 'Home'})
      } else {
        vm.addManageMessages(vm)
        vm.scrollToLastPosition()
      }
    },
    mounted: function () {
      let vm = this
      setInterval(function () {
        vm.$data.now = Date.now()
      }, 1000)
    },
    methods: {
      scrollToLastPosition () {
        let vm = this
        setTimeout(function () {
          vm.$nextTick(vm.scrollDown(-1, true))
        }, 100)
      },
      addManageMessages: function (vm) {
        if (vm.chatSocket instanceof ReconnectingWebSocket && !vm.chatSocket.onmessage) {
          vm.chatSocket.onmessage = function (message) {
            vm.manageMessage(message)
          }
        } else if (!(vm.chatSocket instanceof ReconnectingWebSocket)) {
          setTimeout(function () {
            vm.addManageMessages(vm)
          }, 1000)
        }
      },
      addChat: function (msg, user, id) {
        let vm = this
        if (msg && !user) {
          if (msg instanceof Object && vm) {
            let info = Object.assign({}, msg)
            delete info.msg
            msg = vm.$root.$t(msg.msg, info)
          }
          vm.chats.push({
            origin: 0,
            message: msg,
            date: new Date()
          })
        } else if (msg) {
          vm.chats.push({
            origin: user,
            message: msg,
            date: new Date(),
            question: false,
            post_id: id
          })
        }
        vm.$nextTick(vm.scrollDown())
      },
      updateChat: function (savedMsg) {
        let vm = this
        // update a message send by user
        let ind = vm.chats.findIndex(function (c) {
          return (c.message === savedMsg.message &&
            c.post_id === undefined &&
            c.origin === 1)
        })
        if (ind) {
          let msgToUpdate = vm.chats[ind]
          if (msgToUpdate) {
            msgToUpdate.post_id = savedMsg.post_id
            vm.chats.splice(ind, 1, msgToUpdate)
          }
        }
      },
      manageMessage: function (msg) {
        let vm = this
        let msgJson = JSON.parse(msg.data)
        console.log('manageMessage', msgJson)
        if (msgJson.text || msgJson.username === 0) {
          // Bot message
          vm.addChat(msgJson.text || msgJson.message)
        } else {
          if (msgJson.username !== vm.user.username) {
            if (msgJson.msg_type === 0) {
              vm.addChat(msgJson.message, {
                username: msgJson.username,
                portrait: msgJson.portrait
              }, msgJson.post_id)
            }
          } else {
            // update a message send by user
            vm.updateChat(msgJson)
          }
        }
      },
      scrollDown: function (time, forced) {
        let vm = this
        if (vm.scrolling === false) {
          let chat = document.getElementById('chat-messages')
          if (chat && (vm.lastScrollTop - 5 <= chat.scrollTop || forced)) {
            vm.scrolling = true
            vm.$nextTick(function () {
              setTimeout(function () {
                let bubblesBottoms = [].slice.call(document.querySelectorAll('.left > .time'))
                if (bubblesBottoms && chat) {
                  let timeDIVHeight = 20
                  let nextY = bubblesBottoms.reduce(function (max, val) {
                    let pos = Math.ceil(val.offsetTop)
                    return (max > pos) ? max : pos
                  }, 0)
                  nextY = nextY - chat.offsetTop - chat.offsetHeight + timeDIVHeight
                  if (nextY > 0) {
                    time = time || 600
                    Animate.scrollToPos(chat, nextY, time)
                    vm.lastScrollTop = nextY
                  }
                }
                vm.scrolling = false
              }, 500)
            })
          }
        }
      },
      sendMessage: function (evt) {
        let vm = this
        let msg = vm.$refs['message']
        if (msg.value && msg.value.length > 0) {
          let txt = msg.value
          txt = txt.trim()
          vm.chats.push({
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
  }

  #chat-messages {
    position: relative;
    height: 80%;
    overflow-y: auto;
    overflow-x: hidden;
    padding-right: 20px;
    border-bottom: solid 1px #e4e4e4;
  }

  #sendmessage {
    position: relative;
    height: 20%;
    bottom: 0;
    width: 100%;
    display: table;
  }

  #sendmessage textarea {
    resize: none;
    background: #fff;
    position: relative;
    margin: 5px;
    width: 100%;
    height: 90%;
    display: table-cell;
    border: 0 solid #e0e0e0;
    border-right-width: 1px;
    padding: 0;
    font-size: 13px;
    font-family: "Roboto", "Open Sans", sans-serif;
    font-weight: 400;
    color: #403f3e;
  }

  #sendmessage textarea:focus {
    outline: 0;
    outline: none;
  }

  #send {
    position: relative;
    cursor: pointer;
    margin: 5px;
    height: 100%;
    padding: 0;
    display: table-cell;
  }

  #send button {
    background-color: rgba(0, 0, 0, 0);
    bottom: 50%;
    -webkit-transition: all 500ms ease-out;
    -moz-transition: all 500ms ease-out;
    -ms-transition: all 500ms ease-out;
    -o-transition: all 500ms ease-out;
    transition: all 500ms ease-out;
  }

  #send:hover button {
    background-color: rgba(0, 0, 0, 0);
    color: rgb(255, 64, 129);
  }

  #sendmessage textarea:not(:invalid) ~ #send button {
    background-color: rgba(0, 0, 0, 0);
    color: rgb(255, 64, 129);
  }
</style>
