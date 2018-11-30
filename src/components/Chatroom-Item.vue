<template>
  <li class="chatroom-item mdl-list__item mdl-list__item--three-line"
      v-on:click="gotoChat(index)">
    <div class="mdl-list__item-primary-content">
      <i class="material-icons mdl-list__item-avatar">person</i>
      <span>{{chatroom.user_label}}</span>
      <span class="mdl-list__item-text-body">
        {{chatroom.user_notepad}}
      </span>
    </div>
    <div class="mdl-list__item-secondary-content">
      <i class="tooltip material-icons">chat</i>
    </div>
    <router-link :to="'/chat/'+chatroom.id" class="mdl-list__item-secondary-action mdl-js-ripple-effect">
    </router-link>
  </li>
</template>

<script>
  export default {
    name: 'chatroom-item',
    props: ['chatroom', 'index'],
    methods: {
      gotoChat: function (index) {
        this.$router.push({name: 'Chat', params: {id: index}})
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .chatroom-item {
    text-align: left;
    background-color: #fff;
  }

  .chatroom-item:hover {
    background-color: #eeeeee;
    cursor: pointer;
    cursor: hand;
  }

  li {
    border-bottom: solid 1px #e4e4e4;
  }

  li > div > i {
    color: rgba(0, 0, 0, .54);
  }

  a {
    color: rgba(0, 0, 0, .54);
    text-decoration: none;
  }
</style>
