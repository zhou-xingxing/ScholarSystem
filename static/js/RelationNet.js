var center_data={};
var datalist=[];

center_data={
    "name":"罗贯中",
    //这个值没有实际意义，但必须要有，可以给每个中心点设一固定值
    "corpnum":100,
    "in":"三国",
}
// 合作学者结点
datalist=[{"name":"诸葛亮","corpnum":80,"in":"蜀国"},{"name":"刘备","corpnum":60,"in":"蜀国"},{"name":"曹操","corpnum":50,"in":"魏国"},
{"name": "关羽", "corpnum": 50, "in": "蜀国"},{"name":"赵云","corpnum":40,"in":"蜀国"},{"name":"孙权","corpnum":20,"in":"吴国"},{"name":"张飞","corpnum":10,"in":"蜀国"}]

//需要从html获取数据
function fillRelation(center,datalist){
    center_data=center;
    datalist=datalist;
}


var local_data = []; //结点数组
var local_links = []; //连接数组
var local_category=[]; //种类

//中心学者结点



//设置categories 一人一个种类，方便以不同颜色区分
function setCategory(datalist){
    //先把中心放进去
    local_category.push({
        "name":center_data["name"]
    })
    for (i = 0,len=datalist.length; i < len; i++){
        local_category.push({
            "name":datalist[i]["name"]
            });
    }
}

//设置data
function setData(datalist) {
    //先把中心放进去
    local_data.push({
        "name":center_data["name"],
        //图形大小
        "symbolSize": center_data["corpnum"],
        "value":center_data["corpnum"],
        "category": center_data["name"],
        //禁止拖动
        "draggable": false,
        "in":center_data["in"],
    })

    for (i = 0,len=datalist.length; i < len; i++) {
        local_data.push({
            "name": datalist[i]["name"],
            "symbolSize": datalist[i]["corpnum"],
            "value":datalist[i]["corpnum"],
            "category": datalist[i]["name"],
            "draggable": true,
            "in":datalist[i]["in"],
        });

    }
}

//设置links
function setLinks(datalist){
    for (i = 0,len=datalist.length; i < len; i++){
        local_links.push({
            "source":center_data["name"],
            "target":datalist[i]["name"],
            "value":datalist[i]["corpnum"]
        })
    }
}
//调用填充函数
setCategory(datalist);
setData(datalist);
setLinks(datalist);
// local_data, local_links,local_category
//3.初始化echarts
function draw () {
    var ec = echarts.init(document.getElementById('RelationNet'))
    //4.配置option
    var option = {
    title: {
        text: "学者关系网络",
        top: "top",
        left: "center"
    },
    //定义提示框内容
    tooltip: {
         trigger:'item',
         show:true,
        //  自定义提示框内容
         formatter:function(params){
                if (params.data.source) {//注意判断，else是将节点的文字也初始化成想要的格式
                   return params.data.source + '和' + params.data.target + '合作了'+ params.data.value+'次';
                }
                else {
                    return '姓名：'+params.data.name+'<br/>'+'所在机构：'+params.data.in;
                }
                }
    },
    //工具盒
    toolbox: {
        show: true,
        feature: {
            dataView: {
                show: false,
                readOnly: true
            },
            restore: {
                show: true
            },
            saveAsImage: {
                show: true
            }
        }
    },
    animationDuration: 1000,
    animationEasingUpdate: 'quinticInOut',
    series: [{
        type: 'graph',
        //力引导图
        layout: 'force',
        force: {
            //斥力因子
            repulsion: 2000,
            //加载动画
            layoutAnimation: true,
            //线的长度，根据线的value线性映射
            edgeLength: [100, 300],
        },
        symbol:"circle",
        // 鼠标滑过聚焦
         focusNodeAdjacency: true,
        // 允许缩放和拖动
        roam: true,

        data: local_data,
        links: local_links,
        categories:local_category,

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
        lineStyle: {
            normal: {
                color: 'target',
                width: 5,
                type: "solid",
            },

        },
        edgeLabel: {
            normal: {
                show: true,
                textStyle: {
                    fontSize: 14
                },
                formatter: "{c}"
            }
        },
    }]
};
    //5.设置option
    ec.setOption(option)
}



