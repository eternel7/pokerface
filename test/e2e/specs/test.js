// For authoring Nightwatch tests, see
// http://nightwatchjs.org/guide#usage

module.exports = {
  'user management e2e tests': function (browser) {
    // automatically uses dev Server port from /config.index.js
    // default: http://localhost:8080
    // see nightwatch.conf.js
    const devServer = browser.globals.devServerURL
    browser
      .url(devServer)
      .waitForElementVisible('#app-content', 1500)
      .assert.elementCount('a#secondary-button', 1)
      .click('a#secondary-button')
      .pause(1500)
      .assert.elementCount('input#email', 1)
      .setValue('input#email', 'masse.david.07@gmail.com')
      .setValue('input#password', 'masse.david.07@gmail.com')
      .setValue('input#passwordConfirm', 'masse.david.07@gmail.com')
      .click('button#main-button')
      .pause(1500)
      .click('div.mdl-layout__drawer-button')
      .pause(500)
      .click('a#nav_logout')
      .pause(1500)
      .assert.containsText('h2.card__title.mdl-card__title-text', 'Connexion')
      .assert.elementCount('input#email', 1)
      .setValue('input#email', 'masse.david.07@gmail.com')
      .setValue('input#password', 'masse.david.07@gmail.com')
      .click('button#main-button')
      .pause(1500)
      .click('div.mdl-layout__drawer-button')
      .pause(500)
      .click('a#nav_profile')
      .pause(1500)
      .click('div#profile_tab_3')
      .click('button#secondary-button')
      .pause(500)
      .click('button#CancelDialog')
      .click('button#secondary-button')
      .pause(500)
      .click('button#OkDialog')
      .pause(2000)
      .assert.containsText('h2.card__title.mdl-card__title-text', 'Inscription')
      .end()
  },
  'sign in': function (browser) {
    const devServer = browser.globals.devServerURL
    browser
      .url(devServer)
      .waitForElementVisible('#app-content', 1500)
      .assert.elementCount('a#secondary-button', 1)
      .click('a#secondary-button')
      .pause(1500)
      .assert.elementCount('input#email', 1)
      .setValue('input#email', 'masse.david.07@gmail.com')
      .setValue('input#password', 'masse.david.07@gmail.com')
      .setValue('input#passwordConfirm', 'masse.david.07@gmail.com')
      .click('button#main-button')
      .pause(1500)
      .click('div.mdl-layout__drawer-button')
      .end()
  },
  'Sign up, go to room (should be empty) and create a room': function (browser) {
    const devServer = browser.globals.devServerURL
    const path = require('path')
    browser
      .url(devServer)
      .waitForElementVisible('#app-content', 1500)
      .assert.containsText('h2.card__title.mdl-card__title-text', 'Connexion')
      .assert.elementCount('input#email', 1)
      .setValue('input#email', 'masse.david.07@gmail.com')
      .setValue('input#password', 'masse.david.07@gmail.com')
      .click('button#main-button')
      .pause(1500)
      .assert.elementCount('h4.solo', 1)
      .assert.elementCount('button#fab_displayRoomForm', 1)
      .assert.elementCount('button#solo_displayRoomForm', 1)
      .click('button#solo_displayRoomForm')
      .pause(500)
      .assert.elementCount('input#label', 1)
      .setValue('input#label', 'label')
      .setValue('textarea#description', 'description')
      .assert.elementCount('div#PlaceForFilePortraitInput', 1)
      .setValue('input#filePortraitInput', path.join(__dirname, '/../uploads/anonymous.jpg'))
      .pause(500)
      .setValue('input#fileImageInput', path.join(__dirname, '/../uploads/anonymous.jpg'))
      .pause(500)
      .click('button#OkDialog')
      .pause(1500)
      .assert.elementCount('div.mdl-list__item-primary-content', 1)
      .click('div.mdl-list__item-primary-content')
      .pause(2000)
      .assert.elementCount('#chat_tab_0.is-active', 1)
      .end()
  },
  'Post a question, answer, post same question. Good answer should be display': function (browser) {
    const devServer = browser.globals.devServerURL
    browser
      .url(devServer)
      .waitForElementVisible('#app-content', 1500)
      .click('button#closeCookieConsent')
      .assert.containsText('h2.card__title.mdl-card__title-text', 'Connexion')
      .assert.elementCount('input#email', 1)
      .setValue('input#email', 'masse.david.07@gmail.com')
      .setValue('input#password', 'masse.david.07@gmail.com')
      .click('button#main-button')
      .waitForElementVisible('div.mdl-list__item-primary-content', 1500)
      .assert.elementCount('div.mdl-list__item-primary-content', 1)
      .click('div.mdl-list__item-primary-content')
      .waitForElementVisible('#chat_tab_0.is-active', 1500)
      .assert.elementCount('#chat_tab_0.is-active', 1)
      .waitForElementVisible('.messages.left', 5000)
      .assert.elementCount('.messages.left', 1)
      .setValue('div#sendmessage>textarea', 'Quel est l\'âge du capitaine?')
      .click('div#send')
      .waitForElementVisible('.messages.right', 500)
      .assert.elementCount('.messages.right', 1)
      .click('div.messages.right')
      .waitForElementVisible('div.mdl-menu__container.is-visible>ul>li.mdl-menu__item.action_menu_isAQuestion', 1000)
      .click('div.mdl-menu__container.is-visible>ul>li.mdl-menu__item.action_menu_isAQuestion')
      .setValue('div#sendmessage>textarea', 'Le capitaine a 51 ans.')
      .click('div#send')
      .waitForElementVisible('.messages.right:not(.a-question)', 500)
      .click('div.messages.right:not(.a-question)')
      .waitForElementVisible('div.mdl-menu__container.is-visible>ul>li.mdl-menu__item.action_menu_isAnAction', 1000)
      .click('div.mdl-menu__container.is-visible>ul>li.mdl-menu__item.action_menu_isAnAction')
      .click('#chat_tab_1')
      .waitForElementVisible('li.question', 1000)
      .click('li.question')
      .waitForElementVisible('div.grid--item.answer-indicator.link.unselectable', 1000)
      .click('div.grid--item.answer-indicator.link.unselectable')
      .click('#chat_tab_0')
      .waitForElementVisible('.messages.right:not(.a-question)', 500)
      .setValue('div#sendmessage>textarea', 'Quel est l\'âge du capitaine?')
      .click('div#send')
      .waitForElementVisible('.messages.left:not(.a-question)', 500)
      .end()
  },
  'Post a question, answer, post similar question and add it to synonyms and post last question. Good answer should be display': function (browser) {
    const devServer = browser.globals.devServerURL
    browser
      .url(devServer)
      .waitForElementVisible('#app-content', 1500)
      .click('button#closeCookieConsent')
      .assert.containsText('h2.card__title.mdl-card__title-text', 'Connexion')
      .assert.elementCount('input#email', 1)
      .setValue('input#email', 'masse.david.07@gmail.com')
      .setValue('input#password', 'masse.david.07@gmail.com')
      .click('button#main-button')
      .waitForElementVisible('div.mdl-list__item-primary-content', 1500)
      .assert.elementCount('div.mdl-list__item-primary-content', 1)
      .click('div.mdl-list__item-primary-content')
      .waitForElementVisible('#chat_tab_0.is-active', 1500)
      .assert.elementCount('#chat_tab_0.is-active', 1)
      .waitForElementVisible('.messages.left', 5000)
      .assert.elementCount('.messages.left', 1)
      .setValue('div#sendmessage>textarea', 'Quel âge a le capitaine?')
      .click('div#send')
      .waitForElementVisible('.messages.right', 500)
      .assert.elementCount('.messages.right', 1)
      .pause(500)
      .assert.elementCount('.messages.left', 2)
      .assert.elementCount('div.user_quick_response>button.yes', 1)
      .click('div.user_quick_response>button.yes')
      .pause(500)
      .assert.elementCount('.messages.left', 3)
      .end()
  }
}
