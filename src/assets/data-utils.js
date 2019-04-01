'use strict'

/**
 * Created by eternel7 on 29/03/2019.
 */

import axios from 'axios'

const DataUtils = (function () {
  function DataUtils () {
  }// eslint-disable-next-line
  
  DataUtils.manageGetRequest = function (url, vm, silent, onSuccess) {
    if (!silent) {
      vm.$root.loading = true
    }
    axios.get(url, vm.authHeader())
      .then(function (response) {
        if (!silent) {
          vm.$root.loading = false
        }
        if (onSuccess) {
          onSuccess(response)
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
  
  DataUtils.refreshQuestions = function (vm, silent) {
    vm.errors = []
    let roomId = vm.$route.params.id
    DataUtils.manageGetRequest('/api/chatroomquestions/' + roomId, vm, silent, function (response) {
      if (response.data.questions) {
        vm.$set(vm.$root.questions, roomId, response.data.questions)
      } else {
        vm.errors = []
        vm.errors.push({message: response.data.message})
      }
    })
  }

  DataUtils.refreshUsers = function (vm, silent) {
    vm.errors = []
    let roomId = vm.$route.params.id
    DataUtils.manageGetRequest('/api/chatroomusers/' + roomId, vm, silent, function (response) {
      if (response.data.users) {
        vm.$set(vm, 'users_in_room', response.data.users)
      } else {
        vm.errors = []
        vm.errors.push({message: response.data.message})
      }
    })
  }
  return DataUtils
}())

export default DataUtils
