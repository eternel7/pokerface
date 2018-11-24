// For authoring Nightwatch tests, see
// http://nightwatchjs.org/guide#usage

module.exports = {
  'home e2e tests': function (browser) {
    // automatically uses dev Server port from /config.index.js
    // default: http://localhost:8080
    // see nightwatch.conf.js
    const devServer = browser.globals.devServerURL
    browser
      .url(devServer)
      .waitForElementVisible('#app-content', 1500)
      .assert.containsText('span.mdl-layout-title', 'Pokerface')
      .assert.elementCount('main', 1)
      .assert.elementPresent('.section')
      .assert.elementPresent('.section-inner')
      .end()
  },
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
      .assert.containsText('h2.card__title.mdl-card__title-text', 'Profil')
      .click('div.mdl-layout__drawer-button')
      .click('a#nav_logout')
      .pause(1500)
      .assert.containsText('h2.card__title.mdl-card__title-text', 'Connexion')
      .assert.elementCount('input#email', 1)
      .setValue('input#email', 'masse.david.07@gmail.com')
      .setValue('input#password', 'masse.david.07@gmail.com')
      .click('button#main-button')
      .pause(1500)
      .assert.containsText('h2.card__title.mdl-card__title-text', 'Profil')
      .pause(500)
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
  }
}
