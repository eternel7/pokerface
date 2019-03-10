<template>
  <div v-if="chatroom" id="chatboxview">
    <ul v-if="users" id="connected" ref="connectedUsers" v-bind:class="{ collapse: pgNum<0 || users.length<1}">
      <li v-for="u in connectedUsers" :key="u.username"
          v-if="u.portrait">
        <img class="mdl-list__item-icon" v-bind:alt="u.username"
             v-bind:src="u.portrait"/>
      </li>
      <li class="paginate-tool" v-if="users.length>0">
        <i v-if="pgNum > -1" class="material-icons left link" @click="pgNum--">chevron_left</i>
        <i @click="pgNum = (pgNum===0) ?  -1 : 0 " class="material-icons link  mdl-badge mdl-badge--overlap"
           v-bind:data-badge="users.length">supervised_user_circle</i>
        <i v-if="pgNum < (users.length/pgSize - 1)" class="material-icons right link"
           @click="pgNum++">chevron_right</i>
      </li>
    </ul>
  </div>
</template>

<script>
  import {authMixin} from '@/auth/authMixin.js'
  import axios from 'axios'

  export default {
    name: 'chatroomUsers',
    mixins: [authMixin],
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
      }
    },
    created () {
      if (!this.chatroom || this.chatroom.length < 1) {
        this.$router.push({name: 'Home'})
      } else {
        let vm = this
        vm.tryGetChatroomUsers()
      }
    },
    methods: {
      tryGetChatroomUsers (evt) {
        let vm = this
        vm.errors = []
        vm.$root.loading = true
        let roomId = vm.$route.params.id
        axios.get('/api/chatroomusers/' + roomId, vm.authHeader())
          .then(function (response) {
            vm.$root.loading = false
            // handle success
            if (response.data.users) {
              vm.$set(vm.users, roomId, response.data.users)
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

  #connected {
    margin-top: 2px;
    font-size: 12px;
    line-height: 14px;
    width: auto;
    display: table;
    padding-left: 1vw;
    background-color: rgba(88, 88, 88, 0.34);
  }

  #connected.collapse {
    margin-top: 2vh;
  }

  #connected > li {
    color: #fff;
    width: auto;
    list-style-type: none;
    padding: 2px;
    margin-bottom: 2px;
    text-align: left;
    vertical-align: middle;
    background-color: rgba(88, 88, 88, 0.34);
  }

  #connected > li > img {
    border-radius: 50%;
    border: solid 2px #fff;
    width: 3vh;
    height: 3vh;
  }

  #connected > li.paginate-tool {
    text-align: center;
  }

  .paginate-tool > i.left {
    float: left;
  }

  .paginate-tool > i.right {
    float: right;
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
    background-color: rgba(88, 88, 88, 0.54);
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
    height: 60vh;
    overflow-y: scroll;
    overflow-x: hidden;
    padding-right: 20px;
    border-bottom: solid 1px #e4e4e4;
  }

  #sendmessage {
    height: 14vh;
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
    bottom: 3.5vh;
    right: 2vw;
  }

  @media screen and (min-height: 640px) {
    .mdl-button--fab {
      min-width: 56px;
      min-height: 56px;
    }
  }

  @media screen and (max-height: 640px) {
    .mdl-button--fab {
      bottom: 2.5vh;
      right: 1vw;
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
