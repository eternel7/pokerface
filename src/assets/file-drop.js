'use strict'
/**
 * Created by eternel7 on 26/03/2016.
 */
const FileDrop = (function () {
  function FileDrop () {
    this.files = []
  }// eslint-disable-next-line

  FileDrop.getFilesOnDrop = function (event, callback) {
    let transfer = FileDrop._getTransfer(event)
    if (!transfer) {
      return
    }
    FileDrop._preventAndStop(event)
    if (FileDrop._haveFiles(transfer.types)) {
      callback(transfer.files)
    }
  }
  FileDrop._getTransfer = function (event) {
    return event.dataTransfer ? event.dataTransfer : event.originalEvent.dataTransfer // jQuery fix;
  }
  FileDrop._preventAndStop = function (event) {
    event.preventDefault()
    event.stopPropagation()
  }
  FileDrop._haveFiles = function (types) {
    if (!types) {
      return false
    }
    if (types.indexOf) {
      return types.indexOf('Files') !== -1
    } else if (types.contains) {
      return types.contains('Files')
    } else {
      return false
    }
  }
  return FileDrop
}())
export default FileDrop
