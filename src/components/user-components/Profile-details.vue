<template>
  <div class="page-content">
    <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label"
         v-bind:class="{'is-dirty' : (user.email) ? true : false}">
      <input class="mdl-textfield__input" type="text" id="email" :readonly="(user.email) ? true : false"
             required
             v-model.trim="user.email"/>
      <label class="mdl-textfield__label" for="email">{{$t('user.Email')}}</label>
    </div>
    <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label"
         v-bind:class="{'is-dirty' : (user.first_name) ? true : false}">
      <input class="mdl-textfield__input" type="text" id="first_name"
             v-model.trim="user.first_name"/>
      <label class="mdl-textfield__label" for="first_name">{{$t('user.First_name')}}</label>
    </div>
    <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label"
         v-bind:class="{'is-dirty' : (user.last_name) ? true : false}">
      <input class="mdl-textfield__input" type="text" id="last_name"
             v-model.trim="user.last_name"/>
      <label class="mdl-textfield__label" for="last_name">{{$t('user.Last_name')}}</label>
    </div>
    <div class="link" v-on:click="askForAnImage"
         v-on:dragover.prevent="onDragOver" v-on:drop.prevent="onDrop">
      <img id="profilePreview" v-bind:src="user.avatar_image">
      <input hidden='hidden' type='file' id='fileInput' ref='fileInput' v-on:change.prevent="updatePreview"
             accept="image/*">
      <p class="center-align">{{$t('SignUp.ClickOrDropToUpdateYourProfilePicture')}}</p>
    </div>
    <button id="main-button" v-on:click.prevent="$emit('tryUpdate')" v-bind:class="{ pulse: updateNeeded }"
            class="mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--colored mdl-color-text--white">
      {{$t('user.Update')}}
    </button>
    <errorMessages v-bind:errors="errors"></errorMessages>
  </div>
</template>

<script>
  import ImageTools from '@/assets/image-tools.js'
  import FileDrop from '@/assets/file-drop.js'
  import ErrorMessages from '@/components/sub-components/ErrorMessages'

  export default {
    name: 'profileDetails',
    props: {
      user: Object,
      updateNeeded: undefined,
      errors: Array
    },
    components: {
      errorMessages: ErrorMessages
    },
    methods: {
      updatePreview (file) {
        const vm = this
        if (file !== undefined) {
          if (file.type === 'change') {
            file = vm.$refs.fileInput.files[0]
          }
          if (file.type.match('image.*')) {
            ImageTools.resizeImageBase64(file, 300, 300, function (result) {
              if (result) {
                vm.user.avatar_image = result
                vm.message = ''
              } else {
                console.log('updatePreview error', result)
              }
            })
          }
        }
        return true
      },
      askForAnImage (e) {
        const vm = this
        e.stopPropagation()
        return vm.$refs.fileInput.click()
      },
      onDrop (e) {
        const vm = this
        FileDrop.getFilesOnDrop(e, function (r) {
          if (r) {
            vm.updatePreview(r[0])
          }
        })
        return true
      },
      onDragOver (evt) {
        // Allow drop there
        return true
      }
    }
  }
</script>
<style scoped>
  #profilePreview {
    max-width: 200px;
    max-height: 200px;
  }

  .mdl-textfield {
    display: block;
    margin: auto;
  }

  .page-content {
    margin: 20px auto 20px;
  }

  .pulse {
    background-color: rgb(96, 125, 139);
    animation: color_change 2s infinite;
  }

  @-webkit-keyframes color_change {
    0%, 100% {
      background-color: rgb(96, 125, 139);
    }
    50% {
      background-color: rgb(255, 64, 129);
    }
  }

  @-moz-keyframes color_change {
    0%, 100% {
      background-color: rgb(96, 125, 139);
    }
    50% {
      background-color: rgb(255, 64, 129);
    }
  }

  @-ms-keyframes color_change {
    0%, 100% {
      background-color: rgb(96, 125, 139);
    }
    50% {
      background-color: rgb(255, 64, 129);
    }
  }

  @-o-keyframes color_change {
    0%, 100% {
      background-color: rgb(96, 125, 139);
    }
    50% {
      background-color: rgb(255, 64, 129);
    }
  }

  @keyframes color_change {
    0%, 100% {
      background-color: rgb(96, 125, 139);
    }
    50% {
      background-color: rgb(255, 64, 129);
    }
  }
</style>
