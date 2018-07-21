<template>
  <div>
    <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
      <input class="mdl-textfield__input" id="email" required autofocus
             v-model.trim="sync_email"/>
      <label class="mdl-textfield__label" for="email">Email</label>
    </div>
    <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
      <input class="mdl-textfield__input" type="password" id="password" required
             v-model.trim="sync_password"/>
      <label class="mdl-textfield__label" for="password">Password</label>
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
    }
  }
</script>
<style scoped>

  #meter {
    background: #1a1a1a;
    color: white;
    height: 1em;
    line-height: 1em;
    position: absolute;
    text-align: center;
    vertical-align: center;
    clear: none;
    float: left;
    top: calc(50% - 0.5em);
    left: calc(100% - 1.5em);
    width: 1em;
  }

  /* Webkit based browsers */
  #meter[value="1"] {
    background: red;
    color: white;
  }

  #meter[value="2"] {
    background: #fe9718;
    color: black;
  }

  #meter[value="3"] {
    background: #5f8ef2;
    color: white;
  }

  #meter[value="4"] {
    background: #33bf13;
    color: white;
  }

  #meter[value="5"] {
    background: #5be030;
    color: #1a1a1a;
  }
</style>
