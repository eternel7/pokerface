<script>
    export default {
      name: 'Page',
      mounted: function () {
        // eslint-disable-next-line
        componentHandler.upgradeDom()
        // eslint-disable-next-line
        componentHandler.upgradeAllRegistered()
      }
    }
</script>
