var app = angular.module('timesum', ['ui.router']);

app.filter('timeblock', function () {
    return function (input, capitalize_index, specified_char) {

        var output;
        var minute=input%6;
        var hour=(input-minute)/6;
        if (minute == 0) {
            minute='00';
        }else {
            minute=minute*10;
        }
        output=hour+':'+minute;
        return output;
    };
});

app.config(function($stateProvider, $urlRouterProvider){
    /*路由模块*/
    $urlRouterProvider
        .otherwise("/404")
        .when('', '/home')
        .when('/ac/:aid', '/ac/:aid/join');
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
            url: "/ac/:aid/detail",
            templateUrl: "partials/ac_detail.html",
            controller:'ctrl_ac_detail'
        })
        .state('ac_recommend', {
            url: "/ac/:aid/recommend",
            templateUrl: "partials/ac_recommend.html",
            controller:'ctrl_ac_recommend'
        })
        .state('ac_edit', {
            url: "/ac/:aid/edit",
            templateUrl: "partials/ac_edit.html",
            controller:'ctrl_ac_edit'
        })
        .state('ac_invite', {
            url: "/ac/:aid/invite",
            templateUrl: "partials/ac_invite.html",
            controller:'ctrl_ac_invite'
        })
        .state('ac_join', {
            url: "/ac/:aid/join",
            templateUrl: "partials/ac_join.html",
            controller:'ctrl_ac_join'
        })
        .state('ac_time_input', {
            url: "/ac/:aid/time_input",
            templateUrl: "partials/time_input.html",
            controller:'ctrl_time_input'
        })
        .state('time_input_done', {
            url: "/ac/:aid/time_input_done",
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


app.run(['$rootScope', '$window', '$location','$state', '$log', function ($rootScope, $window,$location,$state, $log,$http) {


    //监听location的变化，实时更新path变量
    var locationChangeSuccessOff = $rootScope.$on('$locationChangeSuccess', locationChangeSuccess);
    function locationChangeSuccess(event) {
        $rootScope.path=$location.path();
        var path=$location.path();
        if (path=='/home') {
            $rootScope.header_text='活动列表';
        }else if (path=='/new_ac') {
            $rootScope.header_text='创建活动';
        }else if (/\/ac\/\d+\/detail/.test(path)) {
            $rootScope.header_text='活动详情';
        }else if (/\/ac\/\d+\/edit/.test(path)) {
            $rootScope.header_text='修改活动';
        }else if (/\/ac\/\d+\/invite/.test(path)) {
            $rootScope.header_text='邀请加入';
        }else if (/\/ac\/\d+\/join/.test(path)) {
            $rootScope.header_text='加入活动';
        }else if (path=='/time_input_done') {
            $rootScope.header_text='录入完成';
        }else if (path=='/about') {
            $rootScope.header_text='关于';
        }else if (path=='/userinfo') {
            $rootScope.header_text='个人信息';
        }else if (path=='/changepwd') {
            $rootScope.header_text='修改密码';
        }else if (path=='/404') {
            $rootScope.header_text='页面不存在';
        }else{
            $rootScope.header_text='　';
        }
    }


}]);

