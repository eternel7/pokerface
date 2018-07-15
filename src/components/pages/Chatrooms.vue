<template>
  <div class="chatrooms">
    <h1>Chat with</h1>
    <ul>
      <chatroom-item
        v-for="chatroom in chatrooms"
        v-bind:key="chatroom.id"
        v-bind:chatroom="chatroom"
      ></chatroom-item>
    </ul>
  </div>
</template>

<script>
  import ChatroomItem from '@/components/Chatroom-item'
  export default {
    name: 'chatrooms',
    components: {ChatroomItem},
    data () {
      return {
        chatrooms: [{msg: '1'}, {msg: '2'}, {msg: '3'}]
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  h1, h2 {
    font-weight: normal;
  }
</style>
