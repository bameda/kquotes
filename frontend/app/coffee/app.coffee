@kquotes = kquotes = {}


############################
## Load Modules
###########################

modules = [
    # Main Global Modules
    # Specific Modules
    # Vendor modules
    "ngRoute"
    "ngSanitize"
    "ngAnimate"
    "ngMaterial"
]

module = angular.module("kquotes", modules)


############################
## Configuration
###########################

configure = ($routeProvider, $locationProvider, $httpProvider) ->
    $routeProvider.when("/",
        {templateUrl: "/partials/login.html",})
    $routeProvider.when("/org/:slug/",
        {templateUrl: "/partials/organization-home.html"})

    ## Errors/Exceptions
    $routeProvider.when("/error",
        {templateUrl: "/partials/err/error.html"})
    $routeProvider.when("/not-found",
        {templateUrl: "/partials/err/not-found.html"})
    $routeProvider.when("/permission-denied",
        {templateUrl: "/partials/err/permission-denied.html"})

    $routeProvider.otherwise({redirectTo: '/not-found'})
    $locationProvider.html5Mode({enabled: true, requireBase: false})

    defaultHeaders = {
        "Content-Type": "application/json"
        "Accept-Language": "en"
    }

    $httpProvider.defaults.headers.delete = defaultHeaders
    $httpProvider.defaults.headers.patch = defaultHeaders
    $httpProvider.defaults.headers.post = defaultHeaders
    $httpProvider.defaults.headers.put = defaultHeaders
    $httpProvider.defaults.headers.get = {}


module.config(["$routeProvider", "$locationProvider", "$httpProvider", configure])


############################
## Initialize
###########################

init = ($log) ->
    $log.info """
                       Wellcome to kQuotes
                       -------------------

                   .-=-.
                 .'     \\        pio
              __.|    9 )_\\  pio         .-=-.
         _.-''          /              _/     `.
      <`'     ..._    <'              /_( 9    |.__
       `._ .-'    `.  |        pio      \\          ``-._
        ; `.    .-'  /            pio    `>    _...     `'>
         \\  `~~'  _.'                     |  .'    `-. _,'
          `"..."'% _                       \\ `-.    ,' ;
            \\__  |`.                        `.  `~~'  /
            /`.                             _ 7`"..."'
                                            ,'| __/
                                        hjw     ,'\
    """
module.run(["$log", init])