<template>
  <div class="chatrooms">
    <h1>Chat with</h1>
    <ul>
      <chatroom-item
              v-for="chatroom in chatrooms"
              v-bind:key="chatroom.id"
              v-bind:chatroom="chatroom"
      ></chatroom-item>
    </ul>
  </div>
</template>

<script>
  import PageBase from '@/components/pages/Page'
  import ChatroomItem from '@/components/Chatroom-item'
  import {authMixin} from '@/auth/authMixin.js'
  import axios from 'axios'

  export default {
    name: 'chatrooms',
    extends: PageBase,
    mixins: [authMixin],
    components: {ChatroomItem},
    data () {
      return {
        chatrooms: [],
        displaySearch: true
      }
    },
    methods: {
      tryGetChatrooms (evt) {
        let vm = this
        vm.errors = []
        vm.$root.loading = true
        axios.get('/api/chatrooms/', vm.authHeader())
          .then(function (response) {
            vm.$root.loading = false
            // handle success
            if (response.data.chatrooms) {
              console.log(response.data.chatrooms)
              vm.chatrooms = response.data.chatrooms
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
          })
      }
    },
    created: function (e) {
      this.tryGetChatrooms(e)
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .chatrooms{
    margin-top: -60px;
  }
  h1, h2 {
    font-weight: normal;
    color: #fff;
  }

  ul {
    list-style-type: none;
    padding: 0;
  }
</style>
