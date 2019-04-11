<template>
  <div class="questionAndAnswer" id="questionAndAnswers"
       v-bind:class="{'full-size': answered}">
    <div class="question" id="question">
      <qaItem v-bind:item="question"
              v-bind:question="undefined"
              v-bind:user="user"
              v-bind:search="search"></qaItem>
      <div v-if="question.answers.length>0" class="answers" id="answers">
        <h5 v-if="question.answers.length==1" class="answers-title">{{question.answers.length}} Answer</h5>
        <h5 v-else class="answers-title">{{question.answers.length}} Answers</h5>
        <ul class="answers-list">
          <li is="AnswerItem" v-for="answer in sortedAnswers"
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
    props: ['user', 'chatroom', 'question', 'search', 'answered'],
    data () {
      return {
        addComment: false,
        comments: []
      }
    },
    computed: {
      sortedAnswers: function () {
        let vm = this
        if (vm.question && vm.question.answers) {
          return vm.question.answers.sort(vm.sortAnswers)
        }
        return []
      }
    },
    methods: {
      sortAnswers: function (a1, a2) {
        if (this.question.answer === a1.id) {
          return -1
        }
        if (this.question.answer === a2.id) {
          return 1
        }
        let d1 = new Date(a1.updated_at)
        let d2 = new Date(a2.updated_at)
        return (d1 < d2) ? 1 : -1
      },
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
    overflow-y: auto;
    overflow-x: hidden;
    padding: 5px;
    border-bottom: solid 1px #e4e4e4;
  }

  .questionAndAnswer.full-size {
    height: 98%;
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
    padding-left: 10px;
    text-align: left;
  }

  ul.answers-list {
    padding-left: 0;
  }
</style>
