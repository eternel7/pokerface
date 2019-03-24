<template>
  <div v-if="chatroom" id="chatroomview">
    <ul v-if="users_in_room" id="connected" class="mdl-list list">
      <li is="ConnectedUserInRoom" v-for="u in users_in_room" :key="u.user_obj.username" v-bind:userInRoom="u">
      </li>
    </ul>
  </div>
</template>

<script>
  import ConnectedUserInRoom from '@/components/user-components/Connected-user-in-room'
  import {authMixin} from '@/auth/authMixin.js'
  import axios from 'axios'

  export default {
    name: 'chatroomUsers',
    mixins: [authMixin],
    components: {ConnectedUserInRoom},
    props: ['chatroom'],
    data () {
      return {
        users_in_room: []
      }
    },
    created () {
      if (!this.chatroom || this.chatroom.length < 1) {
        this.$router.push({name: 'Home'})
      } else {
        let vm = this
        vm.tryGetChatroomUsers()
      }
    },
    methods: {
      tryGetChatroomUsers (evt) {
        let vm = this
        vm.errors = []
        vm.$root.loading = true
        let roomId = vm.$route.params.id
        axios.get('/api/chatroomusers/' + roomId, vm.authHeader())
          .then(function (response) {
            vm.$root.loading = false
            // handle success
            if (response.data.users) {
              vm.$set(vm, 'users_in_room', response.data.users)
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
    height: 92%;
    width: 100%;
    max-width: 700px;
  }

  .list {
    margin: 0;
    width: 99%;
    padding-left: 1%;
    position: relative;
    height: calc(100% - 15px);
    overflow-y: scroll;
    overflow-x: hidden;
    padding-bottom: 5px;
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

</style>
