//全部数据
all_data = comparedata.data
noscholardata = comparedata.nodatascholar
//比较的人数
compare_num = all_data.length
console.log(all_data)
$(function () {
    var info  ="暂无学者";
    for(var i=0;i<noscholardata.length;i++){
        info += noscholardata[i][1];
        if(i!=noscholardata.length-1){
            info +=",";
        }
    }
    info +="信息，请耐心等待学者更新或对该学者数据进行反馈!";
    if(noscholardata.length!=0){
        alert(info)
    }
    if(compare_num==0){
        window.location.href="../";
    }
})
//关系网络部分
$(document).ready(function () {
    for (i = 0;i < compare_num; i++) {
        var ec = echarts.init(document.getElementsByClassName("netcontent")[i])
        //数据组装部分
        var selfdata = {
            "name": all_data[i][1],
            "in": all_data[i][2],
            "corpnum": 100,
        }
        var partnerdata = all_data[i][13]

        var local_data = []; //结点数组
        var local_links = []; //连接数组
        var local_category = []; //种类

        //设置categories 一人一个种类，方便以不同颜色区分
        //先把中心放进去
        local_category.push({
            "name": selfdata["name"]
        })
        //合作学者放进去
        for (j = 0, len = partnerdata.length; j < len; j++) {
            local_category.push({
                "name": partnerdata[j]["name"]
            });
        }

        //设置结点data
        //先把中心放进去
        local_data.push({
            "name": selfdata["name"],
            //图形大小
            "symbolSize": 60,
            "value": selfdata["corpnum"],
            "category": selfdata["name"],
            //禁止拖动
            "draggable": false,
            "in": selfdata["in"],
        })
        //合作学者放进去
        for (j = 0, len = partnerdata.length; j < len; j++) {
            if (partnerdata[j]["name"] == selfdata["name"]) {
                continue;
            }
            local_data.push({
                "name": partnerdata[j]["name"],
                "symbolSize": 30,
                "value": partnerdata[j]["corpnum"],
                "category": partnerdata[j]["name"],
                "draggable": true,
                "in": partnerdata[j]["in"],
            });
        }

        //设置连线
        for (j = 0, len = partnerdata.length; j < len; j++) {
            if (partnerdata[j]["name"] == selfdata["name"]) {
                continue;
            }
            local_links.push({
                "source": selfdata["name"],
                "target": partnerdata[j]["name"],
                "value": partnerdata[j]["corpnum"]
            })
        }


        var option = {
            //定义提示框内容
            tooltip: {
                trigger: 'item',
                show: true,
                //  自定义提示框内容
                formatter: function (params) {
                    if (params.data.source) {//注意判断，else是将节点的文字也初始化成想要的格式
                        return params.data.source + '和' + params.data.target + '合作了' + params.data.value + '次';
                    }
                    else {
                        return '姓名：' + params.data.name + '<br/>' + '所在机构：' + params.data.in;
                    }
                }
            },
            //工具盒
            toolbox: {
                show: true,
                feature: {
                    // 重新载入
                    restore: {
                        show: true
                    },
                    //下载图片
                    saveAsImage: {
                        show: true
                    }
                }
            },
            //初始动画时长
            animationDuration: 1000,
            animationEasingUpdate: 'quinticInOut',
            series: [{
                type: 'graph',
                //力引导图
                layout: 'force',
                force: {
                    //斥力因子
                    repulsion: 500,
                    //加载动画
                    layoutAnimation: true,
                    //线的长度，根据线的value线性映射
                    edgeLength: [45, 90],
                },
                symbol: "circle",
                // 鼠标滑过线是否聚焦
                focusNodeAdjacency: true,
                // 允许缩放和拖动
                roam: true,
                //加载图表数据
                data: local_data,
                links: local_links,
                categories: local_category,
                //结点标签
                label: {
                    normal: {
                        show: true,
                        position: 'top',
                        textStyle: {
                            fontSize: 16
                        },
                        // 模板变量有 {a}, {b}，{c}，分别表示系列名，数据名，数据值
                        formatter: "{b}",
                    }
                },
                //连线样式
                lineStyle: {
                    normal: {
                        color: 'target',
                        width: 5,
                        type: "solid",
                    },

                },
                //连线标签
                edgeLabel: {
                    normal: {
                        show: true,
                        textStyle: {
                            fontSize: 14
                        },
                        formatter: "{c}次"
                    }
                },
            }]
        };
        ec.setOption(option);
    }

})


//个人画像部分
$(document).ready(function() {
    for(i=0;i<compare_num;i++){
        //数据组装
        var paint_paper_key=all_data[i][19];
        var paint_paper_num =all_data[i][20];
        var paint_scholar_school=all_data[i][2];
        var paint_scholar_name=all_data[i][1];
        var paint_scholar_college=all_data[i][3];
        var paint_scholar_field=all_data[i][5]
        var labels=[];  //个人画像的标签，目前考虑到的有：论文关键词、工作机构、学科专业、
        var max_value=0; //这里是为了取到关键词的最大value值，然后赋给学者姓名。
        // 可能会因为太大，而背景尺寸太小字数无法显示。需要修改64行的width和height。 ---2020.3.4 bwm
        //这个循环是输入论文关键词及其对应的出现次数
        for (j=0,len=paint_paper_key.length;j<len;j++){
                    labels.push({
                        "name": paint_paper_key[j],
                        "value": paint_paper_num[j],
                    });
                    if (paint_paper_num[j]>max_value){
                        max_value=paint_paper_num[j]
                    };
                }
        paint_scholar_field=paint_scholar_field.split(',')
        //下面是push进学者姓名与工作机构与研究领域
        labels.push({
          "name":paint_scholar_school,
          "value":max_value-2,
        },
            {
          "name":paint_scholar_name,
          "value":max_value,
        },
            {
          "name":paint_scholar_college,
          "value":1,
        },{
          "name":paint_scholar_field,
          "value":1,
        });
        var  ec = echarts.init(document.getElementsByClassName("personalpaintcontent")[i])
        var option = {
    tooltip: {
        show:false
    },
    toolbox: {
        show: true,
        feature: {
            restore: {
                show: true
            },
            saveAsImage: {
                show: true
            },
        },
        top: '3%',
	    right: '10%',
    },
    series: [{
        type: 'wordCloud',
        gridSize: 8,
        //大小范围随value变动
        sizeRange: [15, 40],
        rotationRange: [0, 0],
        shape: 'circle',
        roam:true,
        textStyle: {
            normal: {
                color: function() {
                    return 'rgb(' + [
                        Math.round(Math.random() * 160),
                        Math.round(Math.random() * 160),
                        Math.round(Math.random() * 160)
                    ].join(',') + ')';
                }
            },
            emphasis: {
                shadowBlur: 10,
                shadowColor: '#333'
            }
        },
        data: labels,
    }]
};
        ec.setOption(option);
    }
})



//学术成果
$(document).ready(function () {
    for (i = 0; i < compare_num; i++) {
        var ec = echarts.init(document.getElementsByClassName("visual1")[i])
        //填入数据
        var achivedata = all_data[i][11]
        var achiveyear = []
        var achivenum = []

        for (j = 0, len = achivedata.length; j < len; j++) {

            achiveyear.push(achivedata[j]["year"]);
            achivenum.push(achivedata[j]["num"]);
        }

        var option = {
            //标题内容
            //     title: {
            //     text: '1. 学术成果可视化',
            //     textStyle: {
            //     	 align: 'center',
            //         color: '#000',
            //         fontSize: 20,
            //     },
            //     top: '3%',
            //     left: '5%',
            // },
            //定义鼠标提示框内容
            tooltip: {
                show: true,
                formatter: '{b}年：{c}篇'
            },
            //工具盒
            toolbox: {
                show: true,
                feature: {
                    //重新加载
                    restore: {
                        show: true
                    },
                    //下载图片
                    saveAsImage: {
                        show: true
                    },
                },
                top: '3%',
                right: '10%',
            },
            grid: {
                top: '15%',
                right: '10%',
                left: '10%',
                bottom: '12%'
            },
            //设置横坐标轴
            xAxis: [{
                type: 'category',
                color: '#59588D',
                data: achiveyear,
                axisLabel: {
                    margin: 15,
                    color: '#000',
                    textStyle: {
                        fontSize: 16
                    },
                },
                axisLine: {
                    lineStyle: {
                        color: 'rgba(107,107,107,0.37)',
                    }
                },
                axisTick: {
                    show: false
                },
            }],
            //设置纵坐标轴
            yAxis: [{
                type: 'value',
                //坐标轴范围自适应
                scale: true,
                //坐标轴从0开始
                min: 0,
                axisLabel: {
                    show: true,
                    color: '#000',
                    textStyle: {
                        fontSize: 16
                    },
                    //自定义坐标轴标签格式
                    formatter: '{value}'
                },
                axisLine: {
                    lineStyle: {
                        color: 'rgba(107,107,107,0.37)',
                    }
                },
                axisTick: {
                    show: false
                },
                //坐标轴的分割线
                splitLine: {
                    lineStyle: {
                        color: 'rgba(131,101,101,0.2)',
                        type: 'dashed',
                    }
                }
            }],

            series: [{
                type: 'bar',
                data: achivenum,
                barWidth: '90%',
                itemStyle: {
                    normal: {
                        //设置bar颜色随数值渐变
                        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                            offset: 0,
                            color: '#ff7204' // 100% 处的颜色 #ff7204
                        }, {
                            offset: 0.75,
                            color: '#ff8d19' // 75% 处的颜色
                        }, {
                            offset: 0.5,
                            color: '#ff8c1a' // 50% 处的颜色
                        }, {
                            offset: 0.25,
                            color: '#ff934f' // 25% 处的颜色
                        }, {
                            offset: 1,
                            color: '#ffe670' // 0% 处的颜色
                        }], false),
                        barBorderRadius: [3, 3, 0, 0],
                    }
                },
                //bar的标签
                label: {
                    normal: {
                        show: true,
                        fontSize: 16,
                        fontWeight: 'bold',
                        color: '#333',
                        position: 'top',
                    }
                }
            }
            ]
        };

        ec.setOption(option);
    }

})

//引用成果
$(document).ready(function () {
    for (i = 0; i < compare_num; i++) {
        var ec = echarts.init(document.getElementsByClassName("visual2")[i])
        //填入数据
        var citeddata = all_data[i][12]
        var citedyear = []
        var citednum = []

        for (j = 0, len = citeddata.length; j < len; j++) {

            citedyear.push(citeddata[j]["year"]);
            citednum.push(citeddata[j]["num"]);
        }

        var option = {
            //     title: {
            //     text: '2. 引用可视化',
            //     textStyle: {
            //     	 align: 'center',
            //         color:'black',
            //         fontSize: 20,
            //     },
            //
            //     top: '3%',
            //     left: '5%',
            // },
            tooltip: {
                show: true,
                formatter: '{b}年：{c}次'
            },
            toolbox: {
                show: true,
                feature: {
                    restore: {
                        show: true
                    },
                    saveAsImage: {
                        show: true
                    },

                },
                top: '3%',
                right: '10%',
            },
            grid: {
                top: '15%',
                right: '10%',
                left: '10%',
                bottom: '12%'
            },
            xAxis: [{
                type: 'category',
                color: 'green',
                data: citedyear,
                axisLabel: {
                    margin: 15,
                    color: 'black',
                    textStyle: {
                        fontSize: 16
                    },
                },
                axisLine: {
                    lineStyle: {
                        color: 'rgba(107,107,107,0.37)',
                    }
                },
                axisTick: {
                    show: false
                },
            }],
            yAxis: [{
                type: 'value',
                scale: true,
                min: 0,
                axisLabel: {
                    formatter: '{value}',
                    color: 'black',
                    textStyle: {
                        fontSize: 16
                    },
                },
                axisLine: {
                    lineStyle: {
                        color: 'rgba(107,107,107,0.37)',
                    }
                },
                axisTick: {
                    show: false
                },
                splitLine: {
                    lineStyle: {
                        color: 'rgba(131,101,101,0.2)',
                        type: 'dashed',
                    }
                }
            }],
            series: [{
                type: 'bar',
                data: citednum,
                barWidth: '90%',
                itemStyle: {
                    normal: {
                        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                            offset: 0,
                            color: '#ff7204' // 100% 处的颜色 #ff7204
                        }, {
                            offset: 0.75,
                            color: '#ff8d19' // 75% 处的颜色
                        }, {
                            offset: 0.5,
                            color: '#ff8c1a' // 50% 处的颜色
                        }, {
                            offset: 0.25,
                            color: '#ff934f' // 25% 处的颜色
                        }, {
                            offset: 1,
                            color: '#ffe670' // 0% 处的颜色
                        }], false),
                        barBorderRadius: [3, 3, 0, 0],

                    }
                },
                label: {
                    normal: {
                        show: true,
                        fontSize: 16,
                        fontWeight: 'bold',
                        color: '#333',
                        position: 'top',
                    }
                }
            }
            ]
        };

        ec.setOption(option);
    }

})

//期刊分布
$(document).ready(function () {
    for (i = 0; i < compare_num; i++) {
        var ec = echarts.init(document.getElementsByClassName("visual3")[i])
        //填入数据
        var paperdata = all_data[i][10]
        var papername = [];
        var papernum = [];

        for (var key in paperdata) {
            papername.push(key);
            papernum.push(paperdata[key]);
        }

        var option = {
            //     title: {
            //     text: '2. 引用可视化',
            //     textStyle: {
            //     	 align: 'center',
            //         color:'black',
            //         fontSize: 20,
            //     },
            //
            //     top: '3%',
            //     left: '5%',
            // },
            tooltip: {
                show: true,
                formatter: '{b}：{c}篇'
            },
            toolbox: {
                show: true,
                feature: {
                    restore: {
                        show: true
                    },
                    saveAsImage: {
                        show: true
                    },

                },
                top: '3%',
                right: '10%',
            },
            grid: {
                top: '15%',
                right: '10%',
                left: '10%',
                bottom: '12%'
            },
            xAxis: [{
                type: 'category',
                color: 'green',
                data: papername,
                axisLabel: {
                    margin: 15,
                    color: 'black',
                    textStyle: {
                        fontSize: 16
                    },
                },
                axisLine: {
                    lineStyle: {
                        color: 'rgba(107,107,107,0.37)',
                    }
                },
                axisTick: {
                    show: false
                },
            }],
            yAxis: [{
                type: 'value',
                scale: true,
                min: 0,
                axisLabel: {
                    formatter: '{value}',
                    color: 'black',
                    textStyle: {
                        fontSize: 16
                    },
                },
                axisLine: {
                    lineStyle: {
                        color: 'rgba(107,107,107,0.37)',
                    }
                },
                axisTick: {
                    show: false
                },
                splitLine: {
                    lineStyle: {
                        color: 'rgba(131,101,101,0.2)',
                        type: 'dashed',
                    }
                }
            }],
            series: [{
                type: 'bar',
                data: papernum,
                barWidth: '90%',
                itemStyle: {
                    normal: {
                        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                            offset: 0,
                            color: '#ff7204' // 100% 处的颜色 #ff7204
                        }, {
                            offset: 0.75,
                            color: '#ff8d19' // 75% 处的颜色
                        }, {
                            offset: 0.5,
                            color: '#ff8c1a' // 50% 处的颜色
                        }, {
                            offset: 0.25,
                            color: '#ff934f' // 25% 处的颜色
                        }, {
                            offset: 1,
                            color: '#ffe670' // 0% 处的颜色
                        }], false),
                        barBorderRadius: [3, 3, 0, 0],

                    }
                },
                label: {
                    normal: {
                        show: true,
                        fontSize: 16,
                        fontWeight: 'bold',
                        color: '#333',
                        position: 'top',
                    }
                }
            }
            ]
        };

        ec.setOption(option);
    }

})


// 论文关键词
$(document).ready(function () {
    for (i = 0; i < compare_num; i++) {
        var ec = echarts.init(document.getElementsByClassName("visual4")[i])
        //填入数据
        var paper_key = all_data[i][19]
        var paper_key_num = all_data[i][20];
        var paper_key_data = []

        for (j = 0, len = paper_key.length; j < len; j++) {
            paper_key_data.push({
                "name": paper_key[j],
                "value": paper_key_num[j],
            });
        }

        var option = {

            tooltip: {},
            toolbox: {
                show: true,
                feature: {
                    restore: {
                        show: true
                    },
                    saveAsImage: {
                        show: true
                    },

                },
                top: '3%',
                right: '10%',
            },
            series: [{
                type: 'wordCloud',
                gridSize: 20,
                //大小范围随value变动
                sizeRange: [15, 50],
                rotationRange: [0, 0],
                shape: 'circle',
                roam: true,
                textStyle: {
                    normal: {
                        color: function () {
                            return 'rgb(' + [
                                Math.round(Math.random() * 160),
                                Math.round(Math.random() * 160),
                                Math.round(Math.random() * 160)
                            ].join(',') + ')';
                        }
                    },
                    emphasis: {
                        shadowBlur: 10,
                        shadowColor: '#333'
                    }
                },
                data: paper_key_data,
            }]
        };

        ec.setOption(option);
    }

})