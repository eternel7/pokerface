'use strict'
/**
 * Created by eternel7 on 26/03/2016.
 */
var ImageTools = (function () {
  function ImageTools () {
  }

  ImageTools.fileToBase64 = function (file, callback) {
    if (file.type.match('image.*')) {
      var charge = new FileReader()
      charge.readAsDataURL(file)
      charge.onloadend = function (ev) {
        callback(ev.target.result)
      }
    }
  }
  ImageTools.resizeImageBase64 = function (file, maxWidth, maxHeight, callback) {
    ImageTools.fileToBase64(file, function (base64) {
      if (base64) {
        var img = new Image()
        img.src = base64
        img.onload = function () {
          var MAX_WIDTH = maxWidth
          var MAX_HEIGHT = maxHeight
          var width = img.naturalWidth || img.width
          var height = img.naturalHeight || img.height
          var resize = false
          if (width > height) {
            if (width > MAX_WIDTH) {
              height *= MAX_WIDTH / width
              width = MAX_WIDTH
              resize = true
            }
          } else {
            if (height > MAX_HEIGHT) {
              width *= MAX_HEIGHT / height
              height = MAX_HEIGHT
              resize = true
            }
          }
          if (resize) {
            // resize only if needed to not lost gif animation or pixelize
            var canvas = document.createElement('canvas')
            canvas.width = width
            canvas.height = height
            var ctx = canvas.getContext('2d')
            ctx.drawImage(img, 0, 0, width, height)
            callback(canvas.toDataURL('image/png'))
          } else {
            callback(base64)
          }
        }
      }
    })
  }
  return ImageTools
}())
export default ImageTools
