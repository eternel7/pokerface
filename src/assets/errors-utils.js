'use strict'
/**
 * Created by eternel7 on 10/03/2019.
 */
const ErrorMngt = (function () {
  function ErrorMngt () {
  }

  ErrorMngt.add = function (errorsArray, e, vm, prefix) {
    errorsArray.push({message: e.message})
    if (e.errors) {
      for (let er in e.errors) {
        let str = e.errors[er][0]
        console.log(typeof str, str)
        errorsArray.push({
          message: vm.$i18n.t((prefix) ? prefix + '.' + er : er) +
            ': ' + vm.$i18n.t((prefix) ? prefix + '.' + str.replace(/\s+|\./g, '') : str.replace(/\s+|\./g, ''))
        })
      }
    }
  }
  return ErrorMngt
}())
export default ErrorMngt
