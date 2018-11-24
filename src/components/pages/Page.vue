<script>
  export default {
    name: 'Page',
    data: function () {
      return {}
    },
    mounted: function () {
      // eslint-disable-next-line
      componentHandler.upgradeDom()
      // eslint-disable-next-line
      componentHandler.upgradeAllRegistered()
      if (this.$root.setSearch && this.$root.setBack) {
        this.$root.setSearch(!!this.displaySearch)
        this.$root.setBack(!!this.displayBack)
      }
    }
  }
</script>
