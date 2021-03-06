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
    console.log('updateDataRoomStore', data)
    if (roomId) {
      if (data instanceof Array) {
        vm.$set(vm.$root.store[storePlace], roomId, data)
      } else if (data.update_id_field && data.update_id && data.update_field) {
        let objectIndex = vm.$root.store[storePlace][roomId].map(function (e) {
          if (data.update_parent_field) {
            return e[data.update_parent_field][data.update_id_field]
          }
          return e[data.update_id_field]
        }).indexOf(data.update_id)
        if (!isNaN(objectIndex)) {
          if (data.update_parent_field) {
            vm.$set(vm.$root.store[storePlace][roomId][objectIndex][data.update_parent_field], data.update_field, data[data.update_field])
          } else {
            vm.$set(vm.$root.store[storePlace][roomId][objectIndex], data.update_field, data[data.update_field])
          }
        } else {
          console.log('No data to update found in updateDataRoomStore',
            data, data.update_id_field, data.update_id, data.update_field)
        }
      } else {
        console.log('Missing data info on update to perform found in updateDataRoomStore',
          data, data.update_id_field, data.update_id, data.update_field)
      }
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
      'answer': answer,
      lang: vm.$root.$i18n.locale
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
  }// eslint-disable-next-line
  
  DataUtils.setAnswer = function (vm, answer, question) {
    vm.errors = []
    let roomId = vm.$route.params.id
    let answerMsg = Object.assign({}, answer)
    answerMsg.room = roomId
    answerMsg.message = vm.message
    let data = {
      question: question,
      answer: answerMsg,
      room: roomId,
      lang: vm.$root.$i18n.locale
    }
    DataUtils.managePostRequest('/api/chatroomsetanswer/', vm, true, data, function (response) {
      if (response.data.answer) {
        vm.$set(answer, 'answer_to', response.data.answer.answer_to)
        vm.$set(answer, 'type', response.data.answer.type)
        vm.$set(answer, 'post_id', response.data.answer.post_id)
        if (response.data.answer.answer_to) {
          vm.$root.showSnackbar(vm.$i18n.t('post.questionAnswered'))
        } else {
          vm.$root.showSnackbar(vm.$i18n.t('post.answerRejected'))
        }
        if (response.data.questions && vm.$root.questions instanceof Object) {
          DataUtils.updateDataRoomStore(vm, 'questions', roomId, response.data.questions)
        }
      } else {
        vm.errors = []
        vm.errors.push({message: response.data.message})
      }
    })
  }// eslint-disable-next-line
  
  DataUtils.updateQuestionState = function (vm, msg) {
    vm.errors = []
    msg.room = vm.$route.params.id
    msg.lang = vm.$root.$i18n.locale
    console.log('DataUtils.updateQuestionState')
    DataUtils.managePostRequest('/api/chatroomquestion/', vm, true, msg, function (response) {
      if (response.data.post) {
        if (msg.question) {
          vm.$root.showSnackbar(vm.$i18n.t('post.savedAsQuestion'))
        } else {
          vm.$root.showSnackbar(vm.$i18n.t('post.notAQuestionAnymore'))
        }
        if (response.data.questions && vm.$root.questions instanceof Object) {
          DataUtils.updateDataRoomStore(vm, 'questions', msg.room, response.data.questions)
        }
        vm.$nextTick(vm.updatemdl())
      } else {
        vm.errors = []
        vm.errors.push({message: response.data.message})
      }
    })
  }// eslint-disable-next-line
  
  DataUtils.sendBackAnswerToBot = function (vm, answer) {
    vm.errors = []
    answer.room = vm.$route.params.id
    answer.lang = vm.$root.$i18n.locale
    DataUtils.managePostRequest('/api/chatroomanswerbot/', vm, true, answer, function (response) {
      if (response.data.post) {
        if (response.data.questions && vm.$root.questions instanceof Object) {
          DataUtils.updateDataRoomStore(vm, 'questions', answer.room, response.data.questions)
        }
        vm.$nextTick(vm.updatemdl())
      } else {
        vm.errors = []
        vm.errors.push({message: response.data.message})
      }
    })
  }// eslint-disable-next-line
  
  return DataUtils
}())

export default DataUtils
