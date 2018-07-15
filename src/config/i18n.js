import Vue from 'vue'
import VueI18n from 'vue-i18n'
import fr from '@/../static/translations/fr.json'
import en from '@/../static/translations/en.json'

Vue.use(VueI18n)

// Should be load on demand depending on user selected locale
const messages = {
  en: en,
  fr: fr
}

export const locales = ['en', 'fr']

function getBrowserLanguage () {
  // last choice first if there is one
  let stored = localStorage.getItem('language')
  if (stored) {
    return stored
  }
  const DEFAULT_VALUE = 'en'
  const lang = navigator.language || navigator.userLanguage || navigator.browserLanguage || navigator.systemLanguage || DEFAULT_VALUE
  if (locales.indexOf(lang) > -1) {
    return lang
  }
  const availableLanguages = navigator.languages
  for (let lg of availableLanguages) {
    if (locales.indexOf(lg) > -1) {
      return lg
    }
  }
  return DEFAULT_VALUE
}
// Create VueI18n instance with options
const i18n = new VueI18n({
  locale: getBrowserLanguage(), // set locale
  messages // set locale messages
})
export default i18n

export function setLocale (lg) {
  i18n.locale = lg
  if (typeof Storage !== 'undefined') {
    localStorage.setItem('language', lg)
    // Code for localStorage/sessionStorage.
  } else {
    // Sorry! No Web Storage support..
  }
  return true
}
