<template>
  <li class="question mdl-list__item mdl-list__item--three-line">
    <span class="mdl-list__item-primary-content">
      <span class="mdl-list__item-avatar img who" :title="question.owner.username"
            v-bind:style="'background-image: url('+question.owner.avatar_image+')'">
      </span>
      <span class="what" :title="question.body" v-html="smallMsg">
      </span>
      <span class="mdl-list__item-text-body when">
        <span v-if='question.last_editor' :title="question.updated_at">{{$t('post.updated')}} {{update_date}}</span>
        <span v-else :title="question.created_at">{{$t('post.created')}} {{creation_date}}</span>
        <span class="last_editor">{{(question.last_editor) ? question.last_editor.username : question.owner.username}}</span>
      </span>
    </span>
    <span class="mdl-list__item-secondary-content answers">
      <span :title="$t('post.proposed_answers')">
        <table>
          <tr><td class="answers-count title">{{question.answers_count}}</td></tr>
          <tr><td class="answers-count count">{{$t('post.answers')}}</td></tr>
        </table>
      </span>
  </span>
  </li>
</template>

<script>
  import {authMixin} from '@/auth/authMixin.js'
  import axios from 'axios'
  import moment from 'moment'

  require('material-design-lite')

  export default {
    name: 'question-item',
    mixins: [authMixin],
    props: ['user', 'chatroom', 'question'],
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
        return moment(new Date(this.question.created_at)).fromNow()
      },
      update_date: function () {
        return moment(new Date(this.question.updated_at)).fromNow()
      },
      smallMsg: function () {
        return (this.question.body.length > 100) ? this.question.body.substring(0, 100) + '...' : this.question.body
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
    margin-bottom: 100%
  }

  .question {
    border-bottom: solid 1px #e4e4e4;
  }

  .what {
    font-size: small;
  }

  .when {
    font-size: x-small;
  }

  .answers-count {
    text-align: center;
    font-size: small;
  }
</style>
