app.controller("ctrl_header",function($scope,$rootScope,$location,$http) {
    /*获取用户基本信息*/
    $http({
        url: 'api/userinfo',
        method: 'get',
        params: {}
    }).success(function (data) {
        $rootScope.userinfo=data;
    }).error(function (data,status) {
        if (status == 401) {//如果是unauthorized
            alert("您还没有登录");
            location.href="login.html";//就跳转到登录页面
        }else{
            alert("获取用户个人信息失败，请稍后再试");
        }
    });


    /*APP多页面通用信息的获取*/
    // 获取分组列表
    $http({
        url: 'api/group_list',
        method: 'get',
        params: {}
    }).success(function (data) {
        $rootScope.group_list=data;
    }).error(function () {
        alert("获取分组列表失败，请稍后再试");
    });
    //获取全部成员列表
    $http({
        url: 'api/crew_list',
        method: 'get',
        params: {}
    }).success(function (data) {
        $rootScope.crew_list=data;
    }).error(function () {
        alert("获取成员列表失败，请稍后再试");
    });


    /*退出登录*/
    $scope.logout=function () {
        //api logout
        $http({
            url: 'api/logout',
            method: 'get',
            params: {}
        }).success(function (data) {
            if (data == 'success') {
                location.href="login.html";
            }
        }).error(function () {
            alert("获取信息失败，请稍后再试");
        });
    }

});

