//加载第一个图表数据
var achivelist = data.cited
var achiveyear = []
var achivenum =[]

//加载第二个图表数据
var citedlist = data.achive
var citedyear = []
var citednum =[]

//加载第三个图表数据
var paper=data.paper;
var papername=[];
var papernum=[];

//加载第四个图表数据
var paper_key=data.paper_search_key;
var paper_num =data.paper_search_num;
var paper_data=[]

$(function() {
        //初始化echarts
        var  ec1 = echarts.init(document.getElementById('8_main1'))
        var  ec2= echarts.init(document.getElementById('8_main2'))
        var  ec3= echarts.init(document.getElementById('8_main3'))
        var  ec4= echarts.init(document.getElementById('8_main4'))
        //填充为图表可用数据格式
        for(i=0,len=achivelist.length;i<len;i++){

            achiveyear.push(achivelist[i]["year"]);
            achivenum.push(achivelist[i]["num"]);
        }

         for(i=0,len=citedlist.length;i<len;i++){

            citedyear.push(citedlist[i]["year"]);
            citednum.push(citedlist[i]["num"]);
        }

        for(var key in paper){
            papername.push(key);
            papernum.push(paper[key]);
        }

        for (i=0,len=paper_key.length;i<len;i++){
            paper_data.push({
                "name": paper_key[i],
                "value": paper_num[i],
            });
        }
        //配置option
        //<!--可视化模块：成果可视化findResultByWD-->
        var option1 = {
            //标题内容
            title: {
	        text: '1. 学术成果可视化',
	        textStyle: {
	        	 align: 'center',
	            color: '#000',
	            fontSize: 20,
	        },
	        top: '3%',
	        left: '5%',
	    },
            //定义鼠标提示框内容
            tooltip:{
                show:true,
                formatter:'{b}年：{c}篇'
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
            top:'3%',
            right:'10%',
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
                margin: 20,
                color: '#000',
                textStyle: {
                    fontSize: 18
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
            type:'value',
            //坐标轴范围自适应
            scale:true,
            //坐标轴从0开始
            min:0,
            axisLabel: {
                show:true,
                color: '#000',
                textStyle: {
                    fontSize: 18
                },
                //自定义坐标轴标签格式
                formatter:'{value}'
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
                    },{
                        offset: 0.5,
                        color:'#ff8c1a' // 50% 处的颜色
                    }, {
                        offset: 0.25,
                        color:'#ff934f' // 25% 处的颜色
                    }, {
                        offset: 1,
                        color:'#ffe670' // 0% 处的颜色
                    }], false),
                    barBorderRadius: [3, 3, 0, 0],
                }
            },
            //bar的标签
            label: {
                normal: {
                    show: true,
                    fontSize: 18,
                    fontWeight: 'bold',
                    color: '#333',
                    position: 'top',
                }
            }
        }
    ]
    };
        //<!--可视化模块：引用可视化findQuationByWD-->
        var option2 = {
            title: {
	        text: '2. 引用可视化',
	        textStyle: {
	        	 align: 'center',
	            color:'black',
	            fontSize: 20,
	        },

	        top: '3%',
	        left: '5%',
	    },
            tooltip:{
                show:true,
                formatter:'{b}年：{c}次'
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
        top:'3%',
        right:'10%',
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
            margin: 20,
            color: 'black',
            textStyle: {
                fontSize: 18
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
        type:'value',
        scale:true,
        min: 0,
        axisLabel: {
            formatter: '{value}',
            color: 'black',
            textStyle: {
                fontSize: 18
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
                    },{
                        offset: 0.5,
                        color:'#ff8c1a' // 50% 处的颜色
                    }, {
                        offset: 0.25,
                        color:'#ff934f' // 25% 处的颜色
                    }, {
                        offset: 1,
                        color:'#ffe670' // 0% 处的颜色
                    }], false),
                    barBorderRadius: [3, 3, 0, 0],
                    //     offset: 0,
                //     color: '#ff7204' // 100% 处的颜色
                // }, {
                //     offset: 1,
                //     color: '#ffe670' // 0% 处的颜色
                // }], false),
                // barBorderRadius: [30, 30, 0, 0],
            }
        },
        label: {
            normal: {
                show: true,
                fontSize: 18,
                fontWeight: 'bold',
                color: '#333',
                position: 'top',
            }
        }
    }
]
};
        //<!--可视化模块：论文会议分布可视化findPaperDistributeByWD-->

        var option3= {
            title: {
	        text: '3. 论文分布情况',
	        textStyle: {
	        	 align: 'center',
	            color:'black',
	            fontSize: 20,
	        },
	        top: '3%',
	        left: '5%',
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
        top:'3%',
        right:'10%',
    },
  tooltip: {
    trigger: 'item',
    formatter:'{c}篇'
  },
  grid: {
    borderWidth: 0,
    top: '10%',
    left: '5%',
    right: '15%',
    bottom: '3%'
  },
  color: '#ff4d1e',
  //两个纵坐标轴
  yAxis: [{
    type: 'category',
    axisTick: {
      show: false
    },
    axisLine: {
      show: false
    },
    axisLabel: {
      show: true,
      inside: false,
        //自定义坐标轴标签
        formatter: function (val) {
        return `${val}`
      },
        textStyle: {
        color: '#000',
        fontSize: '16',
        fontFamily: 'PingFangSC-Regular'
      },
    },
    data: papernum
  }, {
    type: 'category',
    axisLine: {
      show: false
    },
    axisTick: {
      show: false
    },
    axisLabel: {
      show: true,
      inside: false,
      textStyle: {
        color: '#000',
        fontSize: '16',
        fontFamily: 'PingFangSC-Regular'
      },
      formatter: function (val) {
        return `${val}`
      }
    },
    splitArea: {
      show: false
    },
    splitLine: {
      show: false
    },
    data: papername
  }],
  // 横坐标轴
  xAxis: {
    type: 'value',
    axisTick: {
      show: false
    },
    axisLine: {
      show: true
    },
    splitLine: {
      show: true
    },
    axisLabel: {
      show: true
    }
  },

  series: [{
    name: '',
    type: 'bar',
    barWidth: '15px',
    data: papernum,
    label: {
      normal: {
        color: '#000',
        show: false,
      }
    }
  }],
  // animationEasing: 'cubicOut'
};
        //<!--可视化模块：论文关键词可视化findDirectionByWD-->
        var option4 = {
    title: {
	        text: '4. 论文关键词词云',
	        textStyle: {
	        	 align: 'center',
	            color: '#000',
	            fontSize: 20,
	        },
	        top: '3%',
	        left: '5%',
	    },
    tooltip: {

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
        gridSize: 20,
        //大小范围随value变动
        sizeRange: [15, 50],
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
        data: paper_data,
    }]
};
        //设置option
        ec1.setOption(option1)
        ec2.setOption(option2)
        ec3.setOption(option3)
        ec4.setOption(option4)

        window.addEventListener("resize",function (){
            ec1.resize();
            ec2.resize();
            ec3.resize();
            ec4.resize();
        });
    })




