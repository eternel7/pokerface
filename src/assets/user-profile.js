'use strict'
/**
 * Created by eternel7 on 26/03/2016.
 */

import FileDrop from '@/assets/file-drop.js'
import ImageTools from '@/assets/image-tools.js'

const UserProfile = (function () {
  function UserProfile () {
  }

  UserProfile.updatePreview = function (file, vm) {
    if (file !== undefined) {
      if (file.type === 'change') {
        file = vm.$refs.fileInput.files[0]
      }
      if (file.type.match('image.*')) {
        ImageTools.resizeImageBase64(file, 300, 300, function (result) {
          if (result) {
            vm.image = result
            vm.message = ''
          } else {
            console.log('updatePreview error', result)
          }
        })
      }
    }
    return true
  }
  UserProfile.askForAnImage = function (e, vm) {
    e.stopPropagation()
    return vm.$refs.fileInput.click()
  }
  UserProfile.onDrop = function (e, vm) {
    FileDrop.getFilesOnDrop(e, function (r) {
      if (r) {
        vm.updatePreview(r[0])
      }
    })
    return true
  }
  UserProfile.onDragOver = function (e, vm) {
    // Allow drop there
    return true
  }
  return UserProfile
}())
export default UserProfile
