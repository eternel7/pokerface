<template>
  <li class="answer">
    <qaItem v-bind:item="answer"
            v-bind:question="question"
            v-bind:user="user"
            v-bind:closable="false"
            v-bind:search="search"></qaItem>
    <hr/>
  </li>
</template>

<script>
  import qaItem from '@/components/sub-components/Q&A-item'
  import {authMixin} from '@/auth/authMixin.js'
  import {momentMixin} from '@/assets/momentMixin.js'

  require('material-design-lite')

  export default {
    name: 'answer-item',
    mixins: [authMixin, momentMixin],
    components: {qaItem},
    props: ['user', 'answer', 'search', 'question'],
    data: function () {
      return {
        comments: []
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .answer {
    list-style: none;
    padding-left: 0;
  }

  .answer hr {
    width: 95%;
    margin-top: 5px;
    margin-right: auto;
    margin-left: auto;
    margin-bottom: 5px;
  }
</style>
