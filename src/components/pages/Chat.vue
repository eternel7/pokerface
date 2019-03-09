<template>
  <div id="chatroomview">
    <div class="mdl-tabs mdl-js-tabs mdl-js-ripple-effect is-upgraded">
      <div class="mdl-tabs__tab-bar">
        <div v-for="tab in tabs" class="mdl-tabs__tab link"
             v-bind:href="tab.id" v-bind:id="'chat_tab_'+tab.id" v-on:click="tabActive=tab.id"
             v-bind:class="{'is-active' : (tab.id===tabActive)}">
          <i class="material-icons">
            {{tab.icon}}
          </i><span>{{$t('chat.' + tab.Title)}}</span>
        </div>
        <div id="close" v-on:click="backHome">
          <i class="material-icons">close</i>
        </div>
      </div>
      <div class="mdl-tabs__panel is-active" id="0" v-if="tabActive==='0'">
        <ChatBox></ChatBox>
      </div>
      <div class="mdl-tabs__panel is-active" id="1" v-if="tabActive==='1'">
      </div>
      <div class="mdl-tabs__panel is-active" id="2" v-if="tabActive==='2'">
        <ChatBox></ChatBox>
      </div>
      <div class="mdl-tabs__panel is-active" id="3" v-if="tabActive==='3'">
      </div>
    </div>
  </div>
</template>

<script>
  import PageBase from '@/components/pages/Page'
  import ChatBox from '@/components/sub-components/Chat-box'
  import {authMixin} from '@/auth/authMixin.js'

  export default {
    name: 'chat',
    extends: PageBase,
    mixins: [authMixin],
    components: {ChatBox},
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
          },
          {
            id: '5',
            Title: 'TabSpace',
            icon: ''
          }
        ],
        sessionStarted: false,
        displaySearch: true,
        displayBack: true,
        displayHeader: false,
        tabActive: '0',
        message: '',
        errors: [],
        updateNeeded: 'noNeed',
        loaded: false
      }
    },
    methods: {
      backHome: function () {
        this.$router.push({name: 'Home'})
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->


<style scoped>
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

  .mdl-tabs__panel {
    height: calc(100% - 49px);
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
    top: 11px;
    right: 14px;
    width: 24px;
    height: 24px;
    cursor: pointer;
    z-index: 2;
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
</style>
