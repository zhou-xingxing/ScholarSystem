var local_data = []; //节点数组
var local_links = []; //连接数组
var local_category=[]; //种类

//中心结点
center_data={
    "姓名":"三国演义",
    "value":100,
    "所在机构":"都听泽哥的"
}
// 合作结点
datalist=[{"姓名":"诸葛亮","合作次数":80,"所在机构":"蜀国"},{"姓名":"刘备","合作次数":60,"所在机构":"蜀国"},{"姓名":"曹操","合作次数":50,"所在机构":"魏国"},
{"姓名":"赵云","合作次数":40,"所在机构":"蜀国"},{"姓名":"孙权","合作次数":20,"所在机构":"吴国"},{"姓名":"张飞","合作次数":10,"所在机构":"蜀国"}]

//设置categories
function setCategory(datalist){
    //先把中心放进去
    local_category.push({
        "name":center_data["姓名"]
    })
    for (i = 0,len=datalist.length; i < len; i++){
        local_category.push({
            "name":datalist[i]["姓名"]
            });
    }
}

//设置data
function setData(datalist) {
    //先把中心放进去
    local_data.push({
        "name":center_data["姓名"],
        "symbolSize": center_data["value"],
        "value":center_data["value"],
        "category": center_data["姓名"],
        "draggable": false,
        "school":center_data["所在机构"],
    })

    for (i = 0,len=datalist.length; i < len; i++) {
        local_data.push({
            "name": datalist[i]["姓名"],
            "symbolSize": datalist[i]["合作次数"],
            "value":datalist[i]["合作次数"],
            "category": datalist[i]["姓名"],
            "draggable": true,
            "school":datalist[i]["所在机构"],
        });

    }
}

//设置links
function setLinks(datalist){
    for (i = 0,len=datalist.length; i < len; i++){
        local_links.push({
            "source":center_data["姓名"],
            "target":datalist[i]["姓名"],
            "value":datalist[i]["合作次数"]
        })
    }
}

setCategory(datalist);
setData(datalist);
setLinks(datalist);

//3.初始化echarts
$(function() {
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
                    return '姓名：'+params.data.name+'<br/>'+'所在机构：'+params.data.school;
                }
                }
    },
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
        layout: 'force',
        force: {
            repulsion: 2000,
            layoutAnimation: true,
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
                    fontSize: 15
                },
                formatter: "{b}",
            }
        },
        lineStyle: {
            normal: {
                color: 'target',
                width: 4,
                type: "solid",

            },

        },
        // 模板变量有 {a}, {b}，{c}，分别表示系列名，数据名，数据值
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
})



