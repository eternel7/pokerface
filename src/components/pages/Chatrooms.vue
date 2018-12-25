<template>
  <div class="chatrooms">
    <dialog ref="dialog" class="mdl-dialog">
      <div class="mdl-dialog__content">
        <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
          <input class="mdl-textfield__input" type="text" id="label" v-model.trim="label"/>
          <label class="mdl-textfield__label" for="label">{{$t('room.Label')}}</label>
        </div>
        <div class="mdl-textfield mdl-js-textfield">
          <textarea class="mdl-textfield__input" type="text" rows="3" id="description"
                    v-model.trim="description"></textarea>
          <label class="mdl-textfield__label" for="description">{{$t('room.Description')}}</label>
        </div>
        <div class="link" v-on:click="askForAnImage($event, 'filePortraitInput')"
             v-on:dragover.prevent="onDragOver" v-on:drop.prevent="onDrop($event, 'portrait', 'fileImageInput')">
          <img v-if="portrait" id="portrait" v-bind:src="portrait" width="40px">
          <input hidden='hidden' type='file' id='filePortraitInput' ref='filePortraitInput'
                 v-on:change.prevent="updatePreview($event, 'portrait', 'filePortraitInput', 40, 40)"
                 accept="image/*">
          <p class="center-align">{{$t('room.ClickOrDropToAddAPortrait')}}</p>
        </div>
        <div class="link" v-on:click="askForAnImage($event, 'fileImageInput')"
             v-on:dragover.prevent="onDragOver" v-on:drop.prevent="onDrop($event, 'image', 'fileImageInput')">
          <img v-if="image" id="image" v-bind:src="image" width="80%">
          <input hidden='hidden' type='file' id='fileImageInput' ref='fileImageInput'
                 v-on:change.prevent="updatePreview($event, 'image', 'fileImageInput', 700, 700)"
                 accept="image/*">
          <p class="center-align">{{$t('room.ClickOrDropToAddAnImage')}}</p>
        </div>
      </div>
      <div class="mdl-dialog__actions">
        <button type="button" tabindex="10" id="OkDialog"
                class="mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent mdl-color-text--white"
                @click="tryRoomCreation">
          Ok
        </button>
        <button type="button" tabindex="20" id="CancelDialog" class="mdl-button close" v-on:click="hideRoomForm(true)">
          Cancel
        </button>
      </div>
    </dialog>
    <transition name="fade-slide-up" mode="out-in">
      <ul v-if="chatrooms.length">
        <transition-group name="shrink">
          <li is="chatroom-item"
              v-for="(chatroom, index) in chatrooms"
              v-bind:key="chatroom.id"
              v-bind:index="index"
              v-bind:chatroom="chatroom"
          ></li>
        </transition-group>
      </ul>
      <div v-else-if="$root.loading===false">
        <h4>No workplace.</h4>
        <p>
          <button tabindex="0" type="button"
                  class="mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent mdl-color-text--white"
                  @click="displayRoomForm">Create one!
          </button>
        </p>
      </div>
      <h4 v-else>Looking for a workplace...</h4>
    </transition>
    <button tabindex="30" type="button"
            class="mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--fab mdl-button--colored"
            @click="displayRoomForm">
      <i class="material-icons">add</i>
    </button>
  </div>
</template>

<script>
  import PageBase from '@/components/pages/Page'
  import ImageTools from '@/assets/image-tools.js'
  import FileDrop from '@/assets/file-drop.js'
  import ChatroomItem from '@/components/sub-components/Chatroom-item'
  import ErrorMessages from '@/components/sub-components/ErrorMessages'
  import {authMixin} from '@/auth/authMixin.js'
  import axios from 'axios'

  export default {
    name: 'chatrooms',
    extends: PageBase,
    props: ['search'],
    mixins: [authMixin],
    components: {
      ChatroomItem,
      errorMessages: ErrorMessages
    },
    data () {
      return {
        displaySearch: true,
        image: '',
        portrait: '',
        label: '',
        description: ''
      }
    },
    computed: {
      chatrooms: function () {
        let vm = this
        if (typeof vm.search === 'string' && vm.search !== '') {
          return vm.$root.chatrooms.filter(function (row) {
            return Object.keys(row).some(function (key) {
              return String(row[key]).toLowerCase().indexOf(vm.search) > -1
            })
          })
        } else {
          return vm.$root.chatrooms
        }
      }
    },
    methods: {
      tryGetChatrooms (evt) {
        let vm = this
        vm.errors = []
        vm.$root.loading = true
        vm.reception = false
        axios.get('/api/chatrooms/', vm.authHeader())
          .then(function (response) {
            vm.$root.loading = false
            // handle success
            if (response.data.chatrooms) {
              vm.$root.chatrooms = response.data.chatrooms
            } else {
              vm.errors = []
              vm.errors.push({message: response.data.message})
            }
          })
          .catch(function (error) {
            // handle error
            console.log(error)
            vm.$root.loading = false
            vm.errors = []
            vm.errors.push(error)
          })
          .then(function () {
            // always executed
            vm.$root.loading = false
          })
      },
      displayRoomForm: function (evt) {
        let vm = this
        vm.errors = []
        if (vm.$root.authenticated) {
          vm.image = ''
          vm.portrait = ''
          vm.label = ''
          vm.description = ''
          let dialog = vm.$refs['dialog']
          // eslint-disable-next-line no-undef
          dialogPolyfill.registerDialog(dialog)
          dialog.showModal()
        } else {
          vm.$router.push({name: 'Sign in'})
        }
      },
      hideRoomForm: function (val) {
        let vm = this
        let dialog = vm.$refs['dialog']
        if (dialog) {
          // eslint-disable-next-line no-undef
          dialogPolyfill.registerDialog(dialog)
          dialog.close()
        }
      },
      updatePreview (file, data, ref, imposedWidth, imposedHeight) {
        const vm = this
        if (file !== undefined) {
          if (file.type === 'change') {
            file = vm.$refs[ref].files[0]
          }
          if (file.type.match('image.*')) {
            let iWidth = imposedWidth || 300
            let iHeight = imposedHeight || 300
            ImageTools.resizeImageBase64(file, iWidth, iHeight, function (result) {
              if (result) {
                vm[data] = result
                vm.message = ''
              } else {
                console.log('updatePreview error', result)
              }
            })
          }
        }
        return true
      },
      askForAnImage (e, ref) {
        const vm = this
        e.stopPropagation()
        return vm.$refs[ref].click()
      },
      onDrop (e, data, ref) {
        const vm = this
        FileDrop.getFilesOnDrop(e, function (r) {
          if (r) {
            vm.updatePreview(r[0], data, ref)
          }
        })
        return true
      },
      onDragOver (evt) {
        // Allow drop there
        return true
      },
      tryRoomCreation: function (evt) {
        let vm = this
        let room = {
          label: vm.label,
          description: vm.description,
          portrait: vm.portrait,
          image: vm.image
        }
        vm.hideRoomForm(true)
        vm.$root.loading = true
        axios.post('/api/chatroom/', room, vm.authHeader())
          .then(function (response) {
            // handle success
            vm.$root.loading = false
            if (response.data.chatrooms) {
              vm.$root.chatrooms = response.data.chatrooms
              vm.$root.showSnackbar(vm.$i18n.t('room.CreationConfirmed'))
            } else {
              vm.errors = []
              vm.errors.push({message: response.data.message})
            }
          })
          .catch(function (error) {
            // handle error
            console.log(error)
            vm.$root.loading = false
            vm.errors = []
            vm.errors.push(error)
          })
          .then(function () {
            // always executed
            vm.$root.loading = false
          })
      }
    },
    created: function (e) {
      this.tryGetChatrooms(e)
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

  h1, h2, h3, h4 {
    font-weight: normal;
    color: #fff;
  }

  ul {
    list-style-type: none;
    padding: 0;
  }

  .mdl-dialog {
    top: 2vh;
    padding: 0;
  }

  button.mdl-button--fab {
    position: fixed;
    bottom: 2vh;
    right: 2vw;
  }

  .link-accent {
    color: rgb(255, 64, 129);
    text-decoration: underline;
    cursor: pointer;
  }

  .fade-slide-up-enter-active, .fade-slide-up-leave-active {
    transition: all 0.5s ease;
  }

  .fade-slide-up-enter, .fade-slide-up-leave-to {
    transform: translateY(-40px);
    opacity: 0;
  }

  .shrink, .shrink-move, .shrink-enter-active, .shrink-leave-active {
    transition: all 0.5s ease;
    -webkit-transform-origin: top;
    -moz-transform-origin: top;
    -o-transform-origin: top;
    transform-origin: top;
  }

  .shrink-enter, .shrink-leave-to {
    -webkit-transform: scaleY(0);
    -ms-transform: scaleY(0);
    transform: scaleY(0);
  }

  .shrink-leave, .shrink-enter-to {
    -webkit-transform: scaleY(1);
    -ms-transform: scaleY(1);
    transform: scaleY(1);
  }
</style>
