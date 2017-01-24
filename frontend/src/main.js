// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import { VueRouter, router } from './router'
import ApolloClient, { createNetworkInterface, addTypename } from 'apollo-client'
import VueApollo from 'vue-apollo'

// Apollo GraphQL Connection
const networkInterface = createNetworkInterface({
    uri: 'http://localhost:8000/graphql',
    transportBatching: true
})

const apolloClient = new ApolloClient({
    networkInterface,
    queryTransformer: addTypename
})

Vue.use(VueApollo, { apolloClient })

// Vue Router
Vue.use(VueRouter)

/* eslint-disable no-new */
new Vue({
    el: '#app',
    router,
    template: '<router-view></router-view>'
})
