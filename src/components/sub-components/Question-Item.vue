<template>
  <li class="question mdl-list__item mdl-list__item--three-line">
    <span class="mdl-list__item-primary-content">
      <span class="mdl-list__item-avatar img who" :title="question.owner.username"
            v-bind:style="'background-image: url('+question.owner.avatar_image+')'">
      </span>
      <p class="what block-with-text" :title="bodyH" v-html="bodyH">
      </p>
      <span class="mdl-list__item-text-body when">
        <span v-if='question.last_editor' :title="question.updated_at">
          {{$t('post.updated')}} {{update_date | niceDate}}
        </span>
        <span v-else :title="question.created_at">
          {{$t('post.created')}} {{creation_date | niceDate}}
        </span>
        <span class="last_editor"> - {{(question.last_editor) ? question.last_editor.username : question.owner.username}}</span>
      </span>
    </span>
    <span class="mdl-list__item-secondary-content answers">
      <span :title="$t('post.proposed_answers')">
        <table>
          <tr><td class="answers-count count">{{question.answers_count}}</td></tr>
          <tr><td class="answers-count title">{{$t('post.answers')}}</td></tr>
        </table>
      </span>
  </span>
  </li>
</template>

<script>
  import Search from '@/assets/search-utils.js'
  import {authMixin} from '@/auth/authMixin.js'
  import {momentMixin} from '@/assets/momentMixin.js'
  import axios from 'axios'
  import moment from 'moment'

  require('material-design-lite')

  export default {
    name: 'question-item',
    mixins: [authMixin, momentMixin],
    props: ['user', 'chatroom', 'question', 'search'],
    data: function () {
      return {update_version: 0}
    },
    created () {
      moment.locale(this.$i18n.locale)
    },
    computed: {
      type: function () {
        if (this.question.type === 1) {
          return 'question'
        }
        if (this.question.answer) {
          return 'answered_question'
        }
        if (this.question.question) {
          return 'answer'
        }
        return 'message'
      },
      creation_date: function () {
        return new Date(this.question.created_at)
      },
      update_date: function () {
        return new Date(this.question.updated_at)
      },
      bodyH: function () {
        return Search.highlight(this.question.body, this.search)
      }
    },
    methods: {
      updatemdl: function () {
        // eslint-disable-next-line
        componentHandler.upgradeDom()
        // eslint-disable-next-line
        componentHandler.upgradeAllRegistered()
      },
      doAction: function (actionName, msg, action) {
        let vm = this
        if (actionName === 'changeQuestion') {
          vm.updateQuestion(msg, action)
        } else if (actionName === 'AnswerTo') {
          vm.setAnswer(msg, action.post)
        }
      },
      updateQuestion: function (msg) {
        let vm = this
        msg.question = !msg.question
        if (msg.question === true || msg.post_id) {
          msg.room = vm.$route.params.id
          axios.post('/api/chatroomquestion/', msg, vm.authHeader())
            .then(function (response) {
              // handle success
              vm.$root.loading = false
              if (response.data.post) {
                if (msg.question) {
                  vm.$root.showSnackbar(vm.$i18n.t('post.savedAsQuestion'))
                } else {
                  vm.$root.showSnackbar(vm.$i18n.t('post.notAQuestionAnymore'))
                }
                if (response.data.questions && vm.$root.questions instanceof Object) {
                  vm.$set(vm.$root.questions, vm.$route.params.id, response.data.questions)
                }
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
              vm.$nextTick(vm.updatemdl())
            })
        }
      },
      setAnswer: function (answer, question) {
        let vm = this
        answer.room = vm.$route.params.id
        let QandA = {
          question: question,
          answer: answer,
          room: vm.$route.params.id
        }
        axios.post('/api/chatroomsetanswer/', QandA, vm.authHeader())
          .then(function (response) {
            // handle success
            vm.$root.loading = false
            console.log(response.data)
            if (response.data.question && response.data.answer) {
              vm.$set(answer, 'answer_to', response.data.answer.answer_to)
              vm.$set(answer, 'type', response.data.answer.type)
              if (response.data.question.answer) {
                vm.$root.showSnackbar(vm.$i18n.t('post.questionAnswered'))
              } else {
                vm.$root.showSnackbar(vm.$i18n.t('post.answerRejected'))
              }
              if (response.data.questions && vm.$root.questions instanceof Object) {
                vm.$set(vm.$root.questions, vm.$route.params.id, response.data.questions)
              }
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
            vm.$nextTick(vm.updatemdl())
          })
      }
    },
    mounted: function () {
      let vm = this
      vm.updatemdl()
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  span.img {
    background-size: cover;
    background-position: center center;
    margin-bottom: 100%;
  }

  .question {
    border-bottom: solid 1px #e4e4e4;
  }

  .what {
    font-size: medium;
  }

  /* styles for '...' */
  .block-with-text {
    /* hide text if it more than N lines  */
    overflow: hidden;
    /* for set '...' in absolute position */
    position: relative;
    /* use this value to count block height */
    line-height: 1.2em;
    /* max-height = line-height (1.2) * lines max number (2) */
    max-height: 2.4em;
    /* fix problem when last visible word doesn't adjoin right side  */
    text-align: justify;
    /* place for '...' */
    margin-right: -1em;
    padding-right: 1em;
    margin-top: 0;
    margin-bottom: 0;
  }

  /* create the ... */
  .block-with-text:before {
    /* points in the end */
    content: '...';
    /* absolute position */
    position: absolute;
    /* set position to right bottom corner of block */
    right: 0;
    bottom: 0;
  }

  /* hide ... if we have text, which is less than or equal to max lines */
  .block-with-text:after {
    /* points in the end */
    content: '';
    /* absolute position */
    position: absolute;
    /* set position to right bottom corner of text */
    right: 0;
    /* set width and height */
    width: 1em;
    height: 1em;
    margin-top: 0.2em;
    /* bg color = bg color under block */
    background: white;
  }

  .when {
    font-size: 12px;
    line-height: 14px;
    margin: 0;
    padding: 0;
  }

  .answers-count {
    text-align: center;
  }

  .answers-count.title {
    font-size: 12px;
  }

  .answers-count.count {
    font-size: 14px;
  }

</style>
