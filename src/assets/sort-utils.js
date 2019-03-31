'use strict'
/**
 * Created by eternel7 on 10/03/2019.
 */
const Sort = (function () {
  function Sort () {
  }

  Sort.onUpdated_at = function (q1, q2) {
    let d1 = new Date(q1.updated_at)
    let d2 = new Date(q2.updated_at)
    return (d1 < d2) ? 1 : -1
  }

  return Sort
}())
export default Sort
