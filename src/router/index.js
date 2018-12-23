import Vue from 'vue'
import Router from 'vue-router'
import { authMixin } from '@/auth/authMixin.js'
import Home from '@/components/pages/Home'
import SignInPage from '@/components/pages/Sign-in'
import SignUp from '@/components/pages/Sign-up'
import Profile from '@/components/pages/Profile'
import ForgotPassword from '@/components/pages/Forgot-password'
import ResetPassword from '@/components/pages/Reset-password'
import CookiesPolicy from '@/components/pages/Cookies-Policy'
import PrivacyStatement from '@/components/pages/Privacy-Statement'
import Chat from '@/components/pages/Chat'
import Chatrooms from '@/components/pages/Chatrooms'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/signin',
      name: 'Sign in',
      component: SignInPage
    },
    {
      path: '/signup',
      name: 'Sign up',
      component: SignUp
    },
    {
      path: '/profile',
      name: 'Profile',
      component: Profile,
      beforeEnter: (to, from, next) => {
        authMixin.methods.checkToken('all', next)
      }
    },
    {
      path: '/forgotpassword',
      name: 'Forgotpassword',
      component: ForgotPassword
    },
    {
      path: '/resetpassword/:resetPasswordToken?',
      name: 'ResetPassword',
      component: ResetPassword
    },
    {
      path: '/cookiespolicy',
      name: 'Cookies policy',
      component: CookiesPolicy
    },
    {
      path: '/privacystatement',
      name: 'Privacy statement',
      component: PrivacyStatement
    },
    {
      path: '/chat/:id',
      name: 'Chat',
      component: Chat,
      beforeEnter: (to, from, next) => {
        authMixin.methods.checkToken('all', next)
      }
    },
    {
      path: '/chatrooms',
      name: 'Chatrooms',
      component: Chatrooms,
      beforeEnter: (to, from, next) => {
        authMixin.methods.checkToken('all', next)
      }
    }
  ]
})
