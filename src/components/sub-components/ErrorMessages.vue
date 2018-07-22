<template>
  <ul v-if="errors && errors.length" class="errorList">
    <li v-for="error of errors">
      {{$t(error.message)}}
    </li>
  </ul>
</template>
<script>
  export default {
    props: {
      errors: Array
    },
    name: 'errorMessages'
  }
</script>
<style>
  .errorList {
    margin: 1em;
    padding: 0;
  }

  .errorList li {
    list-style: none;
    margin: 0;
    padding: 0;
    color: #f44336;
  }
</style>
