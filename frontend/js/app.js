var app = angular.module('timesum', ['ui.router']);


app.config(function($stateProvider, $urlRouterProvider){
    /*路由模块*/
    $urlRouterProvider
        .otherwise("/404")
        .when('', '/home')
        .when('/ac/:ac_id', '/ac/:ac_id/detail');
    $stateProvider
        .state('home', {
            url: "/home",
            templateUrl: "partials/home.html",
            controller:'ctrl_home'
        })
        .state('new_ac', {
            url: "/new_ac",
            templateUrl: "partials/new_ac.html",
            controller:'ctrl_new_ac'
        })
        .state('ac_detail', {
            url: "/ac/:ac_id/detail",
            templateUrl: "partials/ac_detail.html",
            controller:'ctrl_ac_detail'
        })
        .state('time_input', {
            url: "/time_input",
            templateUrl: "partials/time_input.html",
            controller:'ctrl_time_input'
        })
        .state('about', {
            url: "/about",
            templateUrl: "partials/about.html"
        })
        .state('404', {
            url: "/404",
            templateUrl: "partials/404.html"
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