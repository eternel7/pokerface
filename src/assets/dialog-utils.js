'use strict'

/**
 * Created by eternel7 on 26/03/2016.
 */
const DialogUtils = (function () {
  function DialogUtils () {
    this.dialog = undefined
  }// eslint-disable-next-line
  
  DialogUtils.showModal = function (vm, ref) {
    let dialog = vm.$refs[ref]
    // eslint-disable-next-line
    dialogPolyfill.registerDialog(dialog)
    dialog.showModal()
    // eslint-disable-next-line
    componentHandler.upgradeDom()
    // eslint-disable-next-line
    componentHandler.upgradeAllRegistered()
  }
  DialogUtils.close = function (vm, ref) {
    let dialog = vm.$refs[ref]
    if (dialog) {
      // eslint-disable-next-line no-undef
      dialogPolyfill.registerDialog(dialog)
      dialog.close()
    }
  }
  return DialogUtils
}())
export default DialogUtils
