app.controller("ctrl_header",function($scope,$rootScope,$location,$http) {
    // /*获取用户基本信息*/
    // $http({
    //     url: 'api/userinfo',
    //     method: 'get',
    //     params: {}
    // }).success(function (data) {
    //     $rootScope.userinfo=data;
    // }).error(function (data,status) {
    //     if (status == 401) {//如果是unauthorized
    //         alert("您还没有登录");
    //         location.href="login.html";//就跳转到登录页面
    //     }else{
    //         alert("获取用户个人信息失败，请稍后再试");
    //     }
    // });


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


app.controller("ctrl_home",function($scope,$rootScope,$location,$http) {
    $scope.ac_published=[
        {
            aid:21513,
            title:'sparker开发团队会议',
            opening:false,
            participators:[1256884,1846848,1865493],
            expected_number:5,
            published_time:1463295585807,
            time_determined:0
        },
        {
            aid:21513,
            title:'小组讨论',
            opening:true,
            participators:[1256884,1846848],
            expected_number:8,
            published_time:1463295585807,
            time_determined:1463395585807
        },
        {
            aid:21513,
            title:'SQTP答辩',
            opening:true,
            participators:[1256884,1846848,1865493,4855556,84465],
            expected_number:4,
            published_time:1463295585807,
            time_determined:0
        }
    ];

    $scope.ac_participated=[
        {
            aid:21513,
            title:'sparker开发团队会议',
            opening:false,
            participators:[1256884,1846848,1865493],
            expected_number:5,
            published_time:1463295585807,
            time_determined:0
        },
        {
            aid:21513,
            title:'小组讨论',
            opening:true,
            participators:[1256884,1846848],
            expected_number:8,
            published_time:1463295585807,
            time_determined:[1463396585807,1463497585807]
        },
        {
            aid:21513,
            title:'SQTP答辩',
            opening:true,
            participators:[1256884,1846848,1865493,4855556,84465],
            expected_number:4,
            published_time:1463295585807,
            time_determined:0
        }
    ];

    $scope.ac_published_history=[
        {
            aid:21513,
            title:'sparker开发团队会议',
            time_determined:[1463297585807,1463497585807]
        },
        {
            aid:21513,
            title:'小组讨论',
            time_determined:0
        },
        {
            aid:21513,
            title:'SQTP答辩',
            time_determined:[1463295685807,1463497585807]
        }
    ];

    $scope.ac_participated_history=[
        {
            aid:21513,
            title:'sparker开发团队会议',
            time_determined:0
        },
        {
            aid:21513,
            title:'UI设计讨论',
            time_determined:[1463396585807,1463497585807]
        },
        {
            aid:21513,
            title:'SQTP答辩',
            time_determined:[1463295685807,1463497585807]
        }
    ];
});


app.controller("ctrl_new_ac",function($scope,$rootScope,$location,$http) {
    
});