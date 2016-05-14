var app = angular.module('timesum', ['ui.router']);


app.config(function($stateProvider, $urlRouterProvider){
    /*路由模块*/
    $urlRouterProvider.otherwise("/home");
    $stateProvider
        .state('home', {
            url: "/home",
            templateUrl: "partials/home.html",
            controller:'ctrl_home'
        })
        .state('about', {
            url: "/about",
            templateUrl: "partials/about.html"
        })
        .state('userinfo', {
            url: "/userinfo",
            templateUrl: "partials/userinfo.html",
            controller:'ctrl_userinfo'
        })
        .state('changepwd', {
            url: "/changepwd",
            templateUrl: "partials/changepwd.html",
            controller:'ctrl_changepwd'
        });


});


app.run(['$rootScope', '$window', '$location', '$log', function ($rootScope, $window, $location, $log,$http) {
    //监听location的变化，实时更新path变量
    var locationChangeSuccessOff = $rootScope.$on('$locationChangeSuccess', locationChangeSuccess);
    function locationChangeSuccess(event) {
        $rootScope.path=$location.path();
    }
    
    
}]);