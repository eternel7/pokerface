<template>
  <div v-if="visible" id="cookieConsent">
    <button id="closeCookieConsent"
            class="mdl-button mdl-button--raised mdl-button--colored mdl-color-text--white"
            v-on:click.prevent="accept">x
    </button>
    <div>
      <h6>Notice</h6>
      <p>This website or its third-party tools use cookies, which are necessary to its functioning and required to
        achieve
        the purposes illustrated in the <a href="#" target="_blank">Privacy Shield Policy</a>. By closing this banner,
        clicking a link or continuing to
        browse otherwise, you agree to the use of cookies.
      </p>
      <button
        class="mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--colored mdl-color-text--white"
        v-on:click.prevent="accept">That's Fine
      </button>
    </div>
  </div>
</template>
<script>
  function setCookie (cname, cvalue, exdays) {
    let d = new Date()
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000))
    let expires = 'expires=' + d.toUTCString()
    document.cookie = cname + '=' + cvalue + ';' + expires + ';path=/'
  }

  function getCookie (cname) {
    let name = cname + '='
    let decodedCookie = decodeURIComponent(document.cookie)
    let ca = decodedCookie.split(';')
    for (let i = 0; i < ca.length; i++) {
      let c = ca[i]
      while (c.charAt(0) === ' ') {
        c = c.substring(1)
      }
      if (c.indexOf(name) === 0) {
        return c.substring(name.length, c.length)
      }
    }
    return ''
  }

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
        let enable = getCookie(enableCookieId)
        return (enable !== 'true' && !this.hideMe)
      }
    },
    methods: {
      accept () {
        setCookie(enableCookieId, true, 30)
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
</style>
