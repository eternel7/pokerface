import {shallowMount} from '@vue/test-utils'
import App from '@/App'
import router from '@/router'
import Loading from '@/components/Loading'
import NavBar from '@/components/Navbar'

describe('App.vue', () => {
  let wrapper

  beforeEach(() => {
    wrapper = shallowMount(App, {router})
  })

  it('should match Snapshot', () => {
    expect(wrapper.element).toBeDefined()
    expect(wrapper.element).toMatchSnapshot()
  })

  it('should contain Loading component', () => {
    expect(wrapper.contains(Loading)).toBeTruthy()
  })

  it('should contain Navbar component', () => {
    expect(wrapper.contains(NavBar)).toBeTruthy()
  })
})
