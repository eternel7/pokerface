import moment from 'moment'

export const momentMixin = {
  filters: {
    formatDate: function (value) {
      if (value) {
        let d = new Date(value)
        return d.toLocaleDateString() + ' ' + d.toLocaleTimeString()
      }
    },
    formatTime: function (value) {
      if (value) {
        let d = new Date(value)
        return d.toLocaleTimeString()
      }
    },
    niceDate: function (value) {
      if (value) {
        let d = new Date(value)
        let n = new Date()
        if (Math.abs(n.getTime() - d.getTime()) < 1000 * 60 * 60) {
          return moment(d).fromNow().toLowerCase()
        } else {
          return moment(d).calendar().toLowerCase()
        }
      }
    }
  }
}
