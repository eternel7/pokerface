<template>
  <div>
    <div v-if="chatroom" id="chatroomview">
      <div id="chatroomprofile"
           v-bind:style="'background-image: url('+chatroom.image+')'">
        <div id="bot">{{chatroom.label}}</div>
        <div id="close" v-on:click="backHome">
          <i class="material-icons">close</i>
        </div>
      </div>
      <div id="chatroomtabs" class="mdl-tabs mdl-js-tabs mdl-js-ripple-effect is-upgraded">
        <div class="mdl-tabs__tab-bar">
          <div v-for="tab in tabs" class="mdl-tabs__tab link"
               v-bind:href="tab.id" v-bind:id="'chat_tab_'+tab.id" v-on:click="clickOnTab(tab.id)"
               v-bind:class="{'is-active' : (tab.id===tabActive)}">
            <i class="material-icons">
              {{tab.icon}}
            </i><span>{{$t('chat.' + tab.Title)}}</span>
          </div>
        </div>
        <div class="mdl-tabs__panel is-active" id="0" v-if="tabActive==='0'">
          <ChatBox v-bind:chatroom="chatroom"
                   v-bind:chatSocket="chatSocket"
                   v-bind:chats="chats"
                   v-bind:user="user"></ChatBox>
        </div>
        <div class="mdl-tabs__panel is-active" id="1" v-if="tabActive==='1'">
          <ChatroomUsers v-bind:chatroom="chatroom"
                         v-bind:user="user"></ChatroomUsers>
        </div>
        <div class="mdl-tabs__panel is-active" id="2" v-if="tabActive==='2'">
          <div>Hello world!</div>
        </div>
        <div class="mdl-tabs__panel is-active" id="3" v-if="tabActive==='3'">
          <div>Hello world!</div>
        </div>
        <div class="mdl-tabs__panel is-active" id="4" v-if="tabActive==='4'">
          <div>Hello world!</div>
        </div>
      </div>
    </div>
    <h4 class="solo" v-else v-click="backHome()">
      {{$t('ConnectionNeeded')}}
    </h4>
  </div>
</template>

<script>
  import ReconnectingWebSocket from 'reconnecting-websocket'
  import ChatBox from '@/components/sub-components/Chat-box'
  import ChatroomUsers from '@/components/sub-components/Chatroom-users'
  import {authMixin} from '@/auth/authMixin.js'

  export default {
    name: 'chat',
    mixins: [authMixin],
    components: {ChatBox, ChatroomUsers},
    data () {
      return {
        tabs: [
          {
            id: '0',
            Title: 'TabChat',
            icon: 'chat'
          },
          {
            id: '1',
            Title: 'TabUsers',
            icon: 'people'
          },
          {
            id: '2',
            Title: 'TabQuestions',
            icon: 'contact_support'
          },
          {
            id: '3',
            Title: 'TabAnswers',
            icon: 'question_answer'
          },
          {
            id: '4',
            Title: 'TabData',
            icon: 'attachment'
          }
        ],
        sessionStarted: false,
        chats: [],
        displaySearch: true,
        displayBack: true,
        displayHeader: false,
        chatSocket: undefined,
        tabActive: '0',
        message: '',
        errors: [],
        updateNeeded: 'noNeed',
        loaded: false
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
      }
    },
    created () {
      if (!this.chatroom || this.chatroom.length < 1) {
        this.$router.push({name: 'Home'})
      } else {
        let vm = this
        vm.startReconnectingWebSocket()
      }
    },
    beforeDestroy: function () {
      if (this.chatSocket) {
        this.chatSocket.close()
      }
    },
    methods: {
      backHome: function () {
        this.$router.push({name: 'Home'})
      },
      clickOnTab: function (tabId) {
        if (tabId === '5') {
          this.backHome()
        }
        this.tabActive = tabId
      },
      startReconnectingWebSocket () {
        let vm = this
        if (vm.$route.params.id) {
          vm.sessionStarted = true
          let wsScheme = window.location.protocol === 'https:' ? 'wss' : 'ws'
          vm.chatSocket = new ReconnectingWebSocket(wsScheme + '://' + window.location.host + '/ws/chat/' + vm.$route.params.id + '/')
        }
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->


<style scoped>

  h4.solo {
    color: #eeeeee;
  }

  #chatroomview {
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

  #chatroomprofile {
    position: relative;
    padding: 0;
    margin: 0;
    height: 8vh;
    overflow: hidden;
    text-align: center;
    background-color: #e4e4e4;
    background-size: cover;
    background-repeat: no-repeat;
    color: #fff;
  }

  #bot {
    position: absolute;
    bottom: 0;
    vertical-align: middle;
    width: 100%;
    height: 50%;
    line-height: 4vh;
    background-color: rgba(88, 88, 88, 0.54);
    font-weight: 400;
    font-size: 3vh;
  }

  @media screen and (max-height: 640px) {
    #bot {
      height: 9vh;
      min-height: 9vh;
      line-height: 9vh;
      font-size: 20px;
    }
  }

  #chatroomtabs {
    height: 92vh;
  }

  .mdl-tabs__tab > i {
    display: block;
    margin-top: 10px;
  }

  .mdl-tabs__tab > span {
    display: none;
  }

  #close {
    position: absolute;
    color: white;
    top: 11px;
    right: 14px;
    width: 24px;
    height: 24px;
    cursor: pointer;
    z-index: 2;
  }

  #close:hover > i {
    color: rgb(255, 64, 129);
  }

  #close > i:hover {
    color: rgb(255, 64, 129);
  }

  #close > i {
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
</style>
