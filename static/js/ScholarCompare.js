$(function() {
    $("#comparescholar").click(function() {
        //利用ajax请求参数
        partner_list=compare_data.partnerlist;
        console.log(partner_list);
        //初始化echarts
        var  ec1 = echarts.init(document.getElementById('partnerCompare1'));
        var  ec2 = echarts.init(document.getElementById('partnerCompare2'));
        var  ec3 = echarts.init(document.getElementById('partnerCompare3'));
        //加载图表前的loading动画
        ec1.showLoading();
        layer.open({
            type:1,
            title:"学者对比",
            area:["900px","700px"],
            content: $('#partnercompare')
        });
        $.ajax({
            url:'/compare',
            type:'GET',
            data:{'partner':JSON.stringify(partner_list) },
            success:function(compare_ans){
                compare_ans = eval('('+compare_ans+')');
                compare_all_name=compare_ans['all_name'];
                compare_achivement_list=compare_ans['achivement_list'];
                compare_achivement_list2=compare_ans['achivement_list2'];
                compare_cited_list=compare_ans['cited_list'];
                compare_achive_minyear=compare_ans['achive_minyear'];
                compare_achive_maxyear=compare_ans['achive_maxyear'];
                compare_cited_minyear=compare_ans['cited_minyear'];
                compare_cited_maxyear=compare_ans['cited_maxyear'];
                compare_achive_minyear=parseInt(compare_achive_minyear);
                compare_achive_maxyear=parseInt(compare_achive_maxyear);
                compare_cited_minyear=parseInt(compare_cited_minyear);
                compare_cited_maxyear=parseInt(compare_cited_maxyear);
                //共有成果数量时间
                compare_achive_year=[];
                for(i=compare_achive_minyear;i<=compare_achive_maxyear;i++){
                    compare_achive_year.push(i);
                }
                //共有引用数量时间
                compare_cited_year=[];
                for(i=compare_cited_minyear;i<=compare_cited_maxyear;i++){
                    compare_cited_year.push(i);
                }
                //加载第一个对比图表数据-学术成果
                compare_achive_data=[];
                for(i=0;i<compare_all_name.length;i++){
                    dd=[];
                    //先把共有时间内数量都填空
                    for(j=compare_achive_minyear;j<=compare_achive_maxyear;j++){
                        dd.push(null)
                    }
                    //再把有数据的填上
                    for(j=0;j<compare_achivement_list2[i].length;j++){
                        k=compare_achivement_list2[i][j];
                        dd[k['year']-compare_achive_minyear]=k['num']
                    }
                    a={
                        name:compare_all_name[i],
                        type:'line',
                        data:dd,
                        smooth: true,
                         lineStyle: {
                            type:'solid',
                            width: 3,
                            shadowColor: 'rgba(0, 0, 0, 0.5)',
                            shadowBlur: 6,
                            shadowOffsetY:6,
                        }
                    };
                    compare_achive_data.push(a)
                }

                //加载第二个对比图表数据-引用数量
                compare_cited_data=[];
                for(i=0;i<compare_all_name.length;i++){
                    dd=[];
                    //先把共有时间内数量都填空
                    for(j=compare_cited_minyear;j<=compare_cited_maxyear;j++){
                        dd.push(null)
                    }
                    //再把有数据的填上
                    for(j=0;j<compare_cited_list[i].length;j++){
                        k=compare_cited_list[i][j];
                        dd[k['year']-compare_cited_minyear]=k['num']
                    }
                    a={
                        name:compare_all_name[i],
                        type:'line',
                        data:dd,
                        smooth: true,
                        lineStyle: {
                            type:'solid',
                            width: 3,
                            shadowColor: 'rgba(0, 0, 0, 0.5)',
                            shadowBlur: 6,
                            shadowOffsetY:6,
                        }
                    };
                    compare_cited_data.push(a)
                }
                //加载第三个对比图表数据-期刊
                compare_paper_name=['北大核心期刊','其他期刊数','其他会议数', '其他', '中国科技核心', '专著','SSCI期刊数', 'SCI期刊数', 'SCIE期刊数', 'EI期刊数','CSSCI期刊数','CSCD期刊数'];
                compare_paper_data=[];
                for(i=0;i<compare_all_name.length;i++){
                    dd=[];
                    //把有数据的填上
                    for(j=0;j<compare_paper_name.length;j++){
                        name_key=compare_paper_name[j];
                        if(compare_achivement_list[i].hasOwnProperty(name_key)){
                            dd.push(compare_achivement_list[i][name_key])
                        }
                        else{
                            dd.push(0)
                        }
                    }
                    a={
                        name:compare_all_name[i],
                        type:'line',
                        data:dd,
                        smooth: true,
                        lineStyle: {
                            type:'solid',
                            width: 3,
                            shadowColor: 'rgba(0, 0, 0, 0.5)',
                            shadowBlur: 6,
                            shadowOffsetY:6,
                        }
                    };
                    compare_paper_data.push(a)
                }
                var option1 = {
                    title: {
                        text: '学术成果对比'
                    },
                    tooltip: {
                        trigger: 'axis'
                    },
                    legend: {
                        data: compare_all_name
                    },
                    grid: {
                        left: '3%',
                        right: '3%',
                        bottom: '3%',
                        containLabel: true
                    },
                    toolbox: {
                        feature: {
                            saveAsImage: {}
                        }
                    },
                    xAxis: {
                        type: 'category',
                        boundaryGap: false,
                        data: compare_achive_year,
                    },
                    yAxis: {
                        type: 'value'
                    },
                    //坐标轴伸缩，可拖动，可滚轮
                    dataZoom:[
                        {
                            type:'slider',
                            show:true,
                            xAxisIndex:[0],
                            start:40,
                            end:100
                        },
                         {
                            type:'inside',
                            show:true,
                            xAxisIndex:[0],
                            start:40,
                            end:100
                        }
                    ],
                    series:compare_achive_data
                };
                var option2 = {
                    title: {
                        text: '引用数量对比'
                    },
                    tooltip: {
                        trigger: 'axis'
                    },
                    legend: {
                        data: compare_all_name
                    },
                    grid: {
                        left: '3%',
                        right: '3%',
                        bottom: '3%',
                        containLabel: true
                    },
                    toolbox: {
                        feature: {
                            saveAsImage: {}
                        }
                    },
                    xAxis: {
                        type: 'category',
                        boundaryGap: false,
                        data: compare_cited_year,
                    },
                    yAxis: {
                        type: 'value'
                    },
                    dataZoom:[
                        {
                            type:'slider',
                            show:true,
                            xAxisIndex:[0],
                            start:40,
                            end:100
                        },
                         {
                            type:'inside',
                            show:true,
                            xAxisIndex:[0],
                            start:40,
                            end:100
                        }
                    ],
                    series:compare_cited_data
                };
                var option3 = {
                    title: {
                        text: '期刊对比'
                    },
                    tooltip: {
                        trigger: 'axis'
                    },
                    legend: {
                        data: compare_all_name
                    },
                    grid: {
                        left: '3%',
                        right: '3%',
                        bottom: '3%',
                        containLabel: true
                    },
                    toolbox: {
                        feature: {
                            saveAsImage: {}
                        }
                    },
                    xAxis: {
                        type: 'category',
                        boundaryGap: false,
                        data: compare_paper_name,
                    },
                    yAxis: {
                        type: 'value'
                    },
                    dataZoom:[
                        {
                            type:'slider',
                            show:true,
                            xAxisIndex:[0],
                            start:40,
                            end:100
                        },
                         {
                            type:'inside',
                            show:true,
                            xAxisIndex:[0],
                            start:40,
                            end:100
                        }
                    ],
                    series:compare_paper_data
                 };
                ec1.hideLoading();
                ec1.setOption(option1);
                ec2.setOption(option2);
                ec3.setOption(option3);
                window.addEventListener("resize",function (){
                    ec1.resize();
                    ec2.resize();
                    ec3.resize();

                });
            }
        });
    })
});







