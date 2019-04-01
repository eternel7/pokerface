<template>
  <div class="questionAndAnswer">
    <div class="question" data-questionid="55438828" id="question">
      <div class="post-layout">
        <div class="post-layout--left">
          <div class="grid fd-column ai-stretch">
            <i class="material-icons grid--cell post-vote-button link"
               title="This question shows research effort; it is useful and clear" aria-pressed="false"
               aria-label="up vote" data-selected-classes="fc-theme-primary">
              keyboard_arrow_up
            </i>
            <div class="vote-count"
                 itemprop="upvoteCount">
              {{question.answers_count}}
            </div>
            <i class="material-icons grid--cell post-vote-button link"
               title="This question does not show any research effort; it is unclear or not useful"
               aria-pressed="false" aria-label="down vote" data-selected-classes="fc-theme-primary">
              keyboard_arrow_down
            </i>
          </div>
        </div>
        <div class="post-layout--right">
          <div class="post-text">
            <i class="material-icons link close" @click="close()">
              close
            </i>
            <div class="text" itemprop="text" :title="textBody" v-html="question.body"></div>
          </div>
          <div v-if='question.last_editor' class="last-editor text">
              <span :title="question.updated_at">
                  {{$t('post.updated')}} {{update_date | niceDate}}
              </span>
            <span> - {{question.last_editor.username}}</span>
          </div>
          <div class="post-footer text">
            <div class="post-signature owner text">
              <div class="user-info">
                <div :title="question.created_at" class="user-action-time">
                  {{$t('post.created')}} {{creation_date | niceDate}}
                </div>
                <span class="user-avatar" :title="question.owner.username"
                      v-bind:style="'background-image: url('+question.owner.avatar_image+')'">
                  </span>
                <span class="user-details link" itemprop="author" itemscope=""
                      itemtype="http://schema.org/Person">
                    {{question.owner.username}}
                  </span>
              </div>
            </div>
            <div class="post-menu">
                <span title="short permalink to this question"
                      class="link-post link" itemprop="url" id="link-post">share</span>
              <span class="lsep">&nbsp;-&nbsp;</span>
              <span class="edit-post link"
                    title="revise and improve this post">edit</span>
              <span class="lsep">&nbsp;-&nbsp;</span>
              <span class="comments-link link"
                    title="Use comments to ask for more information or suggest improvements. Avoid answering questions in comments.">
                  add a comment
                </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import {authMixin} from '@/auth/authMixin.js'
  import {momentMixin} from '@/assets/momentMixin.js'
  import StringUtils from '@/assets/string-utils.js'
  import moment from 'moment'

  export default {
    name: 'Question-and-answers',
    mixins: [authMixin, momentMixin],
    props: ['user', 'chatroom', 'question'],
    created () {
      moment.locale(this.$i18n.locale)
    },
    computed: {
      creation_date: function () {
        return new Date(this.question.created_at)
      },
      update_date: function () {
        return new Date(this.question.updated_at)
      },
      userRelUrl: function () {
        return '/users/' + this.question.owner.id + '/' + this.question.owner.username
      },
      textBody: function () {
        return StringUtils.htmlToText(this.question.body)
      }
    },
    methods: {
      close: function () {
        this.$emit('close')
      }
    }
  }
</script>

<style scoped>
  .questionAndAnswer {
    position: relative;
    height: 80%;
    left: 50%;
    -webkit-transform: translateX(-50%); /* Chrome 4+, Op 15+, Saf 3.1, iOS Saf 3.2+ */
    -moz-transform: translateX(-50%); /* Fx 3.5-15 */
    -ms-transform: translateX(-50%); /* IE 9 */
    -o-transform: translateX(-50%); /* Op 10.5-12 */
    transform: translateX(-50%); /* Fx 16+, IE 10+ */
    margin-left: auto;
    margin-right: auto;
    background: #fff;
    max-width: 700px;
    overflow-y: scroll;
    overflow-x: hidden;
    padding: 5px;
    border-bottom: solid 1px #e4e4e4;
  }

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
    margin: 0 0 5px 0;
    word-break: break-word;
    overflow-x: scroll;
  }

  .post-text > div {
    width: calc(100% - 10px);
  }

  .close {
    position: absolute;
    top: 5px;
    right: 0;
    width: 36px;
    height: 24px;
  }

  .last-editor {
    margin: 0 0 10px 0;
  }

  .post-footer {
    position: relative;
  }

  .post-menu {
    float: left;
    display: inline-block;
    height: 100%;
  }

  .post-signature {
    float: right;
    display: inline-block;
    background-color: #eceff1;
    padding: 10px;
    margin-right: 10px;
  }

  .user-info {
    text-align: left;
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

  @supports (display: grid) {
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
