<template>
  <div>
    <cardFabTitle userTitle="user.SignIn"></cardFabTitle>
    <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
      <input class="mdl-textfield__input" id="email" required autofocus
             v-model="sync_email"/>
      <label class="mdl-textfield__label" for="email">Email</label>
    </div>
    <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
      <input class="mdl-textfield__input" type="password" id="password" required
             v-model="sync_password"/>
      <label class="mdl-textfield__label" for="password">Password</label>
    </div>
  </div>
</template>

<script>
  import CardFabTitle from '@/components/sub-components/Card-fab-title'
  export default {
    name: 'profileDetails',
    components: {
      cardFabTitle: CardFabTitle
    }
  }
</script>
<style scoped>
  .card__title {
    text-align: center;
    font-weight: 600;
    font-size: 32px;
    line-height: 40px;
    margin: auto;
  }

  #login-fab {
    border-radius: 50%;
    height: 56px;
    margin: auto;
    min-width: 56px;
    width: 56px;
    overflow: hidden;
    background: rgba(158, 158, 158, .2);
    box-shadow: 0 1px 1.5px 0 rgba(0, 0, 0, .12), 0 1px 1px 0 rgba(0, 0, 0, .24);
    position: absolute;
    top: -30px;
    text-align: center;
    left: 0;
    right: 0;
  }

  #lock-icon {
    margin-top: 5px;
  }
</style>
