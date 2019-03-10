<template>
  <div v-if="chatroom" id="chatroomusersview">
    <ul v-if="users_in_room" id="connected">
      <li v-for="u in users_in_room" :key="u.user_obj.username">
        <div>
          <span class="image-cropper"><img class="mdl-list__item-icon" v-bind:alt="u.user_obj.username"
                                           v-bind:src="u.user_obj.avatar_image"/></span>
          {{u.user_obj.username}} - Last action :
          {{u.updated_at | formatDate}}
        </div>

      </li>
    </ul>
  </div>
</template>

<script>
  import {authMixin} from '@/auth/authMixin.js'
  import axios from 'axios'

  export default {
    name: 'chatroomUsers',
    mixins: [authMixin],
    data () {
      return {
        users_in_room: []
      }
    },
    filters: {
      formatDate: function (value) {
        if (value) {
          let d = new Date(value)
          return d.toLocaleDateString() + ' ' + d.toLocaleTimeString()
        }
      }
    },
    computed: {
      chatroom: function () {
        let vm = this
        return vm.$root.chatrooms.filter(function (row) {
          return row.id === vm.$route.params.id
        })[0]
      },
      user: function () {
        return this.$root.user
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
              console.log(response.data.users)
              // vm.users = response.data.users
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
  #chatroomusersview {
    position: relative;
    top: 0;
    bottom: 0;
    margin-left: auto;
    margin-right: auto;
    background: #fff;
    height: 100%;
    width: 100%;
    max-width: 700px;
  }

  #connected {
    margin-top: 2px;
    font-size: 12px;
    line-height: 14px;
    width: auto;
    display: table;
    padding-left: 1vw;
  }

  #connected > li {
    width: auto;
    list-style-type: none;
    padding: 2px;
    margin-bottom: 2px;
    text-align: left;
    vertical-align: middle;
  }

  .image-cropper {
    padding: 5px;
    line-height: 5vh;
    background-color: rgba(88, 88, 88, 0.34);
  }

  #connected > li img {
    border-radius: 50%;
    border: solid 2px #fff;
    width: 5vh;
    height: 5vh;
  }
</style>
