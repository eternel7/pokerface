<template>
  <div id="message" class="messages" v-bind:class="{ 'right': msg.origin===1, 'left': msg.origin!==1,
            'a-question': msg.question}">
    <div class="img-and-bubble">
      <span v-if="msg.origin===1"
            class="mdl-list__item-avatar img"
            v-bind:style="'background-image: url('+user.avatar_image+')'">
      </span>
      <span v-else-if="msg.origin===0" alt="Room"
            class="mdl-list__item-avatar img"
            v-bind:style="'background-image: url('+chatroom.portrait+')'">
      </span>
      <span v-if="msg.origin.portrait" v-bind:title="msg.origin.username"
            class="mdl-list__item-avatar img"
            v-bind:style="'background-image: url('+msg.origin.portrait+')'">
      </span>
      <div :id="'badge_menu'+unique_id"
           v-bind:class="{ 'mdl-menu--bottom-right': msg.origin===1, 'mdl-menu--bottom-left': msg.origin!==1,
            'a-question': msg.question}">
        <div class="bubble">
          {{message}}
        </div>
        <div v-if="msg.origin===1" class="link mdl-badge mdl-badge--overlap badge-menu"
             v-bind:data-badge="badge_icon">
        </div>
        <ul class="mdl-menu mdl-js-menu mdl-js-ripple-effect"
            v-bind:class="{ 'mdl-menu--bottom-right': msg.origin===1, 'mdl-menu--bottom-left': msg.origin!==1,
            'a-question': msg.question}"
            :for="'badge_menu'+unique_id" :data-mdl-for="'badge_menu'+unique_id">
          <li v-for="action in badge_menu_actions" v-on:click="doAction(action.js, msg, action)" v-if="!action.post"
              :class="['mdl-menu__item','action_menu_' + action.labelId,
              {'mdl-menu__item--full-bleed-divider': action.separatorAfter, 'action_menu_question' : msg.question}]">
            <span>{{$t('badge_menu.action.' + action.labelId)}}</span>
          </li>
          <li v-if="!msg.question && action.post" v-for="action in badge_menu_actions"
              v-on:click="doAction(action.js, msg, action)"
              class="mdl-menu__item action_menu_isAnAction" v-bind:class="{'mdl-menu__item--full-bleed-divider': action.separatorAfter,
              'selected-answer' : action.post.post_id===msg.answer_to}">
            <span :title="action.post.body">{{$t('badge_menu.action.' + action.labelId)}} {{action.post.post_id}}</span>
          </li>
        </ul>
      </div>
    </div>
    <div class="user_quick_response" v-if="msg.message && msg.message.send_back">
      <span v-if="msg.message.send_back.done"
            @click="sendBack('!')">
        {{$t('post.send_back.thanks_for_reply')}}
      </span>
      <button v-if="msg.message.send_back.yes" class="yes mdl-button mdl-js-button mdl-button--raised mdl-button--colored"
              @click="sendBack(true)">
        {{$t('post.send_back.Yes')}}
      </button>
      <button v-if="msg.message.send_back.no" class="no mdl-button mdl-js-button mdl-button--raised mdl-button--colored"
              @click="sendBack(false)">
        {{$t('post.send_back.No')}}
      </button>
      <div v-if="msg.message.send_back.input" class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
        <input class="mdl-textfield__input" type="text" id="send_back_input">
        <label class="mdl-textfield__label" for="send_back_input">{{$t('post.send_back_placeholder.' +
          msg.message.send_back.input.placeholder)}}</label>
      </div>
      <button v-if="msg.message.send_back.input" class="send-back-input mdl-button mdl-js-button mdl-button--raised mdl-button--colored"
              @click="sendBack('input')">
        {{$t('post.send_back.input.Button')}}
      </button>
      <div v-if="msg.message.send_back.textarea" class=" mdl-textfield mdl-js-textfield">
        <textarea class="mdl-textfield__input" type="text" rows="3" id="send_back_textarea"></textarea>
        <label class="mdl-textfield__label" for="send_back_textarea">{{$t('post.send_back_placeholder.' +
          msg.message.send_back.textarea.placeholder)}}</label>
      </div>
      <button v-if="msg.message.send_back.textarea"
              class="send-back-textarea mdl-button mdl-js-button mdl-button--raised mdl-button--colored"
              @click="sendBack('textarea')">
        {{$t('post.send_back.textarea.Button')}}
      </button>
    </div>
    <div v-if="!msg.origin.portrait" class="time">
      {{tillNowDate}}
    </div>
    <div v-else class="time">{{tillNowDate}} - {{msg.origin.username}}</div>
  </div>
</template>

<script>
  import {authMixin} from '@/auth/authMixin.js'
  import {momentMixin} from '@/assets/momentMixin.js'
  import DataUtils from '@/assets/data-utils.js'
  import moment from 'moment'

  require('material-design-lite')

  function hashCode (str) {
    let hash = 0
    let i
    let chr
    if (str.length === 0) return hash
    for (i = 0; i < str.length; i++) {
      chr = str.charCodeAt(i)
      hash = ((hash << 5) - hash) + chr
      hash |= 0 // Convert to 32bit integer
    }
    return hash
  }

  export default {
    name: 'msg-item',
    mixins: [authMixin, momentMixin],
    props: ['msg', 'user', 'chatroom', 'questions', 'chats', 'now'],
    data: function () {
      return {update_version: 0}
    },
    computed: {
      badge_icon: function () {
        if (this.msg.question) {
          return this.msg.post_id || '...'
        } else {
          if (this.msg.message.endsWith('?')) {
            return '?'
          }
          return '⋮'
        }
      },
      unique_id: function () {
        return (this.msg.post_id) ? this.msg.post_id : 'loc_' + hashCode(this.msg.message) + hashCode(this.msg.date.getTime().toString())
      },
      type: function () {
        if (this.msg.question) {
          return 'question'
        }
        if (this.msg.answer) {
          return 'answered_question'
        }
        if (this.msg.question) {
          return 'answer'
        }
        return 'message'
      },
      badge_menu_actions: function () {
        let vm = this
        let entries = [{
          'js': 'editMsg',
          'labelId': 'editMsg'
        }, {
          'js': 'changeQuestion',
          'labelId': 'isAQuestion',
          'separatorAfter': true
        }]
        if (vm.chats instanceof Array && vm.chats.length > 0) {
          let qEntries = []
          for (const q of vm.chats) {
            if (q.question === true) {
              qEntries.push({
                'js': 'AnswerTo',
                'labelId': 'AnswerTo',
                'post': q
              })
            }
          }
          qEntries.sort((a, b) => (a.post.id > b.post.id) ? 1 : (b.post.id > a.post.id) ? -1 : 0)
          for (let action in qEntries) {
            entries.push(qEntries[action])
          }
        }
        return entries
      },
      tillNowDate: function () {
        let vm = this
        let now = new Date(vm.now)
        let d = new Date(vm.msg.date)
        if (Math.abs(now.getTime() - d.getTime()) < 1000 * 60 * 60) {
          return moment(d).fromNow().toLowerCase() + ' - ' + d.toLocaleTimeString()
        } else {
          return moment(d).calendar().toLowerCase()
        }
      },
      message: function () {
        if (this.msg.message instanceof Object) {
          let info = Object.assign({}, this.msg.message)
          delete info.msg
          return this.$root.$t(this.msg.message.msg, info)
        }
        return this.msg.message
      }
    },
    methods: {
      updatemdl: function () {
        // eslint-disable-next-line
        componentHandler.upgradeDom()
        // eslint-disable-next-line
        componentHandler.upgradeAllRegistered()
      },
      couldBeAQuestion: function (msg) {
        return !!(!msg.question && msg.message.endsWith('?'))
      },
      doAction: function (actionName, msg, action) {
        let vm = this
        if (actionName === 'changeQuestion') {
          vm.updateQuestion(msg, action)
        } else if (actionName === 'AnswerTo') {
          vm.setAnswer(msg, action.post)
        }
      },
      sendBack: function (answer) {
        let vm = this
        console.log(answer)
        if (answer !== '!') {
          let sendBackAnswer = {
            client_id: vm.unique_id,
            answer: answer,
            msg: vm.msg.message
          }
          DataUtils.sendBackAnswerToBot(vm, sendBackAnswer)
        }
        // hide send back button on client side
        vm.msg.message.send_back = null
      },
      updateQuestion: function (msg) {
        let vm = this
        msg.question = !msg.question
        if (msg.question === true || msg.post_id) {
          DataUtils.updateQuestionState(vm, msg)
        }
      },
      setAnswer: function (answer, question) {
        let vm = this
        DataUtils.setAnswer(vm, answer, question)
        vm.$nextTick(vm.updatemdl())
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
  .badge-menu:after {
    bottom: 0;
    color: #365dad;
    background-color: #dbe3f9;
  }

  .selected-answer .action_menu_question.action_menu_isAQuestion {
    background-color: #69f0ae;
  }

  .selected-answer:hover {
    background-color: #2bbd7e;
  }

  .user_quick_response {
    clear: both;
    text-align: left;
    max-width: 60%;
    margin-bottom: 0.5vh;
    margin-top: 0.5vh;
  }

  #message {
    display: flex;
    flex-direction: column;
    padding: 0 0 5px 58px;
    clear: both;
    text-align: left;
    max-width: 60%;
    margin-top: 1vh;
  }

  #message.right {
    float: right;
    padding: 0 58px 5px 0;
    margin-right: -19px;
    margin-left: 19px;
  }

  #message div.img-and-bubble {
    position: relative;
  }

  #message .img {
    position: absolute;
    bottom: 0;
    left: -45px;
    margin-top: 12px;
    background-size: cover;
    background-position: center center;
  }

  #message.right .img {
    right: -45px;
    left: auto;
  }

  #message .bubble {
    position: relative;
    float: left;
    background: #dbe3f9;
    font-size: 13px;
    font-weight: 400;
    padding: 8px 8px;
    border-radius: 5px 5px 5px 0px;
    color: #365dad;
    width: max-content;
    word-break: break-word;
    max-width: 100%; /* do not oversize message width*/
  }

  #message.right .bubble {
    float: right;
    border-radius: 5px 5px 0px 5px;
  }

  #message .bubble:after {
    content: '';
    position: absolute;
    top: 100%;
    width: 0;
    height: 0;
    border: 7px solid transparent;
    border-bottom: 0;
    margin-top: -7px;
  }

  #message.left .bubble:after {
    left: 0;
    border-right-color: #dbe3f9;
    border-left: 0;
    margin-left: -7px;
  }

  #message.right .bubble:after {
    right: 0;
    border-left-color: #dbe3f9;
    border-right: 0;
    margin-right: -7px;
  }

  #message > .time {
    clear: both;
    color: #8eace8;
    font-size: 0.8em;
    position: relative;
    bottom: 0;
    margin-bottom: 0.5em;
    width: max-content;
  }

  #message.left > .time {
    margin-left: 0;
    margin-right: auto;
  }

  #message.right > .time {
    margin-left: auto;
    margin-right: 0;
  }
</style>
