<template>
  <div v-if="chatroom" id="chatroomview">
    <ul v-if="!selectedQuestion && questions " id="questions" ref="questions" class="mdl-list list"
        v-bind:class="{'is-active' : (selectedQuestion!==undefined)}">
      <li is="QuestionItem" v-for="(question, index) in questions"
          v-on:click.native="displayQuestionForm(question)"
          :key="index"
          v-bind:user="user"
          v-bind:chatroom="chatroom"
          v-bind:question="question"
          v-bind:search="search">
      </li>
    </ul>
    <div v-else class="selected-question">
      <QuestionAndAnswers
              v-bind:question="selectedQuestion"
              v-on:close="unselectQuestion()"></QuestionAndAnswers>
      <div id="sendmessage">
      <textarea type="text" ref="message" required placeholder="Answer or ask for more information..."
                @keyup.ctrl.enter="sendMessage"></textarea>
        <span id="send" @click="sendMessage">
        <button id="sendButton" class="mdl-button mdl-js-button mdl-js-ripple-effect mdl-button--colored">
          <i class="material-icons">send</i>
        </button>
      </span>
      </div>
    </div>
    <button v-if="!selectedQuestion" tabindex="30" type="button"
            class="mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--fab mdl-button--colored"
            @click="displayQuestionForm(undefined)">
      <i class="material-icons">add</i>
    </button>
  </div>
</template>

<script>
  import QuestionItem from '@/components/sub-components/Question-item'
  import QuestionAndAnswers from '@/components/sub-components/Question-and-answers'
  import {authMixin} from '@/auth/authMixin.js'
  import DataUtils from '@/assets/data-utils.js'
  import SortUtils from '@/assets/sort-utils.js'

  require('material-design-lite')

  export default {
    name: 'chatQuestions',
    mixins: [authMixin],
    components: {QuestionItem, QuestionAndAnswers},
    props: ['chatroom', 'user', 'search'],
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
        if (vm.$root.store.questions instanceof Object) {
          let unsorted = Object.assign([], (vm.$root.store.questions[vm.$route.params.id]) ? vm.$root.store.questions[vm.$route.params.id] : [])
          let searchInKeys = ['body']
          if (typeof vm.search === 'string' && vm.search !== '') {
            return unsorted.filter(function (row) {
              return Object.keys(row).some(function (key) {
                if (searchInKeys.indexOf(key) > -1) {
                  return String(row[key]).toLowerCase().indexOf(vm.search) > -1
                }
              })
            }).sort(SortUtils.onUpdated_at)
          }
          return unsorted.sort(SortUtils.onUpdated_at)
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
      },
      displayQuestionForm: function (question) {
        if (question) {
          this.selectedQuestion = question
        } else {
          console.log('question empty form')
        }
      },
      unselectQuestion: function () {
        this.selectedQuestion = undefined
      },
      sendMessage: function (msg) {
        console.log('sendMessage', msg)
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
    height: calc(92vh - 50px);
    width: 100%;
    max-width: 700px;
  }

  .list {
    margin: 0;
    width: 98%;
    padding: 0 1% 0 1%;
    position: relative;
    height: 100%;
    overflow-y: scroll;
    overflow-x: hidden;
    -ms-overflow-style: none;
    overflow: -moz-scrollbars-none;
  }

  .list > li {
    text-align: left;
    vertical-align: middle;
  }

  @media screen and (max-height: 640px) {
    .list > li {
      padding: 0;
    }
  }

  button.mdl-button--fab {
    position: fixed;
    bottom: 2vh;
    right: 2vw;
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
    resize: none;
    background: #fff;
    position: relative;
    padding: 0;
    margin: 0;
    width: 100%;
    height: 90%;
    display: table-cell;
    border: 0 solid #e0e0e0;
    border-right-width: 1px;
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
