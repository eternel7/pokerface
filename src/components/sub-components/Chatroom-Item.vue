<template>
  <li class="chatroom-item mdl-list__item mdl-list__item--three-line">
    <div class="mdl-list__item-primary-content" v-on:click="gotoChat(chatroom.id)">
      <div class="img" v-if="chatroom.portrait"
           v-bind:style="'background-image: url('+chatroom.portrait+')'"></div>
      <i v-else class="material-icons mdl-list__item-avatar">person</i>
      <span>{{chatroom.label}}</span>
      <span class="mdl-list__item-text-body" :alt="chatroom.description">
        {{notepad}}
      </span>
    </div>
    <div class="mdl-list__item-secondary-content"
         v-on:click="addContent(chatroom.id)">
      <i class="tooltip material-icons">cloud_upload</i>
    </div>
    <router-link :to="'/chat/'+chatroom.id" class="mdl-list__item-secondary-action mdl-js-ripple-effect">
    </router-link>
  </li>
</template>

<script>
  export default {
    name: 'chatroom-item',
    props: ['chatroom', 'index'],
    data: function () {
      return {
        notepad: (this.chatroom.description.length > 60) ? this.chatroom.description.substr(0, 57) + '...' : this.chatroom.description,
        displayRoomForm: false
      }
    },
    methods: {
      gotoChat: function (index) {
        this.$router.push({name: 'Chat', params: {id: index}})
      },
      addContent: function (index) {
        console.log('trying to add content to room id :', index)
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .chatroom-item {
    text-align: left;
    background-color: #fff;
  }

  .chatroom-item:hover {
    background-color: #eeeeee;
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

  li {
    border-bottom: solid 1px #e4e4e4;
  }

  li > div > i {
    color: rgba(0, 0, 0, .54);
  }

  a {
    color: rgba(0, 0, 0, .54);
    text-decoration: none;
  }
</style>
