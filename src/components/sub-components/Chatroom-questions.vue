<template>
  <div v-if="chatroom" id="chatboxview">
    <div id="chatroom-questions" ref="chatromquestions"
         v-bind:class="{'is-active' : (selectedQuestion!==undefined)}">

    </div>
    <div v-if="selectedQuestion" id="sendmessage">
      <textarea type="text" ref="message" placeholder="Send message..."
                @keyup.ctrl.enter="sendMessage"></textarea>
      <span id="send" @click="sendMessage">
        <button id="sendButton" class="mdl-button mdl-js-button mdl-js-ripple-effect mdl-button--colored">
          <i class="material-icons">send</i>
        </button>
      </span>
    </div>
  </div>
</template>

<script>
  import MsgItem from '@/components/sub-components/Msg-item'
  import {authMixin} from '@/auth/authMixin.js'

  export default {
    name: 'chatQuestions',
    mixins: [authMixin],
    components: {MsgItem},
    props: ['chatroom', 'chats', 'user', 'chatSocket', 'nextId'],
    data () {
      return {
        selectedQuestion: undefined,
        scrolling: false,
        lastScrollTop: 0
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
      }
    },
    methods: {
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

  #chatroom-questions {
    position: relative;
    height: 100%;
    background-color: #959595;
    overflow-y: scroll;
    overflow-x: hidden;
    padding-right: 20px;
    border-bottom: solid 1px #e4e4e4;
  }

  #chatroom-questions.is-active {
    height: 80%;
  }

  #sendmessage {
    position: relative;
    padding: 5px;
    height: 20%;
    bottom: 0;
    width: calc(100% - 10px);
    display: table;
  }

  #sendmessage textarea {
    background: #fff;
    position: relative;
    padding: 0;
    margin: 0;
    width: 100%;
    height: 90%;
    display: table-cell;
    border: none;
    font-size: 13px;
    font-family: "Roboto", "Open Sans", sans-serif;
    font-weight: 400;
    color: #403f3e;
  }

  #sendmessage textarea:focus {
    outline: 0;
  }

  #send {
    position: relative;
    padding: 0;
    margin: 0;
    cursor: pointer;
    width: 20%;
    height: 100%;
    display: table-cell;
  }

  #send button {
    bottom: 45%;
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

</style>
