<template>
  <div id="container" class="mdl-card mdl-shadow--16dp">
    <div class="mdl-card__supporting-text">
      <cardFabTitle userTitle="Page.Profile"></cardFabTitle>
      <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
        <input class="mdl-textfield__input" type="text" id="email" readonly required
               v-model.trim="user.email"/>
        <label class="mdl-textfield__label" for="email">Email</label>
      </div>
      <div class="link" v-on:click="askForAnImage"
           v-on:dragover.prevent="onDragOver" v-on:drop.prevent="onDrop">
        <img id="profilePreview" v-bind:src="image" style="max-width:200px; max-height:200px">
        <input hidden='hidden' type='file' id='fileInput' ref='fileInput' v-on:change.prevent="updatePreview"
               accept="image/*">
        <p class="center-align">{{$t('SignUp.ClickOrDropToUpdateYourProfilePicture')}}</p>
      </div>
    </div>
    </div>
</template>

<script>
  import UserProfile from '@/assets/user-profile.js'
  import PageBase from '@/components/pages/Page'
  import CardFabTitle from '@/components/sub-components/Card-fab-title'
  export default {
    name: 'Profile',
    extends: PageBase,
    components: {
      cardFabTitle: CardFabTitle
    },
    data () {
      return {
        image: '/static/img/icons/apple-touch-icon-76x76.png',
        message: '',
        errors: []
      }
    },
    computed: {
      user: function () {
        return JSON.parse(window.localStorage.getItem('auth-user'))
      }
    },
    methods: {
      updatePreview (file) {
        return UserProfile.updatePreview(file, this)
      },
      askForAnImage (e) {
        return UserProfile.askForAnImage(e, this)
      },
      onDrop (e) {
        return UserProfile.onDrop(e, this)
      },
      onDragOver (e) {
        return UserProfile.onDragOver(e, this)
      }
    }
  }
</script>

<style scoped>

  .mdl-card {
    overflow: visible !important;
    z-index: auto !important;
  }

  #container {
    margin: auto;
  }
</style>
