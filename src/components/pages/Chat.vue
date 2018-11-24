<template>
  <div class="chat">
    <h1>Chat with {{ $route.params.id }}</h1>
    <ul>
      <li>{{ msg }}</li>
    </ul>
  </div>
</template>

<script>
  import PageBase from '@/components/pages/Page'

  export default {
    name: 'chat',
    extends: PageBase,
    data () {
      return {
        msg: Math.random(10).toString(24) + ' Welcome to Your Vue.js PWA ' + Math.random(10).toString(24),
        displaySearch: true,
        displayBack: true
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  h1, h2 {
    font-weight: normal;
    color: #fff;
  }

  ul {
    list-style-type: none;
    padding: 0;
  }

  li {
    display: inline-block;
    margin: 0 10px;
    color: #fff;
  }

  a {
    color: #fff;
  }
</style>
