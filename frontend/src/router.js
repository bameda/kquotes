import VueRouter from 'vue-router'

import home from './layouts/home/home'
import login from './layouts/login/login'

const router = new VueRouter({
    mode: 'history',
    routes: [
        {
            path: '/',
            name: 'home',
            component: home,
            isDefault: true
        },
        {
            path: '/login',
            name: 'login',
            component: login
        }
    ]
})

export { VueRouter, router }
