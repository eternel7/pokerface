'use strict'
/**
 * Created by eternel7 on 10/03/2019.
 */
const Animate = (function () {
  function Animate () {
  }

  // t = current time
  // b = start value
  // c = change in value
  // d = duration
  Math.easeInOutQuad = function (t, b, c, d) {
    t /= d / 2
    if (t < 1) return c / 2 * t * t + b
    t--
    return -c / 2 * (t * (t - 2) - 1) + b
  }

  Animate.scrollToPos = function (scrollableElt, to, duration) {
    if (duration <= 0) {
      scrollableElt.scrollTop = to
    } else {
      let start = scrollableElt.scrollTop
      let change = to - start
      let currentTime = 0
      let increment = 20
      let animateScroll = function () {
        currentTime += increment
        scrollableElt.scrollTop = Math.easeInOutQuad(currentTime, start, change, duration)
        if (currentTime < duration) {
          setTimeout(animateScroll, increment)
        }
      }
      animateScroll()
    }
  }
  return Animate
}())
export default Animate
