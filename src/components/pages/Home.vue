<template>
  <div>
    <signIn v-if="!$root.authenticated"></signIn>
    <chatrooms v-if="$root.authenticated"></chatrooms>
  </div>
</template>

<script>
  import SignIn from '@/components/pages/Sign-in'
  import Profile from '@/components/pages/Profile'
  import Chatrooms from '@/components/pages/Chatrooms'

  require('material-design-lite')

  export default {
    name: 'home',
    components: {
      signIn: SignIn,
      profile: Profile,
      chatrooms: Chatrooms
    }
  }
</script>
