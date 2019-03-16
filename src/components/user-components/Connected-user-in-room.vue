<template>
  <li class="user-in-a-room mdl-list__item mdl-list__item--three-line">

    <div class="mdl-list__item-primary-content">
      <span class="img" v-bind:style="'background-image: url('+userInRoom.user_obj.avatar_image+')'">
      </span>
      <span :alt="niceUserLabel" v-html="niceUserLabel">
      </span>
      <span class="mdl-list__item-text-body">{{$t('user.lastAction')}} {{userInRoom.updated_at | formatDate}}
      </span>
    </div>
  </li>
</template>

<script>
  require('material-design-lite')

  export default {
    name: 'connectedUserInRoom',
    props: ['userInRoom'],
    computed: {
      niceUserLabel: function () {
        if (this.userInRoom.user_obj.first_name) {
          return this.userInRoom.user_obj.first_name + ' ' + this.userInRoom.user_obj.last_name
        } else {
          return this.userInRoom.user_obj.username
        }
      }
    },
    filters: {
      formatDate: function (value) {
        if (value) {
          let d = new Date(value)
          return d.toLocaleDateString() + ' ' + d.toLocaleTimeString()
        }
      }
    }
  }
</script>

<style scoped>
  span.img {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    margin-right: 16px;
    background-size: cover;
    background-position: center center;
    float: left;
  }

  .user-in-a-room {
    border-bottom: solid 1px #e4e4e4;
  }
</style>
