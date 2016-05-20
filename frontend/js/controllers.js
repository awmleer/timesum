app.controller("ctrl_header",function($scope,$rootScope,$http,$state) {
    /*获取用户基本信息*/
    $http({
        url: 'api/userinfo',
        method: 'get',
        params: {}
    }).success(function (data) {
        $rootScope.userinfo=data;
    }).error(function (data,status) {
        if (status == 401) {//如果是unauthorized
            //webstorge获取暂存的用户名和密码，并且尝试自动登录
            var phone=store.get('phone');
            var password=store.get('password');
            if (phone&&password) {
                $.ajax({
                    url: "api/login",
                    type: "get",
                    data: {
                        phone: phone,
                        password:password
                    }
                }).done(function (data) {
                    if (data == 'success') {
                        location.reload();
                    }else{
                        location.href='login.html';
                    }
                }).fail(function () {
                    location.href='login.html';
                });
            }else {
                alert("您还没有登录");
                location.href="login.html";//就跳转到登录页面
            }
        }else{
            alert("获取用户个人信息失败，请稍后再试");
        }
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


app.controller("ctrl_home",function($scope,$rootScope,$http,$state) {
    //历史活动相关
    $scope.ac_published_history_showing=false;
    $scope.ac_participated_history_showing=false;
    $scope.ac_published_history_toggle= function () {
        $scope.ac_published_history_showing=!$scope.ac_published_history_showing;
    };
    $scope.ac_participated_history_toggle= function () {
        $scope.ac_participated_history_showing=!$scope.ac_participated_history_showing;
    };

    //进入活动详情页面
    $scope.ac_detail= function () {
        $state.go('ac_detail',{ac_id:this.ac.aid});
    };
    


    //临时模拟的数据
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



app.controller("ctrl_new_ac",function($scope,$rootScope,$http) {
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



app.controller("ctrl_time_input",function($scope,$rootScope,$http) {
    $scope.timeblocks=[];
    for (var i = 1; i <=144; i++) {
        $scope.timeblocks.push({time:i,status:0});
    }

    $scope.time_scale=1;
    $scope.input_status=1;

    $scope.select_time= function () {
        if ($scope.time_scale==1) {
            if (this.timeblock.status == $scope.input_status) {
                this.timeblock.status=0;
            }else {
                this.timeblock.status=$scope.input_status;
            }
        }else{
            var j=0;
            var flag=1;
            while ($scope.timeblocks[j].time!=this.timeblock.time){
                j++;
            }
            while(j%$scope.time_scale!=0){
                j--;
            }
            var ii;
            for (ii = 0; ii < $scope.time_scale; ii++) {
                if ($scope.timeblocks[j + ii].status != $scope.input_status) {
                    $scope.timeblocks[j+ii].status=$scope.input_status;
                    flag=0;
                }
            }
            if (flag) {
                for (ii = 0; ii < $scope.time_scale; ii++) {
                    $scope.timeblocks[j+ii].status=0;
                }
            }
        }
    }
    
    
});



app.controller("ctrl_ac_detail",function($scope,$rootScope,$http,$stateParams) {
    // alert($stateParams.ac_id);
    // $scope.test_id=111;

    $scope.ac={
        me:{
            relation:'participated',
            time_inputed:false
        },
        aid:21513,
        title:'sparker开发团队会议',
        publisher:{
            uid:1658165,
            name:'小明'
        },
        organizer:'sparker团队',
        place:'月牙楼元空间',
        description:'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Aut beatae consectetur nisi nulla quidem saepe tempora. Ea eligendi ipsam laborum praesentium ullam? Itaque iure laborum, laudantium porro quisquam vel voluptatibus?',
        expected_duration:3,
        date_range:[
            {year:2016,month:5,day:19},
            {year:2016,month:5,day:20}
        ],
        opening:false,
        participators:[
            {
                uid:186115,
                name:'aaa',
                time_inputed:true,
                attendable:2
            },
            {
                uid:164866,
                name:'bbb',
                time_inputed:false,
                attendable:0
            }
        ],
        expected_number:5,
        published_time:1463295585807,
        time_determined:13584846,
        comments:[
            {"uid":165156,"name":'小明',"time":1463295585807,"text":"lorem afaefqgjqpog"},
            {"uid":165861,"name":'小华',"time":1463295585807,"text":"lorem qeee"}
        ]
    }
});