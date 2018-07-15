<template>
  <li class="chatroom-item">
    <router-link class="mdl-navigation__link" :to="'/chat/'+chatroom.msg">Start a chat</router-link>
  </li>
</template>

<script>
export default {
  name: 'chatroom-item',
  props: ['chatroom']
}
</script>
