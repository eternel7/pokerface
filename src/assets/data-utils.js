'use strict'

/**
 * Created by eternel7 on 29/03/2019.
 */

import axios from 'axios'

const DataUtils = (function () {
  function DataUtils () {
  }// eslint-disable-next-line
  
  DataUtils.refreshQuestions = function (vm, silent) {
    console.log('refreshQuestions', silent)
    vm.errors = []
    if (!silent) {
      vm.$root.loading = true
    }
    let roomId = vm.$route.params.id
    axios.get('/api/chatroomquestions/' + roomId, vm.authHeader())
      .then(function (response) {
        if (!silent) {
          vm.$root.loading = false
        }
        // handle success
        if (response.data.questions) {
          vm.$set(vm.$root.questions, roomId, response.data.questions)
        } else {
          vm.errors = []
          vm.errors.push({message: response.data.message})
        }
      })
      .catch(function (error) {
        // handle error
        console.log(error)
        if (!silent) {
          vm.$root.loading = false
        }
        vm.errors = []
        vm.errors.push(error)
      })
      .then(function () {
        // always executed
        vm.$root.loading = false
      })
  }
  return DataUtils
}())

export default DataUtils
