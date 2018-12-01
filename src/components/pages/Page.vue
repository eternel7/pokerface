<script>
  export default {
    name: 'Page',
    data: function () {
      return {
        displayHeader: true
      }
    },
    mounted: function () {
      // eslint-disable-next-line
      componentHandler.upgradeDom()
      // eslint-disable-next-line
      componentHandler.upgradeAllRegistered()
      if (this.$root.setSearch) {
        this.$root.setSearch(!!this.displaySearch)
      }
      if (this.$root.setBack) {
        this.$root.setBack(!!this.displayBack)
      }
      if (this.$root.setHeader) {
        this.$root.setHeader(!!this.displayHeader)
      }
    }
  }
</script>
