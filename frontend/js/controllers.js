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
    $scope.ac_published_history_showing=false;
    $scope.ac_participated_history_showing=false;
    
    $scope.ac_published_history_toggle= function () {
        $scope.ac_published_history_showing=!$scope.ac_published_history_showing;
    };

    $scope.ac_participated_history_toggle= function () {
        $scope.ac_participated_history_showing=!$scope.ac_participated_history_showing;
    };
    
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
    $scope.dates=[];

    $scope.submit_ac= function () {
        var obj={
            title:$scope.title,
            description:$scope.description,
            organizer:$scope.organizer,
            expected_number:$scope.expected_number,
            date_range:$scope.dates
        };
        $http({
            url: 'api/new_ac',
            method: 'post',
            headers: {'Content-Type': 'application/json'},
            data: JSON.stringify(obj)
        }).success(function (data) {
            if (data.result == 'success') {
                alert("添加成功");
            }else{
                alert(data.message);
            }
        }).error(function () {
            alert("获取信息失败，请稍后再试");
        });
        console.log($scope.description);

    };

    $scope.setDateTime= function (current_date) {
        //TODO 判断日期是否已经存在了

        var obj_date={
            year:moment(current_date).format("YYYY"),
            month:moment(current_date).format("M"),
            day:moment(current_date).format("D")
        };
        $scope.dates.push(obj_date);
    };

    $scope.delete_date= function () {
        $scope.dates.remove(this.date);
    }
});



app.controller("ctrl_time_input",function($scope,$rootScope,$location,$http) {
    $scope.times=[];
    for (var i = 0; i < 240; i++) {
        $scope.times.push(i);
    }
    
});



app.controller("ctrl_ac_detail",function($scope,$rootScope,$location,$http,$stateParams) {
    // alert($stateParams.ac_id);
    // $scope.test_id=111;

});