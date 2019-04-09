<template>
  <div class="questionAndAnswer" id="questionAndAnswers">
    <div class="question" id="question">
      <qaItem v-bind:item="question"
              v-bind:question="undefined"
              v-bind:user="user"
              v-bind:closable="true"
              v-bind:search="search"
              v-on:close="close()"></qaItem>
      <div v-if="question.answers.length>0" class="answers" id="answers">
        <h5 v-if="question.answers.length==1" class="answers-title">{{question.answers.length}} Answer</h5>
        <h5 v-else class="answers-title">{{question.answers.length}} Answers</h5>
        <ul class="answers-list">
          <li is="AnswerItem" v-for="answer in question.answers"
              v-bind:answer="answer"
              v-bind:question="question"
              :key="answer.id"
              v-bind:user="user"
              v-bind:search="search"></li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
  import qaItem from '@/components/sub-components/Q&A-item'
  import AnswerItem from '@/components/sub-components/Answer-item'
  import DataUtils from '@/assets/data-utils.js'

  export default {
    name: 'Question-and-answers',
    components: {qaItem, AnswerItem},
    props: ['user', 'chatroom', 'question', 'search'],
    data () {
      return {
        addComment: false,
        comments: []
      }
    },
    methods: {
      tryGetQuestionAnswers: function () {
        DataUtils.refreshQuestionAnswers(this, true, this.question)
      },
      close: function () {
        this.$emit('close')
      }
    }
  }
</script>

<style scoped>
  .questionAndAnswer {
    position: relative;
    height: 80%;
    left: 50%;
    -webkit-transform: translateX(-50%); /* Chrome 4+, Op 15+, Saf 3.1, iOS Saf 3.2+ */
    -moz-transform: translateX(-50%); /* Fx 3.5-15 */
    -ms-transform: translateX(-50%); /* IE 9 */
    -o-transform: translateX(-50%); /* Op 10.5-12 */
    transform: translateX(-50%); /* Fx 16+, IE 10+ */
    margin-left: auto;
    margin-right: auto;
    background: #fff;
    max-width: 700px;
    overflow-y: scroll;
    overflow-x: hidden;
    padding: 5px;
    border-bottom: solid 1px #e4e4e4;
  }

  .text {
    word-wrap: break-word;
    font-size: 13px;
    font-family: "Roboto", "Open Sans", sans-serif;
    font-weight: 400;
    color: #403f3e;
  }

  .answers-title {
    border-top: solid 1px #e4e4e4;
    padding-top: 5px;
    text-align: left;
  }

  ul.answers-list {
    padding-left: 0;
  }
</style>
