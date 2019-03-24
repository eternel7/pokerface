<template>
  <li class="user-in-a-room mdl-list__item mdl-list__item--three-line">
    <span class="mdl-list__item-primary-content">
      <span class="mdl-list__item-avatar img" v-bind:style="'background-image: url('+userInRoom.user_obj.avatar_image+')'">
      </span>
      <span :title="niceUserLabel" v-html="niceUserLabel">
      </span>
      <span class="mdl-list__item-text-body" :title="userInRoom.updated_at">
        {{$t('user.lastAction')}} - {{userInRoom.updated_at | formatTime}}
      </span>
    </span>
  </li>
</template>

<script>
  import {momentMixin} from '@/assets/momentMixin.js'
  require('material-design-lite')

  export default {
    name: 'connectedUserInRoom',
    mixins: [momentMixin],
    props: ['userInRoom'],
    computed: {
      niceUserLabel: function () {
        if (this.userInRoom.user_obj.first_name) {
          return this.userInRoom.user_obj.first_name + ' ' + this.userInRoom.user_obj.last_name
        } else {
          return this.userInRoom.user_obj.username
        }
      }
    }
  }
</script>

<style scoped>
  span.img {
    background-size: cover;
    background-position: center center;
  }

  .user-in-a-room {
    border-bottom: solid 1px #e4e4e4;
  }
</style>
