<template>
  <div class="chat">
    <h1>Chat with {{ $route.params.id }}</h1>
    <ul>
      <li>{{ msg }}</li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'chat',
  data () {
    return {
      msg: 'Welcome to Your Vue.js PWA'
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}

a {
  color: #35495E;
}
</style>
