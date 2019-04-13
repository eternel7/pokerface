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
  }// eslint-disable-next-line
  
  DataUtils.managePostRequest = function (url, vm, silent, data, onSuccess) {
    if (!silent) {
      vm.$root.loading = true
    }
    axios.post(url, data, vm.authHeader())
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
  }// eslint-disable-next-line
  
  DataUtils.updateDataRoomStore = function (vm, storePlace, roomId, data) {
    if (roomId) {
      vm.$set(vm.$root.store[storePlace], roomId, data)
    } else {
      vm.$set(vm.$root.store, storePlace, data)
    }
  }// eslint-disable-next-line
  
  DataUtils.refreshQuestions = function (vm, silent) {
    var roomId = vm.$route.params.id
    vm.errors = []
    DataUtils.manageGetRequest('/api/chatroomquestions/' + roomId, vm, silent, function (response) {
      if (response.data.questions) {
        vm.$set(vm.$root.store.questions, roomId, response.data.questions)
      } else {
        vm.errors = []
        vm.errors.push({message: response.data.message})
      }
    })
  }// eslint-disable-next-line
  
  DataUtils.refreshUsers = function (vm, silent) {
    let roomId = vm.$route.params.id
    vm.errors = []
    DataUtils.manageGetRequest('/api/chatroomusers/' + roomId, vm, silent, function (response) {
      if (response.data.users) {
        vm.$set(vm.$root.store, 'users_in_room', response.data.users)
      } else {
        vm.errors = []
        vm.errors.push({message: response.data.message})
      }
    })
  }// eslint-disable-next-line
  
  DataUtils.acceptAnswer = function (vm, answer, question, user) {
    let data = {
      'question': question,
      'answer': answer
    }
    var roomId = vm.$route.params.id
    vm.errors = []
    DataUtils.managePostRequest('/api/chatroomacceptanswer/', vm, true, data, function (response) {
      if (response.data.questions) {
        vm.$set(vm.$root.store.questions, roomId, response.data.questions)
      } else {
        vm.errors = []
        vm.errors.push({message: response.data.message})
      }
    })
  }// eslint-disable-next-line
  
  DataUtils.sendAnswer = function (vm, answer, question, resetfield) {
    let data = {
      'question': question,
      'answer': answer
    }
    var roomId = vm.$route.params.id
    vm.errors = []
    DataUtils.managePostRequest('/api/chatroomaddanswer/', vm, true, data, function (response) {
      if (response.data.questions) {
        vm.$set(vm.$root.store.questions, roomId, response.data.questions)
        vm.$data[resetfield] = ''
      } else {
        vm.errors = []
        vm.errors.push({message: response.data.message})
      }
    })
  }
  return DataUtils
}())

export default DataUtils
