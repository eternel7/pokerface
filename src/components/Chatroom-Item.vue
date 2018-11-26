<template>
  <li class="chatroom-item mdl-list__item mdl-list__item--three-line">
    <div class="mdl-list__item-primary-content">
      <router-link :to="'/chat/'+chatroom.id" class="mdl-list__item-secondary-action mdl-js-ripple-effect">
      <i class="material-icons mdl-list__item-avatar">person</i>
      <span>{{chatroom.user_label}}</span>
      <span class="mdl-list__item-text-body">
        {{chatroom.user_notepad}}
      </span>
      </router-link>
    </div>
    <div class="mdl-list__item-secondary-content">
      <router-link :to="'/chat/'+chatroom.id" class="mdl-list__item-secondary-action mdl-js-ripple-effect">
        <i class="tooltip material-icons">chat</i>
    </router-link>
    </div>
  </li>
</template>

<script>
  export default {
    name: 'chatroom-item',
    props: ['chatroom']
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .chatroom-item {
    text-align: left;
    background-color: #fff;
  }

  .mdl-list__item-text-body {
    border-bottom: #403838 1px;
    overflow: hidden;
    text-overflow: ellipsis;
    -o-text-overflow: ellipsis;
    -ms-text-overflow: ellipsis;
    display: block;
    display: -webkit-box;
    font-size: 1rem;
    -webkit-box-orient: vertical;
    margin-bottom: 0;
    -webkit-line-clamp: 2; /* number of lines to show */
    line-height: 16px; /* fallback */
    max-height: 32px; /* fallback */
  }

  li {
    color: #9e9e9e;
    border-bottom: solid 1px #e4e4e4;
  }

  a {
    color: #9e9e9e;
    text-decoration: none;
  }
</style>
