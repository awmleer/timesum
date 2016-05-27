app.controller("ctrl_header",function($scope,$rootScope,$http,$state,$location) {

    $rootScope.get_userinfo=function () {
        //获取用户基本信息
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
                        type: "post",
                        headers: {'Content-Type': 'application/json'},
                        data: JSON.stringify({
                            phone: phone,
                            password:password
                        })
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
    };


    //如果是加入活动，则不会在这里请求userinfo
    if (!(/\/ac\/\d+\/join/.test($location.path()))) {
        $rootScope.get_userinfo();
    }



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


    $http({
        url: 'api/activities',
        method: 'get',
        params: {}
    }).success(function (data) {
        $scope.ac_published=data.ac_published;
        $scope.ac_participated=data.ac_participated;
        $scope.ac_published_history=data.ac_published_history;
        $scope.ac_participated_history=data.ac_participated_history;
    }).error(function () {
        alert("获取信息失败，请稍后再试");
    });

    //临时模拟的数据
    // $scope.ac_published=[
    //     {
    //         aid:21513,
    //         title:'sparker开发团队会议',
    //         opening:false,
    //         participators:[1256884,1846848,1865493],
    //         expected_number:5,
    //         published_time:1463295585807,
    //         time_determined:0
    //     },
    //     {
    //         aid:21514,
    //         title:'小组讨论',
    //         opening:true,
    //         participators:[1256884,1846848],
    //         expected_number:8,
    //         published_time:1463295585807,
    //         time_determined:[
    //             {year:2016,month:12,day:7,day_in_week:'周五',time:90},
    //             {year:2016,month:12,day:7,day_in_week:'周五',time:96}
    //         ]
    //     },
    //     {
    //         aid:555,
    //         title:'SQTP答辩',
    //         opening:true,
    //         participators:[1256884,1846848,1865493,4855556,84465],
    //         expected_number:4,
    //         published_time:1463295585807,
    //         time_determined:0
    //     }
    // ];
    //
    // $scope.ac_participated=[
    //     {
    //         aid:666,
    //         title:'sparker开发团队会议',
    //         opening:false,
    //         participators:[1256884,1846848,1865493],
    //         expected_number:5,
    //         published_time:1463295585807,
    //         time_determined:0
    //     },
    //     {
    //         aid:777,
    //         title:'小组讨论',
    //         opening:true,
    //         participators:[1256884,1846848],
    //         expected_number:8,
    //         published_time:1463295585807,
    //         time_determined:[
    //             {year:2016,month:12,day:7,day_in_week:'周五',time:90},
    //             {year:2016,month:12,day:7,day_in_week:'周五',time:90}
    //         ]
    //     },
    //     {
    //         aid:888,
    //         title:'SQTP答辩',
    //         opening:true,
    //         participators:[1256884,1846848,1865493,4855556,84465],
    //         expected_number:4,
    //         published_time:1463295585807,
    //         time_determined:0
    //     }
    // ];
    //
    // $scope.ac_published_history=[
    //     {
    //         aid:999,
    //         title:'sparker开发团队会议',
    //         time_determined:[
    //             {year:2016,month:12,day:7,day_in_week:'周五',time:90},
    //             {year:2016,month:12,day:7,day_in_week:'周五',time:90}
    //         ]
    //     },
    //     {
    //         aid:100,
    //         title:'小组讨论',
    //         time_determined:0
    //     },
    //     {
    //         aid:1999,
    //         title:'SQTP答辩',
    //         time_determined:[
    //             {year:2016,month:12,day:7,day_in_week:'周五',time:90},
    //             {year:2016,month:12,day:7,day_in_week:'周五',time:90}
    //         ]
    //     }
    // ];
    //
    // $scope.ac_participated_history=[
    //     {
    //         aid:786,
    //         title:'sparker开发团队会议',
    //         time_determined:0
    //     },
    //     {
    //         aid:7877,
    //         title:'UI设计讨论',
    //         time_determined:[
    //             {year:2016,month:12,day:7,day_in_week:'周五',time:90},
    //             {year:2016,month:12,day:7,day_in_week:'周五',time:90}
    //         ]
    //     },
    //     {
    //         aid:8888,
    //         title:'SQTP答辩',
    //         time_determined:[
    //             {year:2016,month:12,day:7,day_in_week:'周五',time:90},
    //             {year:2016,month:12,day:7,day_in_week:'周五',time:90}
    //         ]
    //     }
    // ];
});



app.controller("ctrl_new_ac",function($scope,$rootScope,$http,$state) {

    $scope.activity={
        title:'',
        description:'',
        organizer:'',
        expected_number:'',
        date_range:[],
        place:'',
        duration:''
    };

    $scope.submit_ac= function () {
        // var obj={
        //     title:$scope.title,
        //     description:$scope.description,
        //     organizer:$scope.organizer,
        //     expected_number:$scope.expected_number,
        //     date_range:$scope.date_range,
        //     place:$scope.place,
        //     duration:$scope.duration
        // };
        $http({
            url: 'api/new_ac',
            method: 'post',
            headers: {'Content-Type': 'application/json'},
            data: angular.toJson($scope.activity)
        }).success(function (data) {
            if (data.result == 'success') {
                //提醒用户跳转到时间录入界面
                if (window.confirm('添加成功，是否现在录入时间？')) {
                    $state.go('ac_time_input',{aid:data.aid});
                }else{
                    $state.go('ac_detail',{aid:data.aid});
                }
            }else{
                alert(data.message);
            }
        }).error(function () {
            alert("操作失败");
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
        console.log(obj_date);
        $scope.activity.date_range.push(obj_date);
    };

    $scope.delete_date= function () {
        $scope.activity.date_range.remove(this.date);
    }
});



app.controller("ctrl_time_input",function($scope,$rootScope,$http,$stateParams,$state) {


    $http({
        url: 'api/ac_preview',
        method: 'get',
        params: {aid:$stateParams.aid}
    }).success(function (data) {
        $scope.ac=data;

        //关于编辑的日期
        var i=0;
        $scope.time_data=$scope.ac.date_range;
        for (i = 0; i < $scope.time_data.length; i++) {
            $scope.time_data[i].timeblocks=[];
            $scope.time_data[i].clean=true;
        }
        //使用date_active来控制编辑哪一天
        $scope.date_active=0;
        $scope.time_data[0].clean=false;
        for (var j = 0; j <$scope.time_data.length ; j++) {
            for (i = 1; i <=144; i++) {
                $scope.time_data[j].timeblocks.push({time:i,status:0});
            }
        }

    }).error(function () {
        alert("获取信息失败");
    });

    //
    // $scope.ac={
    //     aid:21513,
    //     title:'sparker开发团队会议',
    //     publisher:{
    //         uid:1658165,
    //         name:'小明'
    //     },
    //     organizer:'sparker团队',
    //     place:'月牙楼元空间',
    //     duration:3,
    //     date_range:[
    //         {year:2016,month:5,day:19,day_in_week:'周四'},
    //         {year:2016,month:5,day:20,day_in_week:'周五'},
    //         {year:2016,month:5,day:20,day_in_week:'周五'},
    //         {year:2016,month:5,day:20,day_in_week:'周五'},
    //         {year:2016,month:5,day:22,day_in_week:'周日'}
    //     ],
    //     opening:true
    // };




    $scope.change_date_active= function () {
        $scope.date_active=this.$index;
        this.date.clean=false;
    };


    
    //关于时间刻度
    $scope.time_scale=2;
    $scope.scale_plus= function () {
        if ($scope.time_scale==1) {
            $scope.time_scale=2;
        }else if ($scope.time_scale==2) {
            $scope.time_scale=3;
        }else if ($scope.time_scale==3) {
            $scope.time_scale=6;
        }
    };
    $scope.scale_minus= function () {
        if ($scope.time_scale==6) {
            $scope.time_scale=3;
        }else if ($scope.time_scale==3) {
            $scope.time_scale=2;
        }else if ($scope.time_scale==2) {
            $scope.time_scale=1;
        }
    };


    
    //关于输入的时间状态
    $scope.input_status=2;
    $scope.change_input_status= function (status) {
        $scope.input_status=status;
    };
    
    
    

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
            while ($scope.time_data[$scope.date_active].timeblocks[j].time!=this.timeblock.time){
                j++;
            }
            while(j%$scope.time_scale!=0){
                j--;
            }
            var ii;
            for (ii = 0; ii < $scope.time_scale; ii++) {
                if ($scope.time_data[$scope.date_active].timeblocks[j + ii].status != $scope.input_status) {
                    $scope.time_data[$scope.date_active].timeblocks[j+ii].status=$scope.input_status;
                    flag=0;
                }
            }
            if (flag) {
                for (ii = 0; ii < $scope.time_scale; ii++) {
                    $scope.time_data[$scope.date_active].timeblocks[j+ii].status=0;
                }
            }
        }
    };


    $scope.submit_time= function () {
        // console.log(JSON.stringify($scope.time_data));
        var obj={
            aid:$scope.ac.aid,
            data:[]
        };
        for (var i = 0; i < $scope.time_data.length; i++) {
            obj.data[i]={
                date:{
                    year:$scope.time_data[i].year,
                    month:$scope.time_data[i].month,
                    day:$scope.time_data[i].day
                },
                timeblocks:''
            };
            for (var j = 0; j < $scope.time_data[i].timeblocks.length; j++) {
                obj.data[i].timeblocks+=$scope.time_data[i].timeblocks[j].status.toString();
            }
        }
        $http({
            url: 'api/time_input',
            method: 'post',
            headers: {'Content-Type': 'application/json'},
            data: JSON.stringify(obj)
        }).success(function (data) {
            if (data == 'success') {
                $state.go('time_input_done',{aid:$scope.ac.aid});
            }else {
                alert(data);
            }
        }).error(function () {
            alert("获取信息失败，请稍后再试");
        });
        
    };

    
});



app.controller("ctrl_ac_detail",function($scope,$rootScope,$http,$stateParams) {
    // alert($stateParams.aid);
    // $scope.test_id=111;

    // $scope.ac={
    //     me:{
    //         relation:'participated',
    //         time_inputed:false
    //     },
    //     aid:21513,
    //     title:'sparker开发团队会议',
    //     publisher:{
    //         uid:1658165,
    //         name:'小明'
    //     },
    //     organizer:'sparker团队',
    //     place:'月牙楼元空间',
    //     description:'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Aut beatae consectetur nisi nulla quidem saepe tempora. Ea eligendi ipsam laborum praesentium ullam? Itaque iure laborum, laudantium porro quisquam vel voluptatibus?',
    //     duration:13,
    //     date_range:[
    //         {year:2016,month:5,day:19,day_in_week:'周四'},
    //         {year:2016,month:5,day:20,day_in_week:'周四'}
    //     ],
    //     opening:false,
    //     history:false,
    //     participators:[
    //         {
    //             uid:186115,
    //             name:'aaa',
    //             time_inputed:true,
    //             attendable:2
    //         },
    //         {
    //             uid:164866,
    //             name:'bbb',
    //             time_inputed:false,
    //             attendable:0
    //         }
    //     ],
    //     expected_number:5,
    //     published_time:1463295585807,
    //     time_determined:13584846,
    //     comments:[
    //         {"uid":165156,"name":'小明',"time":1463295585807,"text":"lorem afaefqgjqpog"},
    //         {"uid":165861,"name":'小华',"time":1463295585807,"text":"lorem qeee"}
    //     ]
    // };

    //获取活动详情
    $http({
        url: 'api/ac_detail',
        method: 'get',
        params: {aid: $stateParams.aid}
    }).success(function (data) {
        $scope.ac=data;
    }).error(function () {
        alert("获取信息失败，请稍后再试");
    });

    $scope.submit_comment= function () {
        if ($scope.my_comment=='' || $scope.my_comment==undefined) {
            alert("留言内容不能为空");
            return;
        }
        $http({
            url: 'api/submit_comment',
            method: 'get',
            params: {aid:$scope.ac.aid,comment:$scope.my_comment}
        }).success(function (data) {
            if (data == 'success') {
                location.reload();
            }else {
                alert(data);
            }
        }).error(function () {
            alert("操作失败");
        });

    }


});



app.controller("ctrl_ac_recommend",function($scope,$rootScope,$http,$stateParams) {
    $scope.aid=$stateParams.aid;
});


app.controller("ctrl_time_input_done",function($scope,$rootScope,$http,$stateParams) {
    $scope.aid=$stateParams.aid;
});



app.controller("ctrl_ac_invite",function($scope,$rootScope,$location,$http,$stateParams) {
    $scope.aid=$stateParams.aid;
    console.log($scope.aid);
});


app.controller("ctrl_ac_join",function($scope,$rootScope,$location,$http,$stateParams,$state) {

    $scope.is_signed=false;
    $scope.phone_checked=false;
    $scope.already_login=false;


    $http({
        url: 'api/userinfo',
        method: 'get',
        params: {}
    }).success(function (data) {
        $scope.already_login=true;
        $rootScope.userinfo=data;
    }).error(function (data,status) {
        if (status == 401) {//如果是unauthorized
            //webstorge获取暂存的用户名和密码，并且尝试自动登录
            var phone=store.get('phone');
            var password=store.get('password');
            if (phone&&password) {
                $http({
                    url: 'api/login',
                    method: 'post',
                    headers: {'Content-Type': 'application/json'},
                    data: JSON.stringify({
                        phone: phone,
                        password: password
                    })
                }).success(function (data) {
                    if (data == 'success') {
                        location.reload();
                    }else{
                        $scope.already_login=false;
                    }
                }).error(function () {
                    $scope.already_login=false;
                });
            }else {
                $scope.already_login=false;
            }
        }else{
            alert("获取用户个人信息失败，请稍后再试");
        }
    });


    $http({
        url: 'api/ac_preview',
        method: 'get',
        params: {aid:$stateParams.aid}
    }).success(function (data) {
        $scope.ac=data;
    }).error(function () {
        alert("获取信息失败");
    });

    
    $scope.phone_check= function () {
        if (/^1[0-9]\d{9}$/.test($scope.phone)) {
            $http({
                url: 'api/is_signed',
                method: 'get',
                params: {phone:$scope.phone}
            }).success(function (data) {
                if (data==true || data==false) {
                    $scope.is_signed=data;
                    $scope.phone_checked=true;
                }else{
                    alert(data);
                }
            }).error(function () {
                alert("抱歉，服务器出错了，请您过一会儿再来试试");
            });
        }
    };
    

    //直接加入活动
    $scope.join= function () {
        $http({
            url: 'api/ac_join',
            method: 'get',
            params: {aid:$scope.ac.aid}
        }).success(function (data) {
            if (data == 'success') {
                //提醒用户跳转到时间录入界面
                if (window.confirm('加入成功，是否现在录入时间？')) {
                    $state.go('ac_time_input',{aid:$scope.ac.aid});
                }else{
                    $state.go('ac_detail',{aid:$scope.ac.aid});
                }
            }else {
                alert(data);
            }
        }).error(function () {
            alert("获取信息失败，请稍后再试");
        });
    };

    //登录并加入活动
    $scope.login_join= function () {
        //先调用登录的接口
        $.ajax({
            url: "api/login",
            type: "post",
            headers: {'Content-Type': 'application/json'},
            data: JSON.stringify({
                phone: $scope.phone,
                password:$scope.password
            })
        }).done(function (data) {
            if (data == 'success') {
                //存储用户账号密码
                store.set('phone', phone);
                store.set('password',password);
                //登录成功后，获取userinfo
                $rootScope.get_userinfo();
                //然后加入活动
                $scope.join();
            }else if (data == 'wrong password') {
                alert("您输入的密码错误");
                $("#password").val('').focus();
            }else if (data == 'wrong phone') {
                alert("您输入的手机号尚未注册");
                $("#phone").val('').focus();
                $("#password").val('');
            }else {
                alert(data);
            }
        }).fail(function () {
            alert("请求失败");
        });
    };

    //注册并加入活动
    $scope.signup_join= function () {
        //先调用注册的接口
        $.ajax({
            url: "api/signup",
            type: "post",
            contentType : 'application/json',
            data: JSON.stringify({
                phone:$scope.phone,
                name:$scope.name,
                password:$scope.password,
                code:$scope.code
            })
        }).done(function (data) {
            if (data == "success") {
                //存储用户账号密码
                store.set('phone', phone);
                store.set('password',password);
                //注册成功后，获取userinfo
                $rootScope.get_userinfo();
                //然后加入活动
                $scope.join();
            } else {
                alert(data);
            }
        }).fail(function () {
            alert("请求失败");
        });
    };


});