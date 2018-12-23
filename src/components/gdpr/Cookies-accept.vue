<template>
  <div v-if="visible" id="cookieConsent">
    <button id="closeCookieConsent"
            class="mdl-button mdl-button--raised mdl-button--colored mdl-color-text--white"
            v-on:click.prevent="accept">x
    </button>
    <div>
      <h6>Notice</h6>
      <p>This site uses cookies. By continuing to use this site or clicking "I Agree", you agree to the use of cookies.
        Read our <a class="click" href="/#/cookiespolicy">cookies policy</a> and
        <a class="click" href="/#/privacystatement">privacy statement</a> for more information.
      </p>
      <button
              class="mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--colored mdl-color-text--white"
              v-on:click.prevent="accept">I agree
      </button>
    </div>
  </div>
</template>
<script>
  import Cookies from '@/assets/cookies-management.js'

  let enableCookieId = 'cb-enabled'
  export default {
    name: 'Cookies-accept',
    data () {
      return {
        hideMe: false
      }
    },
    computed: {
      visible: function () {
        let enable = Cookies.get(enableCookieId)
        return (enable !== 'true' && !this.hideMe)
      }
    },
    methods: {
      accept () {
        Cookies.set(enableCookieId, true, 30)
        this.hideMe = true
      }
    }
  }
</script>

<style scoped>
  /*Cookie Consent Begin*/
  #cookieConsent {
    background-color: rgba(20, 20, 20, 0.8);
    padding: 8px 0 8px 30px;
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    display: inline-block;
    z-index: 9999;
  }

  #cookieConsent > div {
    color: #ccc;
    line-height: 26px;
    margin-top: -20px;
    padding: 0 15px 15px 15px;
  }

  #closeCookieConsent {
    float: right;
    cursor: pointer;
    padding: 0 10px 0 10px;
    min-width: 20px;
    margin: -15px 0 0 0;
  }

  #closeCookieConsent:hover {
    color: #FFF;
  }
  .click {
    color: rgb(255, 64, 129);
    cursor: pointer;
    text-decoration: underline;
  }
</style>
