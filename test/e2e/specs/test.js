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
      .assert.elementCount('div#PlaceForFilePortraitInput',1)
      .setValue('input#filePortraitInput', require('path').resolve(__dirname + '/../uploads/anonymous.jpg'))
      .pause(500)
      .setValue('input#fileImageInput', require('path').resolve(__dirname + '/../uploads/anonymous.jpg'))
      .pause(500)
      .click('button#OkDialog')
      .pause(1500)
      .assert.elementCount('div.mdl-list__item-primary-content', 1)
      .click('div.mdl-list__item-primary-content')
      .pause(2000)
      .assert.elementCount('#chat_tab_0.is-active', 1)
      .end()
  }
}
