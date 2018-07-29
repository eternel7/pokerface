<template>
  <div>
    <signIn v-if="!$root.authenticated"></signIn>
    <profile v-if="$root.authenticated"></profile>
  </div>
</template>

<script>
  import SignIn from '@/components/pages/Sign-in'
  import Profile from '@/components/pages/Profile'

  require('material-design-lite')

  export default {
    name: 'home',
    components: {
      signIn: SignIn,
      profile: Profile
    }
  }
</script>
