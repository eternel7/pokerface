<template>
  <div v-if="chatroom" id="chatroomview">
    <ul v-if="questions" id="questions" ref="questions" class="mdl-list"
        v-bind:class="{'is-active' : (selectedQuestion!==undefined)}">
      <li is="QuestionItem" v-for="question in questions" :key="questions.indexOf(question)"
          v-bind:user="user"
          v-bind:chatroom="chatroom"
          v-bind:question="question">
      </li>
    </ul>
    <div v-if="selectedQuestion" class="selected-question">
      <questionForm></questionForm>
      <div id="sendmessage">
      <textarea type="text" ref="message" placeholder="Send message..."
                @keyup.ctrl.enter="sendMessage"></textarea>
        <span id="send" @click="sendMessage">
        <button id="sendButton" class="mdl-button mdl-js-button mdl-js-ripple-effect mdl-button--colored">
          <i class="material-icons">send</i>
        </button>
      </span>
      </div>
    </div>
  </div>
</template>

<script>
  import QuestionItem from '@/components/sub-components/Question-item'
  import {authMixin} from '@/auth/authMixin.js'
  import DataUtils from '@/assets/data-utils.js'

  function sortQuestion (q1, q2) {
    let d1 = new Date(q1.updated_at)
    let d2 = new Date(q2.updated_at)
    return (d1 < d2) ? 1 : -1
  }

  export default {
    name: 'chatQuestions',
    mixins: [authMixin],
    components: {QuestionItem},
    props: ['chatroom', 'user'],
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
          let unsorted = (vm.$root.questions[vm.$route.params.id]) ? vm.$root.questions[vm.$route.params.id] : []
          return unsorted.sort(sortQuestion)
        }
        return []
      }
    },
    created () {
      let vm = this
      if (!vm.chatroom || vm.chatroom.length < 1) {
        vm.$router.push({name: 'Home'})
      } else {
        vm.tryGetChatroomQuestion()
      }
    },
    methods: {
      tryGetChatroomQuestion: function () {
        DataUtils.refreshQuestions(this, true)
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->


<style scoped>
  #chatroomview {
    position: relative;
    margin-left: auto;
    margin-right: auto;
    background: #fff;
    height: 92%;
    width: 100%;
    max-width: 700px;
  }

  #questions {
    margin: 0;
    width: 99%;
    padding-left: 1%;
    position: relative;
    height: 97%;
    overflow-y: scroll;
    overflow-x: hidden;
    padding-bottom: 5px;
    -ms-overflow-style: none;
    overflow: -moz-scrollbars-none;
  }

  #questions.is-active {
    height: 80%;
  }

  #questions > li {
    text-align: left;
    vertical-align: middle;
    padding: 0;
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
