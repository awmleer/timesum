app.controller("ctrl_header",function($scope,$rootScope,$http,$state,$location,$window) {

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
    if (!(/\/ac\/\d+\/join/.test($location.path()) || /\/ac\/\d+/.test($location.path())) ) {
        $rootScope.get_userinfo();
    }

    // $scope.window=$window;



});



app.controller("ctrl_userinfo",function($scope,$rootScope,$http) {
    $scope.NameChgDivVisible = false;
    $rootScope.get_userinfo();
    $scope.NameChgVisibleToogle = function () {
        $scope.NameChgDivVisible = !$scope.NameChgDivVisible;
    }
    $scope.CommitNameChg = function () {
        $http({
            url: 'api/change_name',
            method: 'get',
            params: {name: $scope.name_changed}
        }).success(function (data) {
            if (data == 'success') {
                alert("操作成功！");
                $scope.NameChgDivVisible = false;
                $scope.name_changed='';
                $scope.get_userinfo();
            }else {
                alert(data);
            }
        }).error(function () {
            alert("操作失败");
        });
    }

    //退出登录
    $scope.logout=function () {
        //api logout
        $http({
            url: 'api/logout',
            method: 'get',
            params: {}
        }).success(function (data) {
            if (data == 'success') {
                //清除local storage
                store.remove('phone');
                store.remove('password');
                location.href="login.html";
            }else {
                alert(data);
            }
        }).error(function () {
            alert("操作失败");
        });
    }
    //
    // $scope.CommitPwdChg = function () {
    //     if ($scope.pwdchg.newpwd == $scope.pwdchg.newpwdcfm) {
    //         $http({
    //             url: 'api/changepwd',
    //             method: 'post',
    //             headers: {'Content-Type': 'application/json'},
    //             data: JSON.stringify({
    //                 uid: $rootScope.userinfo.uid,
    //                 name:$rootScope.userinfo.name
    //             })
    //         }).success(function (data) {
    //             if (data == 'success') {
    //                 alert("操作成功！");
    //                 $scope.NameChgDivVisible = false;
    //             }
    //         }).error(function () {
    //             alert("操作失败");
    //         });
    //     }
    //     else {
    //         alert("两次输入的密码不一致！");
    //     }
    // }
});



app.controller("ctrl_changepwd",function($scope,$rootScope,$http,$state) {

    $scope.CommitPwdChg = function () {
        if ($scope.password_new == $scope.password_confirm) {
            $http({
                url: 'api/changepwd',
                method: 'post',
                headers: {'Content-Type': 'application/json'},
                data: JSON.stringify({
                    pwd_old: $scope.password_old,
                    pwd_new:$scope.password_new
                })
            }).success(function (data) {
                if (data == 'success') {
                    alert("操作成功！");
                    $state.go('home');
                }else{
                    alert(data);
                }
            }).error(function () {
                alert("操作失败");
            });
        }
        else {
            alert("两次输入的密码不一致");
        }
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
        alert("获取活动列表失败");
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
        console.log($scope.activity.date_range);
        if ($scope.activity.duration==0) {
            alert("请设置活动的预计时长");
            return;
        }
        if ( $scope.activity.date_range.length==0 ) {
            alert("请设置活动的可能进行日期");
            return;
        }
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

    };

    $scope.change_duration= function (value) {
        if (value==1) {
            $scope.activity.duration++;
        }else if (value == -1) {
            if ($scope.activity.duration>0) $scope.activity.duration--;
        }
    };

    $scope.setDateTime= function (current_date) {
        var obj_date={
            year:moment(current_date).format("YYYY"),
            month:moment(current_date).format("M"),
            day:moment(current_date).format("D")
        };
        //判断日期是否已经存在
        var already_has=_.find($scope.activity.date_range,obj_date);
        if (already_has)return;//如果是，直接退出函数
        //加入日期
        $scope.activity.date_range.push(obj_date);
    };

    $scope.delete_date= function () {
        _.remove($scope.activity.date_range,this.date);
    }

});



app.controller("ctrl_ac_edit",function($scope,$rootScope,$http,$stateParams,$state) {

    $http({
        url: 'api/ac_preview',
        method: 'get',
        params: {aid:$stateParams.aid}
    }).success(function (data) {
        $scope.activity={
            aid:data.aid,
            title:data.title,
            description:data.description,
            organizer:data.organizer,
            expected_number:data.expected_number,
            // date_range:[],//暂时不允许修改date_range
            place:data.place,
            duration:data.duration
        };
        // angular.forEach(data.date_range, function (date,i, array) {
        //     $scope.date_range.push({
        //         year:date.year,
        //         month:date.month,
        //         day:date.day
        //     })
        // });
    }).error(function () {
        alert("获取活动信息失败");
    });
    
    $scope.edit_ac= function () {
        if ($scope.activity.duration==0) {
            alert("请设置活动的预计时长");
            return;
        }
        $http({
            url: 'api/edit_ac',
            method: 'post',
            headers: {'Content-Type': 'application/json'},
            data: angular.toJson($scope.activity)
        }).success(function (data) {
            if (data == 'success') {
                $state.go('ac_detail',{aid:$scope.activity.aid});
            }else{
                alert(data);
            }
        }).error(function () {
            alert("操作失败");
        });
    };

    $scope.change_duration= function (value) {
        if (value==1) {
            $scope.activity.duration++;
        }else if (value == -1) {
            if ($scope.activity.duration>0) $scope.activity.duration--;
        }
    };
    
});



app.controller("ctrl_time_input",function($scope,$rootScope,$http,$stateParams,$state) {

    $http({
        url: 'api/timeblocks',
        method: 'get',
        params: {aid:$stateParams.aid}
    }).success(function (data) {
        $scope.ac=data;

        //关于编辑的日期
        var i=0;
        $scope.time_data=$scope.ac.date_range;
        var timeblock_temp;
        for (i = 0; i < $scope.time_data.length; i++) {
            timeblock_temp=$scope.time_data[i].timeblocks;
            $scope.time_data[i].timeblocks=[];
            $scope.time_data[i].clean=true;
            for (var j = 1; j <=144; j++) {
                $scope.time_data[i].timeblocks.push({time:j,status:timeblock_temp.charAt(j-1)});
            }
        }
        //使用date_active来控制编辑哪一天
        $scope.date_active=0;
        $scope.time_data[0].clean=false;
        if ($scope.ac.time_inputed) {
            for (var ii = 1; ii < $scope.time_data.length; ii++) {
                $scope.time_data[ii].clean=false;
            }
        }

    }).error(function () {
        alert("获取信息失败");
    });


    $scope.change_date_active= function () {
        $scope.date_active=this.$index;
        this.d.clean=false;
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
        var obj={
            aid:$scope.ac.aid,
            data:$scope.time_data
        };
        // for (var i = 0; i < $scope.time_data.length; i++) {
        //     obj.data[i]={
        //         date:{
        //             year:$scope.time_data[i].date.year,
        //             month:$scope.time_data[i].date.month,
        //             day:$scope.time_data[i].date.day
        //         },
        //         timeblocks:''
        //     };
        //     for (var j = 0; j < 144; j++) {
        //         obj.data[i].timeblocks+=$scope.time_data[i].timeblocks[j].status.toString()+'t';
        //     }
        //     obj.data[i].timeblocks=obj.data[i].timeblocks.replace(/t/g,'');
        //     if (obj.data[i].timeblocks.length != 144) {
        //         alert("数据长度出现问题");
        //     }
        // }
        $http({
            url: 'api/time_input',
            method: 'post',
            headers: {'Content-Type': 'application/json'},
            data: angular.toJson(obj)
        }).success(function (data) {
            if (data == 'success') {
                $state.go('time_input_done',{aid:$scope.ac.aid});
            }else {
                alert(data);
            }
        }).error(function () {
            alert("操作失败");
        });
        
    };

    $scope.go_back= function () {
        $("#icon_help").popover('destroy');
        $(".help_pop").popover('destroy');
        $state.go("ac_detail",{aid:$scope.ac.aid});
    }

});



app.controller("ctrl_ac_detail",function($scope,$rootScope,$http,$stateParams,$state) {
    $rootScope.loading=true;
    //获取活动详情
    $scope.get_ac_detail= function () {
        $http({
            url: 'api/ac_detail',
            method: 'get',
            params: {aid: $stateParams.aid}
        }).success(function (data) {
            $scope.ac=data;
            if (!$scope.ac.me.time_inputed) {
                //显示未输入时间的提示，并且三秒后自动消失
                setTimeout("$('#btn_input_time').popover().popover('show');",800);
                setTimeout("$('#btn_input_time').popover('destroy');",3800);
            }
        }).error(function () {
            alert("获取活动详情失败");
        });
    }
    $scope.get_ac_detail();


    $scope.delete_ac=function () {
        if (window.confirm("确定要删除这个活动吗？")) {
            $http({
                url: 'api/delete_ac',
                method: 'get',
                params: {aid:$scope.ac.aid}
            }).success(function (data) {
                if (data == 'success') {
                    alert("删除成功");
                    $state.go('home');
                }else{
                    alert(data);
                }
            }).error(function () {
                alert("获取信息失败，请稍后再试");
            });
        }
    };


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
                $scope.get_ac_detail();
                $scope.my_comment='';
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
    $http({
        url: 'api/time_recommend',
        method: 'get',
        params: {aid:$scope.aid}
    }).success(function (data) {
        $scope.recs=data;
        angular.forEach($scope.recs, function (rec, i , array) {
            rec.list_showing=false;
        });
        // console.log($scope.recs);
    }).error(function () {
        alert("获取活动失败，请稍后再试");
    });

    $scope.toggle_list_showing= function () {
        this.rec.list_showing=!this.rec.list_showing;
    }
    
    
});



app.controller("ctrl_ac_time_table",function($scope,$rootScope,$http,$stateParams) {
    $scope.aid=$stateParams.aid;


    //临时模拟数据
    $http({
        url: 'api/time_collection',
        method: 'get',
        params: {aid:$scope.aid}
    }).success(function (data) {
        $scope.ac=data;
        $scope.time_table=[];
        angular.forEach($scope.ac.time_collection, function (person, i, array) {
            $scope.time_table.push({
                name:person.name,
                uid:person.uid,
                periods:[]
            });
            angular.forEach(person.data, function(data,ii,array){
                // console.log(data.timeblocks);
                var timeblocks=data.timeblocks;
                // console.log(ii);
                var flag=0;
                var start;
                var end;
                for (var j = 0; j < 144 ; j++) {
                    if (flag != 0) {
                        if (timeblocks.charAt(j)!=flag) {
                            end=j;
                            $scope.time_table[i].periods.push({
                                month:data.date.month,
                                day:data.date.day,
                                start:start,
                                end:end,
                                status:flag
                            });
                            start=j;
                            flag=timeblocks.charAt(j);
                        }
                    }else {
                        if (timeblocks.charAt(j)!=0) {
                            flag=timeblocks.charAt(j);
                            start=j;
                        }
                    }
                }
            });
        })
    }).error(function () {
        alert("获取信息失败，请稍后再试");
    });
    // $scope.ac={
    //     aid:43,
    //     "time_collection" : [
    //         {
    //             "uid" : 8,
    //             name:'小明',
    //             "data" : [
    //                 {
    //                     "date" : {
    //                         "year" : "2017",
    //                         "month" : "5",
    //                         "day" : "10",
    //                         day_in_week:'周一'
    //                     },
    //                     "timeblocks" : "000000000011112222222200000000000000000001111111100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
    //                 },
    //                 {
    //                     "date" : {
    //                         "year" : "2016",
    //                         "month" : "5",
    //                         "day" : "29",
    //                         day_in_week:'周一'
    //                     },
    //                     "timeblocks" : "000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
    //                 }
    //             ]
    //         },
    //         {
    //             "uid" : 5,
    //             name:'小华',
    //             "data" : [
    //                 {
    //                     "date" : {
    //                         "year" : "2017",
    //                         "month" : "5",
    //                         "day" : "10",
    //                         day_in_week:'周一'
    //                     },
    //                     "timeblocks" : "000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
    //                 },
    //                 {
    //                     "date" : {
    //                         "year" : "2016",
    //                         "month" : "5",
    //                         "day" : "29",
    //                         day_in_week:'周一'
    //                     },
    //                     "timeblocks" : "000000000000002200220022000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
    //                 }
    //             ]
    //         }
    //     ]
    // };


    

    // for (var i in $scope.ac.time_collection) {
    //
    // }
    // console.log($scope.time_table);
    
    
});



app.controller("ctrl_ac_determine",function($scope,$rootScope,$http,$stateParams,$state) {
    $scope.aid=$stateParams.aid;
    $scope.time_determined=[
        {
            year:'',
            month:'',
            day:'',
            time:''
        },
        {
            year:'',
            month:'',
            day:'',
            time:''
        }
    ];

    $scope.select_date= function (index) {
        $scope.index=index;
    };
    $scope.setDateTime= function (current_date) {
        $scope.time_determined[$scope.index].year=moment(current_date).format("YYYY");
        $scope.time_determined[$scope.index].month=moment(current_date).format("M");
        $scope.time_determined[$scope.index].day=moment(current_date).format("D");
        $scope.time_determined[$scope.index].time=(moment(current_date).format("H")*6+Math.floor(moment(current_date).format("m")/10)).toString();

        // if ($scope.index==0) {
        //     $scope.time_determined[1].year=moment(current_date).format("YYYY");
        //     $scope.time_determined[1].month=moment(current_date).format("M");
        //     $scope.time_determined[1].day=moment(current_date).format("D");
        //     $scope.time_determined[$scope.index].time=moment(current_date).format("H")*6+moment(current_date).format("m")/10;
        // }
    };
    $scope.select_date= function (index) {
        $scope.index=index;
    };
    $scope.commit_determine= function () {

        $http({
            url: 'api/determine_time',
            method: 'post',
            headers: {'Content-Type': 'application/json'},
            data: JSON.stringify({
                aid:$scope.aid,
                time_determined:eval(angular.toJson($scope.time_determined))
            })
        }).success(function (data) {
            if (data == 'success') {
                alert("时间确定成功");
                $state.go('home');
            }else {
                alert(data);
            }
        }).error(function () {
            alert("获取信息失败，请稍后再试");
        });
    }

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
        if (/^1\d{10}$/.test($scope.phone)) {
            $http({
                url: 'api/is_signed',
                method: 'get',
                params: {phone:$scope.phone}
            }).success(function (data) {
                if (data=='true' || data=='false') {
                    if (data == 'true') {
                        $scope.is_signed=true;
                    }else{
                        $scope.is_signed=false;
                    }
                    $scope.phone_checked=true;
                }else{
                    alert(data);
                }
                console.log($scope.is_signed);
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
            alert("操作失败");
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

