<template>
  <div class="chatrooms">
    <transition name="fade-slide-up" mode="out-in">
      <ul v-if="chatrooms.length">
        <transition-group name="shrink">
          <li is="chatroom-item"
              v-for="(chatroom, index) in chatrooms"
              v-bind:key="chatroom.id"
              v-bind:index="index"
              v-bind:chatroom="chatroom"
          ></li>
        </transition-group>
      </ul>
      <h4 v-else>Looking for a chatroom...</h4>
    </transition>
  </div>
</template>

<script>
  import PageBase from '@/components/pages/Page'
  import ChatroomItem from '@/components/sub-components/Chatroom-item'
  import {authMixin} from '@/auth/authMixin.js'
  import axios from 'axios'

  export default {
    name: 'chatrooms',
    extends: PageBase,
    props: ['search'],
    mixins: [authMixin],
    components: {ChatroomItem},
    data () {
      return {
        displaySearch: true
      }
    },
    computed: {
      chatrooms: function () {
        let vm = this
        if (typeof vm.search === 'string' && vm.search !== '') {
          return vm.$root.chatrooms.filter(function (row) {
            return Object.keys(row).some(function (key) {
              return String(row[key]).toLowerCase().indexOf(vm.search) > -1
            })
          })
        } else {
          return vm.$root.chatrooms
        }
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
              vm.$root.chatrooms = response.data.chatrooms
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

  h1, h2, h3, h4 {
    font-weight: normal;
    color: #fff;
  }

  ul {
    list-style-type: none;
    padding: 0;
  }

  .fade-slide-up-enter-active, .fade-slide-up-leave-active {
    transition: all 0.5s ease;
  }

  .fade-slide-up-enter, .fade-slide-up-leave-to {
    transform: translateY(-40px);
    opacity: 0;
  }

  .shrink, .shrink-move, .shrink-enter-active, .shrink-leave-active {
    transition: all 0.5s ease;
    -webkit-transform-origin: top;
    -moz-transform-origin: top;
    -o-transform-origin: top;
    transform-origin: top;
  }

  .shrink-enter, .shrink-leave-to {
    -webkit-transform: scaleY(0);
    -ms-transform: scaleY(0);
    transform: scaleY(0);
  }

  .shrink-leave, .shrink-enter-to {
    -webkit-transform: scaleY(1);
    -ms-transform: scaleY(1);
    transform: scaleY(1);
  }
</style>
