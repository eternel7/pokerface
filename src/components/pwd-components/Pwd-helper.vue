<template>
      <span v-bind:title="$t('password.meter')" class="pwdMeter" v-bind:value="valuePasswordStrength">{{textPassword}}</span>
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
    name: 'Pwdhelper',
    props: {
      pwd: {
        type: String
      }
    },
    data () {
      return {
        valuePasswordStrength: 0,
        textPassword: ''
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
          vm.textPassword = (strToIdNum(this.pwd) % 36).toString(36)
        } else {
          vm.textPassword = ''
        }
      }
    },
    watch: {
      pwd: function () {
        this.testPasswordStrength(this.pwd)
      }
    }
  }
</script>

<style scoped>
  .pwdMeter {
    border-radius: 50%;
    font-size: 0.8em;
    width: 1.5em;
    height: 1.5em;
    line-height: 1.5em;
    padding: 0.2em;
    text-align: center;
    vertical-align: middle;
    clear: none;
    position: absolute;
    top: calc(50% - 1em);
    left: calc(100% - 2em);
    display: -webkit-flex;
    display: -ms-flexbox;
    display: flex;
    -webkit-flex-direction: row;
    -ms-flex-direction: row;
    flex-direction: row;
    -webkit-flex-wrap: wrap;
    -ms-flex-wrap: wrap;
    flex-wrap: wrap;
    -webkit-justify-content: center;
    -ms-flex-pack: center;
    justify-content: center;
    -webkit-align-content: center;
    -ms-flex-line-pack: center;
    align-content: center;
    -webkit-align-items: center;
    -ms-flex-align: center;
    align-items: center;
  }

  /* Webkit based browsers */
  .pwdMeter[value="0"] {
    background: #f44336;
    color: white;
    font-style: italic;
    font-weight: bold;
  }

  .pwdMeter[value="1"] {
    background: #FF9800;
    color: #ffffff;
    font-style: italic;
    font-weight: bold;
  }

  .pwdMeter[value="2"] {
    background: #03A9F4;
    color: white;
    font-weight: bold;
  }

  .pwdMeter[value="3"] {
    background: #4CAF50;
    color: white;
    font-weight: bold;
  }

  .pwdMeter[value="4"] {
    background: #76FF03;
    color: #959595;
    font-weight: bold;
  }
</style>
