<template>
  <div class="chatrooms">
    <dialog ref="dialogChatroom" class="mdl-dialog">
      <h5 v-if="label!==''">{{$t('room.Update')}}</h5>
      <h5 v-else>{{$t('room.New')}}</h5>
      <div class="mdl-dialog__content">
        <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label"
             v-bind:class="{'is-dirty' : (label) ? true : false}">
          <input class="mdl-textfield__input" type="text" id="label" v-model.trim="label"
                 required="required" minlength="3"/>
          <label class="mdl-textfield__label" for="label">{{$t('room.Label')}}</label>
        </div>
        <div class="mdl-textfield mdl-js-textfield" v-bind:class="{'is-dirty' : (description) ? true : false}">
          <textarea class="mdl-textfield__input" type="text" rows="3" id="description"
                    required="required" v-model.trim="description"></textarea>
          <label class="mdl-textfield__label" for="description">{{$t('room.Description')}}</label>
        </div>
        <div class="link" v-on:click="askForAnImage($event, 'filePortraitInput')" id="PlaceForFilePortraitInput"
             v-on:dragover.prevent="onDragOver" v-on:drop.prevent="onDrop($event, 'portrait', 'fileImageInput')">
          <img v-if="portrait" id="portrait" v-bind:src="portrait" width="40px">
          <input hidden='hidden' type='file' id='filePortraitInput' ref='filePortraitInput'
                 v-on:change.prevent="updatePreview($event, 'portrait', 'filePortraitInput', 40, 40)"
                 accept="image/*">
          <p class="center-align">{{$t('room.ClickOrDropToAddAPortrait')}}</p>
        </div>
        <div class="link" v-on:click="askForAnImage($event, 'fileImageInput')" id="PlaceForFileImageInput"
             v-on:dragover.prevent="onDragOver" v-on:drop.prevent="onDrop($event, 'image', 'fileImageInput')">
          <img v-if="image" id="image" v-bind:src="image" width="80%">
          <input hidden='hidden' type='file' id='fileImageInput' ref='fileImageInput'
                 v-on:change.prevent="updatePreview($event, 'image', 'fileImageInput', 700, 700)"
                 accept="image/*">
          <p class="center-align">{{$t('room.ClickOrDropToAddAnImage')}}</p>
        </div>
        <errorMessages v-bind:errors="errors"></errorMessages>
      </div>
      <div class="mdl-dialog__actions">
        <button type="button" tabindex="10" id="OkDialog"
                class="mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent mdl-color-text--white"
                @click="tryRoomCreationOrUpdate">
          {{$t('button.Ok')}}
        </button>
        <button type="button" tabindex="20" id="CancelDialog" class="mdl-button close" v-on:click="hideRoomForm(true)">
          {{$t('button.Cancel')}}
        </button>
      </div>
    </dialog>
    <dialog ref="deleteDialogChatroom" class="mdl-dialog">
      <h5>{{$t('room.Delete')}}</h5>
      <div class="mdl-dialog__content">
        <div>
          <img v-if="portrait" id="portrait-delete" v-bind:src="portrait" width="40px">
        </div>
        <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label"
             v-bind:class="{'is-dirty' : (label) ? true : false}">
          <input class="mdl-textfield__input" readonly="readonly" type="text" id="label-delete" v-model.trim="label"/>
          <label class="mdl-textfield__label" for="label">{{$t('room.Label')}}</label>
        </div>
        <div class="mdl-textfield mdl-js-textfield" v-bind:class="{'is-dirty' : (description) ? true : false}">
          <textarea class="mdl-textfield__input" readonly="readonly" type="text" rows="3" id="description-delete"
                    v-model.trim="description"></textarea>
          <label class="mdl-textfield__label" for="description">{{$t('room.Description')}}</label>
        </div>
        <div>
          <img v-if="image" id="image-delete" v-bind:src="image" width="80%">
        </div>
      </div>
      <div class="mdl-dialog__actions">
        <button type="button" tabindex="10" id="Ok-deleteDialog"
                class="mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent mdl-color-text--white"
                @click="tryRoomDeletion(id)">
          {{$t('button.Ok')}}
        </button>
        <button type="button" tabindex="20" id="Cancel-deleteDialog" class="mdl-button close"
                v-on:click="hideDeleteRoomForm(true)">
          {{$t('button.Cancel')}}
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
              v-bind:search="search"
              v-on:edit="editRoom"
              v-on:remove="removeRoom">
          </li>
        </transition-group>
      </ul>
      <div v-else-if="$root.loading===false">
        <h4 class="solo">{{$t('room.NoWorkplace')}}</h4>
        <p>
          <button tabindex="0" type="button" id="solo_displayRoomForm"
                  class="mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent mdl-color-text--white"
                  @click="displayRoomForm">{{$t('room.CreateOne')}}
          </button>
        </p>
      </div>
      <h4 class="solo" v-else>{{$t('room.LookingForAWorkplace')}}</h4>
    </transition>
    <button tabindex="30" type="button" id="fab_displayRoomForm"
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
  import DialogUtils from '@/assets/dialog-utils.js'
  import ErrorMngt from '@/assets/errors-utils.js'
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
        description: '',
        id: undefined,
        errors: []
      }
    },
    computed: {
      chatrooms: function () {
        let vm = this
        let searchInKeys = ['label', 'description']
        if (typeof vm.search === 'string' && vm.search !== '') {
          return vm.$root.chatrooms.filter(function (row) {
            return Object.keys(row).some(function (key) {
              if (searchInKeys.indexOf(key) > -1) {
                return String(row[key]).toLowerCase().indexOf(vm.search) > -1
              }
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
      displayRoomForm: function (evt, chatroom) {
        let vm = this
        vm.errors = []
        if (vm.$root.authenticated) {
          if (!chatroom) {
            vm.image = ''
            vm.portrait = ''
            vm.label = ''
            vm.description = ''
            vm.id = undefined
          } else {
            Object.assign(vm.$data, chatroom)
          }
          DialogUtils.showModal(vm, 'dialogChatroom')
        } else {
          vm.$router.push({name: 'Sign in'})
        }
      },
      hideRoomForm: function (index) {
        let vm = this
        DialogUtils.close(vm, 'dialogChatroom')
      },
      getChatroom: function (index) {
        let vm = this
        let filter = vm.$root.chatrooms.filter(function (row) {
          return (row.id === index)
        })
        return filter[0]
      },
      editRoom: function (index) {
        let vm = this
        let chatroom = vm.getChatroom(index)
        vm.displayRoomForm(null, chatroom)
      },
      removeRoom: function (index) {
        let vm = this
        let chatroom = vm.getChatroom(index)
        if (chatroom) {
          Object.assign(vm.$data, chatroom)
          DialogUtils.showModal(vm, 'deleteDialogChatroom')
        }
      },
      hideDeleteRoomForm: function (val) {
        let vm = this
        DialogUtils.close(vm, 'deleteDialogChatroom')
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
      tryRoomCreationOrUpdate: function (evt) {
        let vm = this
        let room = {
          label: vm.label,
          description: vm.description,
          portrait: vm.portrait,
          image: vm.image
        }
        vm.$root.loading = true
        if (typeof vm.id === 'number') {
          room['id'] = vm.id
          axios.put('/api/uchatroom/', room, vm.authHeader())
            .then(function (response) {
              // handle success
              vm.$root.loading = false
              if (response.data.chatrooms) {
                vm.$root.chatrooms = response.data.chatrooms
                vm.$root.showSnackbar(vm.$i18n.t('room.UpdateConfirmed'))
                vm.hideRoomForm(true)
              } else {
                vm.errors = []
                ErrorMngt.add(vm.errors, response.data, vm, 'room')
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
        } else {
          axios.post('/api/chatroom/', room, vm.authHeader())
            .then(function (response) {
              // handle success
              vm.$root.loading = false
              if (response.data.chatrooms) {
                vm.$root.chatrooms = response.data.chatrooms
                vm.$root.showSnackbar(vm.$i18n.t('room.CreationConfirmed'))
                vm.hideRoomForm(true)
              } else {
                vm.errors = []
                ErrorMngt.add(vm.errors, response.data, vm, 'room')
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
      tryRoomDeletion: function (index) {
        let vm = this
        vm.hideDeleteRoomForm(true)
        vm.$root.loading = true
        if (typeof vm.id === 'number') {
          axios.delete('/api/dchatroom/' + vm.id, vm.authHeader())
            .then(function (response) {
              console.log(response.data)
              // handle success
              vm.$root.loading = false
              if (response.data.chatrooms) {
                vm.$root.chatrooms = response.data.chatrooms
                vm.$root.showSnackbar(vm.$i18n.t('room.DeletionConfirmed'))
              } else {
                vm.errors = []
                vm.errors.push({message: response.data.message})
                vm.$root.showSnackbar(vm.$i18n.t(response.data.message))
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
      }
    },
    created: function (e) {
      this.tryGetChatrooms(e)
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .chatrooms {
    max-width: 99%;
    margin: auto;
  }

  h1, h2, h3, h4, h5 {
    font-weight: normal;
    color: #424242;
  }

  ul {
    list-style-type: none;
    padding: 0;
  }

  h4.solo {
    color: #eeeeee;
  }

  .mdl-dialog {
    text-align: center;
    top: 2vh;
    padding: 0;
  }

  button.mdl-button--fab {
    position: fixed;
    bottom: 2vh;
    right: 2vw;
  }

  .fade-slide-right-leave-active button.mdl-button--fab,
  .fade-slide-right-enter-active button.mdl-button--fab {
    display: none;
    visibility: hidden;
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
