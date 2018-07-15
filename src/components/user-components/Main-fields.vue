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
      <div v-if="showPasswordStrength" id="meter" v-bind:value="valuePasswordStrength">{{textPassword}}</div>
    </div>
  </div>
</template>

<script>
  import zxcvbn from 'zxcvbn'

  function strToIdNum (str) {
    let n = 0
    for (let st of str) {
      n += st.charCodeAt()
    }
    return n
  }
  export default {
    props: {
      'email': '',
      'password': '',
      'userTitle': {
        default: 'user.Login',
        type: String
      },
      showPasswordStrength: {
        default: true,
        type: Boolean
      }
    },
    name: 'usermainfields',
    data () {
      return {
        valuePasswordStrength: 0,
        textPassword: ''
      }
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
          this.testPasswordStrength(val)
        }
      }
    },
    methods: {
      testPasswordStrength (val) {
        let vm = this
        let result = zxcvbn(val)

        // Update the password strength meter
        vm.valuePasswordStrength = result.score

        // Update the text indicator
        if (val !== '') {
          vm.textPassword = (strToIdNum(this.sync_password) % 36).toString(36)
        } else {
          vm.textPassword = ''
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
