'use strict'
/**
 * Created by eternel7 on 26/03/2016.
 */
const Security = (function () {
  function Security () {
  }
  Security.stripScripts = function (s) {
    var div = document.createElement('div')
    div.innerHTML = s
    var scripts = div.getElementsByTagName('script')
    var i = scripts.length
    while (i--) {
      scripts[i].parentNode.removeChild(scripts[i])
    }
    return div.innerHTML
  }
  Security.noHtmlInjection = function (txt) {
    return txt.replace(/</g, '&lt;').replace(/>/g, '&gt;')
  }
  Security.escapeHtml = function (text) {
    let map = {
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      '"': '&quot;',
      '\'': '&#039;'
    }
    return text.replace(/[&<>"']/g, function (m) {
      return map[m]
    })
  }
  return Security
}())
export default Security
