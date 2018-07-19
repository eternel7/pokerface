<template>
  <div class="mdl-card__supporting-text">
    <button @click="authenticate('facebook')"
            class="mdl-button mdl-js-button mdl-button--icon social-btn__facebook">
      <i class="fa fa-facebook fa-fw"></i>
    </button>
    <button @click="authenticate('twitter')"
            class="mdl-button mdl-js-button mdl-button--icon social-btn__twitter">
      <i class="fa fa-twitter fa-fw"></i>
    </button>
    <button @click="authenticate('google')"
            class="mdl-button mdl-js-button mdl-button--icon social-btn__google">
      <i class="fa fa-google fa-fw"></i>
    </button>
  </div>
</template>
<script>
  import {authMixin} from '@/auth/authMixin'

  export default {
    name: 'socialLogin',
    mixins: [authMixin],
    data () {
      return {}
    }
  }
</script>
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .social-btn__twitter {
    background-color: #00acee;
    color: #ffffff;
  }

  .social-btn__twitter:hover {
    background-color: #07d0ff;
    box-shadow: 0 2px 2px 0 rgba(0, 0, 0, .14), 0 3px 1px -2px rgba(0, 0, 0, .2), 0 1px 5px 0 rgba(0, 0, 0, .12);
  }

  .social-btn__facebook {
    background-color: #3b5998;
    color: #ffffff;
  }

  .social-btn__facebook:hover {
    background-color: #5f8ef2;
    box-shadow: 0 2px 2px 0 rgba(0, 0, 0, .14), 0 3px 1px -2px rgba(0, 0, 0, .2), 0 1px 5px 0 rgba(0, 0, 0, .12);
  }

  .social-btn__google {
    background-color: #e93f2e;
    color: #ffffff;
  }

  .social-btn__google:hover {
    background-color: #fc774e;
    box-shadow: 0 2px 2px 0 rgba(0, 0, 0, .14), 0 3px 1px -2px rgba(0, 0, 0, .2), 0 1px 5px 0 rgba(0, 0, 0, .12);
  }
</style>
