var app = angular.module('timesum', ['ui.router']);


app.config(function($stateProvider, $urlRouterProvider){
    /*路由模块*/
    $urlRouterProvider
        .otherwise("/404")
        .when('', '/home')
        .when('/ac/:ac_id', '/ac/:ac_id/join');
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
        .state('ac_edit', {
            url: "/ac/:ac_id/edit",
            templateUrl: "partials/ac_edit.html",
            controller:'ctrl_ac_edit'
        })
        .state('ac_invite', {
            url: "/ac/:ac_id/invite",
            templateUrl: "partials/ac_invite.html",
            controller:'ctrl_ac_invite'
        })
        .state('time_input', {
            url: "/time_input",
            templateUrl: "partials/time_input.html",
            controller:'ctrl_time_input'
        })
        .state('time_input_done', {
            url: "/time_input_done",
            templateUrl: "partials/time_input_done.html",
            controller:'ctrl_time_input_done'
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


app.run(['$rootScope', '$window', '$location', '$log', function ($rootScope, $window, $log,$http) {
    //监听location的变化，实时更新path变量
    // var locationChangeSuccessOff = $rootScope.$on('$locationChangeSuccess', locationChangeSuccess);
    // function locationChangeSuccess(event) {
    //     $rootScope.path=$location.path();
    // }
    
}]);