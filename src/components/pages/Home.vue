<template>
  <div>
    <signIn v-if="isUnauthenticated"></signIn>
    <profile v-if="!isUnauthenticated"></profile>
  </div>
</template>

<script>
  import SignIn from '@/components/pages/Sign-in'

  require('material-design-lite')

  export default {
    name: 'home',
    components: {
      signIn: SignIn
    },
    data () {
      return {
        isUnauthenticated: true
      }
    }
  }
</script>
