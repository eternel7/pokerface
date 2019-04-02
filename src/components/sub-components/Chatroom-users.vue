<template>
  <div v-if="chatroom" id="chatroomview">
    <ul v-if="sortedUsersInRoom" id="connected" class="mdl-list list">
      <li is="ConnectedUserInRoom" v-for="u in sortedUsersInRoom" :key="u.user_obj.username" v-bind:userInRoom="u">
      </li>
    </ul>
  </div>
</template>

<script>
  import ConnectedUserInRoom from '@/components/user-components/Connected-user-in-room'
  import {authMixin} from '@/auth/authMixin.js'
  import DataUtils from '@/assets/data-utils.js'
  import SortUtils from '@/assets/sort-utils.js'

  export default {
    name: 'chatroomUsers',
    mixins: [authMixin],
    components: {ConnectedUserInRoom},
    props: ['chatroom'],
    computed: {
      sortedUsersInRoom: function () {
        if (this.$root.store.users_in_room) {
          let now = new Date()
          let hourAgo = new Date(now.getTime() - (1000 * 60 * 60))
          return this.$root.store.users_in_room.filter(function (row) {
            let lastAction = new Date(row.updated_at)
            return lastAction > hourAgo
          }).sort(SortUtils.onUpdated_at)
        } else {
          return []
        }
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
        DataUtils.refreshUsers(this, true)
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
    height: calc(92vh - 50px);
    width: 100%;
    max-width: 700px;
  }

  .list {
    position: relative;
    height: 100%;
    margin: 0;
    width: 98%;
    padding: 0 1% 0 1%;
    overflow-y: scroll;
    overflow-x: hidden;
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
