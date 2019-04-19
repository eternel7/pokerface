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
  Math.linearTween = function (t, b, c, d) {
    return c * t / d + b
  }
  Math.easeInQuad = function (t, b, c, d) {
    t /= d
    return c * t * t + b
  }
  Math.easeOutQuad = function (t, b, c, d) {
    t /= d
    return -c * t * (t - 2) + b
  }
  Math.easeInOutQuad = function (t, b, c, d) {
    t /= d / 2
    if (t < 1) return c / 2 * t * t + b
    t--
    return -c / 2 * (t * (t - 2) - 1) + b
  }
  Math.easeInCubic = function (t, b, c, d) {
    t /= d
    return c * t * t * t + b
  }
  Math.easeInCubic = function (t, b, c, d) {
    t /= d
    return c * t * t * t + b
  }
  Math.easeOutCubic = function (t, b, c, d) {
    t /= d
    t--
    return c * (t * t * t + 1) + b
  }
  Math.easeInOutCubic = function (t, b, c, d) {
    t /= d / 2
    if (t < 1) return c / 2 * t * t * t + b
    t -= 2
    return c / 2 * (t * t * t + 2) + b
  }
  Math.easeInSine = function (t, b, c, d) {
    return -c * Math.cos(t / d * (Math.PI / 2)) + c + b
  }
  Math.easeOutSine = function (t, b, c, d) {
    return c * Math.sin(t / d * (Math.PI / 2)) + b
  }
  Math.easeInOutSine = function (t, b, c, d) {
    return -c / 2 * (Math.cos(Math.PI * t / d) - 1) + b
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
        scrollableElt.scrollTop = Math.easeInOutSine(currentTime, start, change, duration)
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
