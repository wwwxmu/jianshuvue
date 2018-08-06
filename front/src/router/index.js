import Vue from 'vue'
import Router from 'vue-router'
const routerOptions = [
//  {path: '/', component: 'Home'},
//  {path: '/about', component: 'About'},
  {path: '/j/:id', component: 'demo', meta: {title: '简书'}},
  {path: '*', component: 'NotFound', meta: {title: '找不到页面'}}
]
const routes = routerOptions.map(route => {
  return {
    ...route,
    component: () => import(`@/components/${route.component}.vue`)
  }
})
Vue.use(Router)
export default new Router({
  routes,
  mode: 'history'
})
