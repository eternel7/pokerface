<template>
  <div>
    <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label"
         v-bind:class="{'is-dirty' : (sync_email) ? true : false}">
      <input class="mdl-textfield__input" type="text" id="email" ref="email" required autofocus
             v-model.trim="sync_email" v-on:keyup.enter="emitEnterKeyUp"/>
      <label class="mdl-textfield__label" for="email">{{$t('user.Email')}}</label>
    </div>
    <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label"
         v-bind:class="{'is-dirty' : (sync_password) ? true : false}">
      <input class="mdl-textfield__input" type="password" id="password" required
             v-model.trim="sync_password" v-on:keyup.enter="emitEnterKeyUp"/>
      <label class="mdl-textfield__label" for="password">{{$t('user.Password')}}</label>
      <pwdMeter v-bind:pwd="sync_password"></pwdMeter>
    </div>
  </div>
</template>

<script>
  import PwdMeter from '@/components/pwd-components/Pwd-helper'

  export default {
    props: {
      'email': '',
      'password': '',
      'userTitle': {
        default: 'user.Login',
        type: String
      }
    },
    name: 'usermainfields',
    components: {
      pwdMeter: PwdMeter
    },
    computed: {
      sync_email: {
        get () {
          return this.email
        },
        set (val) {
          this.$emit('update:email', val)
        }
      },
      sync_password: {
        get () {
          return this.password
        },
        set (val) {
          this.$emit('update:password', val)
        }
      }
    },
    methods: {
      emitEnterKeyUp: function (e) {
        this.$emit('enterKeyUp')
      }
    },
    mounted () {
      this.$refs.email.focus()
    }
  }
</script>
<style scoped>
</style>
