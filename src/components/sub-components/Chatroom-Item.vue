<template>
  <li class="chatroom-item mdl-list__item mdl-list__item--three-line">
    <dialog :ref="'dialog'+chatroom.id" class="mdl-dialog">
      <h5>{{$t('data.New')}}</h5>
      <div class="mdl-dialog__content">
        <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label"
             v-bind:class="{'is-dirty' : (label) ? true : false}">
          <input class="mdl-textfield__input" type="text" id="label" minlength="4"
                 v-model.trim="label"/>
          <label class="mdl-textfield__label" for="label">{{$t('data.Label')}}</label>
        </div>
        <div class="mdl-textfield mdl-js-textfield"
             v-bind:class="{'is-dirty' : (description) ? true : false}">
          <textarea class="mdl-textfield__input" type="text" rows="3" id="description"
                    v-model.trim="description"></textarea>
          <label class="mdl-textfield__label" for="description">{{$t('data.Description')}}</label>
        </div>
        <div class="link" v-on:click="askForAFile($event, 'fileInput')"
             v-on:dragover.prevent="onDragOver" v-on:drop.prevent="onDrop($event, 'fileInput', 'filename')">
          <form enctype="multipart/form-data" novalidate>
            <input hidden='hidden' type='file' id='fileInput' name='fileInput' ref='fileInput'
                   v-on:change.prevent="updateFile($event, 'fileInput', 'filename')"
                   :disabled="$root.loading">
          </form>
          <p v-if="!$root.loading">
            Drag your file here to begin<br/> or click to browse<br/>
            <span class='filename' v-if="filename">{{filename}}</span>
          </p>
          <p v-if="$root.loading">
            Uploading file...
          </p>
        </div>
        <errorMessages v-bind:errors="errors"></errorMessages>
      </div>
      <div class="mdl-dialog__actions">
        <button type="button" tabindex="10" id="OkDialog"
                class="mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent
                mdl-color-text--white" @click="tryDataCreation">
          Ok
        </button>
        <button type="button" tabindex="20" id="CancelDialog" class="mdl-button close"
                v-on:click="hideDataForm(chatroom.id)">
          Cancel
        </button>
      </div>
    </dialog>
    <div class="mdl-list__item-primary-content" v-on:click="gotoChat(chatroom.id)">
      <div class="img" v-if="chatroom.portrait"
           v-bind:style="'background-image: url('+chatroom.portrait+')'"></div>
      <i v-else class="material-icons mdl-list__item-avatar">person</i>
      <span v-html="labelH"></span>
      <span class="mdl-list__item-text-body" :alt="descriptionH" v-html="notepadH">
      </span>
    </div>
    <div class="mdl-list__item-secondary-content" :id="'room_menu'+chatroom.id">
      <i class="tooltip material-icons">more_vert</i>
      <ul v-if="room_menu_item.length > 2" class="mdl-menu mdl-menu--bottom-right mdl-js-menu mdl-js-ripple-effect"
          :for="'room_menu'+chatroom.id" :data-mdl-for="'room_menu'+chatroom.id">
        <li v-for="action in room_menu_item" v-on:click="doAction(action.js, chatroom.id)"
            class="mdl-menu__item" v-bind:class="{ 'mdl-menu__item--full-bleed-divider': action.separatorAfter}">
          {{$t('room_menu.action.' + action.labelId)}}
        </li>
      </ul>
    </div>
  </li>
</template>

<script>
  import Search from '@/assets/search-utils.js'
  import FileDrop from '@/assets/file-drop.js'
  import {authMixin} from '@/auth/authMixin.js'
  import ErrorMessages from '@/components/sub-components/ErrorMessages'
  import axios from 'axios'

  require('material-design-lite')

  export default {
    name: 'chatroom-item',
    props: ['chatroom', 'index', 'search'],
    mixins: [authMixin],
    components: {
      errorMessages: ErrorMessages
    },
    data: function () {
      return {
        notepad: (this.chatroom.description.length > 60) ? this.chatroom.description.substr(0, 57) + '...' : this.chatroom.description,
        label: '',
        description: '',
        filename: '',
        state: 0, // 0 initial , 1 saving
        errors: [],
        room_menu_item: [
          {
            js: 'open',
            labelId: 'open'
          },
          {
            js: 'addData',
            labelId: 'addData'
          },
          {
            js: 'edit',
            labelId: 'edit',
            separatorAfter: true
          },
          {
            js: 'remove',
            labelId: 'remove'
          }
        ]
      }
    },
    mounted: function () {
      // eslint-disable-next-line
      componentHandler.upgradeDom()
      // eslint-disable-next-line
      componentHandler.upgradeAllRegistered()
    },
    computed: {
      descriptionH: function () {
        return Search.highlight(this.chatroom.description, this.search)
      },
      notepadH: function () {
        return Search.highlight(this.notepad, this.search)
      },
      labelH: function () {
        return Search.highlight(this.chatroom.label, this.search)
      }
    },
    methods: {
      doAction: function (actionName, index) {
        let vm = this
        if (actionName === 'open') {
          vm.gotoChat(index)
        } else if (actionName === 'addData') {
          vm.addContent(index)
        } else {
          this.$emit(actionName, index)
        }
      },
      gotoChat: function (index) {
        this.$router.push({name: 'Chat', params: {id: index}})
      },
      addContent: function (index) {
        this.displayDataForm(index)
      },
      displayDataForm: function (index) {
        let vm = this
        vm.errors = []
        if (vm.$root.authenticated) {
          vm.label = ''
          vm.description = ''
          vm.filename = ''
          vm.$refs['fileInput'].value = ''
          let dialog = vm.$refs['dialog' + index]
          // eslint-disable-next-line no-undef
          dialogPolyfill.registerDialog(dialog)
          dialog.showModal()
        } else {
          vm.$router.push({name: 'Sign in'})
        }
      },
      hideDataForm: function (index) {
        let vm = this
        let dialog = vm.$refs['dialog' + index]
        if (dialog) {
          // eslint-disable-next-line no-undef
          dialogPolyfill.registerDialog(dialog)
          dialog.close()
        }
      },
      updateFile (file, ref, data) {
        const vm = this
        if (file !== undefined) {
          if (file.type === 'change') {
            if (vm.$refs[ref].files[0]) {
              vm.$data[data] = vm.$refs[ref].files[0].name
            } else {
              vm.$data[data] = ''
            }
          } else if (file[0] && file[0].name) {
            vm.$refs[ref].files = file
            vm.$data[data] = file[0].name
          }
          if (vm.label === '') {
            vm.label = vm.$data[data]
          }
        }
        return true
      },
      askForAFile (e, ref) {
        const vm = this
        e.stopPropagation()
        return vm.$refs[ref].click()
      },
      onDrop (e, ref, data) {
        const vm = this
        FileDrop.getFilesOnDrop(e, function (r) {
          if (r) {
            vm.updateFile(r, ref, data)
          }
        })
        return true
      },
      onDragOver (evt) {
        // Allow drop there
        return true
      },
      tryDataCreation: function () {
        let vm = this
        vm.errors = []
        let fileInput = vm.$refs['fileInput']
        if (!fileInput || fileInput.files.length !== 1) {
          vm.errors.push({message: 'data.missing.file'})
        } else {
          const formData = new FormData()
          // append the files to FormData
          formData.append('raw_data', fileInput.files[0])
          formData.append('label', vm.label)
          formData.append('description', vm.description)
          formData.append('room', vm.chatroom.id)
          vm.hideDataForm(vm.chatroom.id)
          vm.$root.loading = true
          let header = vm.authHeader()
          header['headers']['Content-Type'] = 'multipart/form-data'
          axios.post('/api/chatroomdata/', formData, header)
            .then(function (response) {
              // handle success
              vm.$root.loading = false
              if (response.data.chatrooms) {
                vm.$root.chatrooms = response.data.chatrooms
                vm.$root.showSnackbar(vm.$i18n.t('data.CreationConfirmed'))
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
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

  h1, h2, h3, h4, h5 {
    font-weight: normal;
    color: #424242;
  }

  .mdl-dialog {
    text-align: center;
    top: 2vh;
    padding: 0;
  }

  .filename {
    background-color: rgb(255, 64, 129);
    box-shadow: 10px 0 0 rgb(255, 64, 129), -10px 0 0 rgb(255, 64, 129);
    color: #ffffff;
    padding: 5px 1px 5px 1px;
    word-break: break-word;
  }

  .chatroom-item {
    border-left: 4px rgb(255, 255, 255) solid;
    text-align: left;
    background-color: #fff;
    -webkit-transition: border 500ms ease;
    -moz-transition: border 500ms ease;
    -o-transition: border 500ms ease;
    transition: border 500ms ease;
  }

  .chatroom-item:hover {
    border-left: 4px rgb(255, 64, 129) solid;
    cursor: pointer;
    cursor: hand;
  }

  .chatroom-item div.img {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    margin-right: 16px;
    background-size: cover;
    background-position: center center;
    float: left;
  }

  li.chatroom-item {
    border-bottom: solid 1px #e4e4e4;
  }

  li.chatroom-item > div > i {
    color: rgba(0, 0, 0, .54);
  }

  a {
    color: rgba(0, 0, 0, .54);
    text-decoration: none;
  }
</style>
