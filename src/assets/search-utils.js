'use strict'
/**
 * Created by eternel7 on 26/03/2016.
 */
const Search = (function () {
  function Search () {
  }
  Search.highlight = function (text, search) {
    if (typeof search === 'string' && search !== '') {
      let reg = new RegExp('(' + search + ')', 'gi')
      let r = text.replace(reg, '<span class="highlight-text">' + search + '</span>')
      return r
    } else {
      return text
    }
  }
  return Search
}())
export default Search
