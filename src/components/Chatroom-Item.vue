<template>
  <li class="chatroom-item">
    <router-link :to="'/chat/'+chatroom.msg">Start a chat</router-link>
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

  li {
    display: inline-block;
    margin: 0 10px;
    color: #fff;
  }

  a {
    color: #fff;
  }
</style>
