//加载第一个图表数据
var achivelist = data.achive
var achiveyear = []
var achivenum =[]

//加载第二个图表数据
var citedlist = data.cited
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
        //3.初始化echarts
        var  ec1 = echarts.init(document.getElementById('8_main1'))
        var  ec2= echarts.init(document.getElementById('8_main2'))
        var  ec3= echarts.init(document.getElementById('8_main3'))
        var  ec4= echarts.init(document.getElementById('8_main4'))

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
        //4.配置option
        //<!--可视化模块：成果可视化findResultByWD-->
        var option1 = {
            title: {
	        text: '1. 学术成果可视化',
	        textStyle: {
	        	 align: 'center',
	            color: '#000',
	            fontSize: 20,
	        },
	        top: '3%',
	        left: '10%',
	    },
        backgroundColor: '#fff',
        grid: {
            top: '15%',
            right: '10%',
            left: '10%',
            bottom: '12%'
        },
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
        yAxis: [{
            min: 0,
            max: 100,
            axisLabel: {
                formatter: '{value}%',
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
            barWidth: '50px',
            itemStyle: {
                normal: {
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                        offset: 0,
                        color: '#FF9A22' // 0% 处的颜色
                    }, {
                        offset: 1,
                        color: '#FFD56E' // 100% 处的颜色
                    }], false),
                    barBorderRadius: [30, 30, 0, 0],
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
        },{
            data: achivenum,
            type: 'line',
            smooth: true,
            name: '折线图',
            symbol: 'none',
            lineStyle: {
                color: '#3275FB',
                width: 4,
                shadowColor: 'rgba(0, 0, 0, 0.3)',//设置折线阴影
                shadowBlur: 15,
                shadowOffsetY: 20,
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
	        left: '10%',
	    },
    backgroundColor: '#fff',
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
        min: 0,
        max: 100,
        axisLabel: {
            formatter: '{value}%',
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
        barWidth: '50px',
        itemStyle: {
            normal: {
                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                    offset: 0,
                    color: '#d3e4ff' // 0% 处的颜色
                }, {
                    offset: 1,
                    color: '#0f4aff' // 100% 处的颜色
                }], false),
                barBorderRadius: [30, 30, 0, 0],
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
    },{
        data: citednum,
        type: 'line',
        smooth: true,
        name: '折线图',
        symbol: 'none',
        lineStyle: {
            color: '#f1c93b',
            width: 4,
            shadowColor: 'rgba(0, 0, 0, 0.3)',//设置折线阴影
            shadowBlur: 15,
            shadowOffsetY: 20,
        }
    }
]
};
        //<!--可视化模块：论文会议分布可视化findPaperDistributeByWD-->
        var charts = { // 按顺序排列从大到小
            cityList: ['SCI', '北大核心期刊', 'CSCD期刊数', '中国科技核心', '其他期刊数'],
            cityData: [7500, 6200, 5700, 4200, 3500]
        }
        var top10CityList = charts.cityList
        var top10CityData = charts.cityData
        var color = ['rgba(248,195,248', 'rgba(100,255,249', 'rgba(135,183,255', 'rgba(248,195,248', 'rgba(100,255,249']
        let lineY = []
        for (var i = 0; i < charts.cityList.length; i++) {
            var x = i
            if (x > color.length - 1) {
                x = color.length - 1
            }
            var data = {
    name: charts.cityList[i],
    color: color[x] + ')',
    value: top10CityData[i],
    itemStyle: {
      normal: {
        show: true,
        color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [{
          offset: 0,
          color: color[x] + ', 0.3)'
        }, {
          offset: 1,
          color: color[x] + ', 1)'
        }], false),
        barBorderRadius: 10
      },
      emphasis: {
        shadowBlur: 15,
        shadowColor: 'rgba(0, 0, 0, 0.1)'
      }
    }
  }
            lineY.push(data)
        }
        console.log(lineY)
        var option3= {
            title: {
	        text: '3. 论文分布情况',
	        textStyle: {
	        	 align: 'center',
	            color:'black',
	            fontSize: 20,
	        },
	        top: '3%',
	        left: '10%',
	    },
    backgroundColor:'#fff',
  tooltip: {
    trigger: 'item'
  },
  grid: {
    borderWidth: 0,
    top: '10%',
    left: '5%',
    right: '15%',
    bottom: '3%'
  },
  color: color,
  yAxis: [{
    type: 'category',
    inverse: true,
    axisTick: {
      show: false
    },
    axisLine: {
      show: false
    },
    axisLabel: {
      show: false,
      inside: false
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
        fontSize: '14',
        fontFamily: 'PingFangSC-Regular'
      },
      formatter: function (val) {
        return `${val}k`
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
  xAxis: {
    type: 'value',
    axisTick: {
      show: false
    },
    axisLine: {
      show: false
    },
    splitLine: {
      show: false
    },
    axisLabel: {
      show: false
    }
  },
  series: [{
    name: '',
    type: 'bar',
    zlevel: 2,
    barWidth: '10px',
    data: papernum,
    animationDuration: 1500,
    label: {
      normal: {
        color: '#000',
        show: true,
        position: [0, '-24px'],
        textStyle: {
          fontSize: 16
        },
        formatter: function (a, b) {
          return a.name
        }
      }
    }
  }],
  animationEasing: 'cubicOut'
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
	        left: '10%',
	    },
    tooltip: {},
    series: [{
        type: 'wordCloud',
        gridSize: 20,
        sizeRange: [12, 50],
        rotationRange: [0, 0],
        shape: 'circle',
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
        //5.设置option
        ec1.setOption(option1)
        ec2.setOption(option2)
        ec3.setOption(option3)
        ec4.setOption(option4)
    })




