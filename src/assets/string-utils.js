'use strict'

/**
 * Created by eternel7 on 01/04/2019.
 */

const StringUtils = (function () {
  function StringUtils () {
  }// eslint-disable-next-line
  
  StringUtils.htmlToText = function (s) {
    let span = document.createElement('span')
    span.innerHTML = s
    return span.textContent || span.innerText
  }// eslint-disable-next-line
  return StringUtils
}())

export default StringUtils
