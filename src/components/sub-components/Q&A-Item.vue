<template>
  <div class="post-layout">
    <div class="post-layout--left">
      <div class="grid fd-column ai-stretch">
        <i class="material-icons grid--cell post-vote-button link"
           title="This item shows research effort; it is useful and clear" aria-pressed="false"
           aria-label="up vote" data-selected-classes="fc-theme-primary">
          keyboard_arrow_up
        </i>
        <div class="vote-count"
             itemprop="upvoteCount">
          {{item.vote_count}}
        </div>
        <i class="material-icons grid--cell post-vote-button link"
           title="This item does not show any research effort; it is unclear or not useful"
           aria-pressed="false" aria-label="down vote" data-selected-classes="fc-theme-primary">
          keyboard_arrow_down
        </i>
      </div>
    </div>
    <div class="post-layout--right">
      <div class="post-text">
        <i v-if="closable" class="material-icons link close" @click="close()">
          close
        </i>
        <div class="text" itemprop="text" v-html="item.body"></div>
      </div>
      <div v-if='item.last_editor' class="last-editor text">
              <span :title="item.updated_at">
                  {{$t('post.updated')}} {{update_date | niceDate}}
              </span>
        <span> - {{item.last_editor.username}}</span>
      </div>
      <div class="post-signature owner text">
        <div :title="item.created_at" class="user-action-time">
          {{$t('post.created')}} {{creation_date | niceDate}}
        </div>
        <span class="user-avatar" :title="item.owner.username"
              v-bind:style="'background-image: url('+item.owner.avatar_image+')'">
                  </span>
        <span class="user-details link" itemprop="author" itemscope=""
              itemtype="http://schema.org/Person">
            {{item.owner.username}}
          </span>
      </div>
      <div class="post-footer text">
        <div class="post-menu">
          <button title="short permalink to this item"
                  class="mdl-button post-link mdl-js-button mdl-js-ripple-effect
                       link-post link" itemprop="url" id="link-post">share
          </button>
          <button class="mdl-button post-link mdl-js-button mdl-js-ripple-effect
               edit-post link"
                  title="revise and improve this post">edit
          </button>
          <button class="mdl-button post-link mdl-js-button mdl-js-ripple-effect
               comments-link link" v-on:click="toggleAddComment()"
                  title="Use comments to ask for more information or suggest improvements. Avoid answering answers in comments.">
            <i class="material-icons" v-html="openCloseIcon"></i>comment
          </button>
          <div v-if="addComment" class="mdl-textfield mdl-js-textfield comment-input-field">
            <input class="mdl-textfield__input text" type="text" :id="'addComment' + item.id">
            <label class="mdl-textfield__label" :for="'addComment' + item.id">add comment...</label>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import Search from '@/assets/search-utils.js'
  import {authMixin} from '@/auth/authMixin.js'
  import {momentMixin} from '@/assets/momentMixin.js'
  import StringUtils from '@/assets/string-utils.js'
  import moment from 'moment'

  require('material-design-lite')

  export default {
    name: 'qa-item',
    mixins: [authMixin, momentMixin],
    props: ['user', 'item', 'search', 'closable'],
    data: function () {
      return {
        addComment: false,
        comments: []
      }
    },
    created () {
      moment.locale(this.$i18n.locale)
    },
    computed: {
      creation_date: function () {
        return new Date(this.item.created_at)
      },
      update_date: function () {
        return new Date(this.item.updated_at)
      },
      bodyH: function () {
        return Search.highlight(StringUtils.htmlToText(this.item.body), this.search)
      },
      openCloseIcon: function () {
        if (this.addComment) {
          return 'keyboard_arrow_up'
        }
        return 'keyboard_arrow_down'
      }
    },
    methods: {
      updatemdl: function () {
        // eslint-disable-next-line
        componentHandler.upgradeDom()
        // eslint-disable-next-line
        componentHandler.upgradeAllRegistered()
      },
      close: function () {
        this.$emit('close')
      },
      toggleAddComment: function () {
        let vm = this
        vm.addComment = !vm.addComment
        if (vm.addComment) {
          vm.$nextTick(function () {
            let addComment = document.getElementById('addComment' + vm.item.id)
            if (addComment) {
              vm.updatemdl()
              addComment.focus()
            }
          })
        }
      }
    },
    mounted: function () {
      let vm = this
      vm.updatemdl()
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

  .post-vote-button {
    width: 40px;
    height: 40px;
    line-height: 40px;
    font-size: 30px;
    font-weight: 400;
    color: #808e95;
    background-color: #eceff1;
    text-align: center;
  }

  .vote-count {
    color: #808e95;
    font-size: 25px;
    font-weight: 600;
    height: 40px;
    line-height: 40px;
    text-align: center;
    vertical-align: middle;
  }

  .post-text {
    background-color: #eceff1;
    text-align: left;
    padding: 5px;
    margin: 0 5px 10px 0;
    word-break: break-word;
    overflow-x: auto;
  }

  .post-text > div {
    width: calc(100% - 10px);
  }

  .close {
    position: absolute;
    top: 10px;
    right: 5px;
    width: 36px;
    height: 24px;
  }

  .last-editor {
    color: #808e95 !important;
    float: left;
    margin: 0 0 10px 0;
  }

  .post-footer {
    position: relative;
  }

  .post-menu {
    float: left;
    display: inline-block;
    text-align: left;
    height: 100%;
  }

  .post-link {
    color: #808e95;
    margin-top: 5px;
    text-transform: none;
  }

  .post-signature {
    float: right;
    display: inline-block;
    text-align: left;
    background-color: #eceff1;
    padding: 10px;
    margin-right: 10px;
  }

  .user-avatar {
    display: inline-block;
    height: 40px;
    width: 40px;
    box-sizing: border-box;
    border-radius: 50%;
    background-color: #757575;
    color: #fff;
    background-size: cover;
    background-position: center center;
  }

  .user-details {
    display: inline-block;
    line-height: 40px;
    vertical-align: top;
  }

  .post-layout {
    display: flex;
    flex-wrap: wrap;
    justify-content: flex-end;
    box-sizing: border-box;
    width: 100%;
  }

  .post-layout--left, .post-layout--left.votecell {
    flex-grow: 0;
    width: 70px;
    padding: 0;
  }

  .post-layout--right {
    flex-shrink: 1;
    width: 100%;
    min-width: 0;
  }

  .post-layout--right .post-text, .post-layout--right .comments {
    margin-right: 10px;
  }

  .text {
    word-wrap: break-word;
    font-size: 13px;
    font-family: "Roboto", "Open Sans", sans-serif;
    font-weight: 400;
    color: #403f3e;
  }

  .comment-input-field {
    padding-top: 0;
    padding-bottom: 0;
    width: 95%;
  }

  .comment-input-field > label {
    top: 4px;
    font-size: 13px;
  }

  .mdl-textfield__label:after {
    bottom: 0;
  }

  @supports (display: grid) {
    /*noinspection CssInvalidPropertyValue*/
    body:not(.no-grid-post-layout) .post-layout {
      display: grid;
      grid-template-columns: -webkit-max-content 1fr;
      grid-template-columns: max-content 1fr;
    }

    body:not(.no-grid-post-layout) .post-layout--left {
      grid-column: 1;
      width: auto;
    }

    body:not(.no-grid-post-layout) .post-layout--left, body:not(.no-grid-post-layout) .post-layout--left.votecell {
      width: auto;
      padding-right: 15px;
      padding-left: 10px;
    }

    body:not(.no-grid-post-layout) .post-layout--right {
      grid-column: 2;
      width: auto;
    }

    body:not(.no-grid-post-layout) .post-layout--full {
      grid-column: 1 / 3;
    }
  }
</style>