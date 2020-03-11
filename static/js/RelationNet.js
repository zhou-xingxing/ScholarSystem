//从后台传入的当前学者数据
var center_data=rela_center.data;
//从后台传入的其合作学者数据
var datalist=rela_partner.data;


var local_data = []; //结点数组
var local_links = []; //连接数组
var local_category=[]; //种类



//设置categories 一人一个种类，方便以不同颜色区分
function setCategory(datalist){
    //先把中心放进去
    local_category.push({
        "name":center_data["name"]
    });
    //合作学者放进去
    for (i = 0,len=datalist.length; i < len; i++){
        local_category.push({
            "name":datalist[i]["name"]
            });
    }
}

//设置结点data
function setData(datalist) {
    //先把中心放进去
    local_data.push({
        "name":center_data["name"],
        //图形大小
        "symbolSize": 100,
        "value":center_data["corpnum"],
        "category": center_data["name"],
        //禁止拖动
        "draggable": false,
        "in":center_data["in"],
    });
    //合作学者放进去
    for (i = 0,len=datalist.length; i < len; i++) {
        local_data.push({
            "name": datalist[i]["name"],
            "symbolSize": 55,
            "value":datalist[i]["corpnum"],
            "category": datalist[i]["name"],
            "draggable": true,
            "in":datalist[i]["in"],
        });
    }
}

//设置连线links
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

//初始化echarts
function draw () {
    var ec = echarts.init(document.getElementById('RelationNet'));
    //配置option
    var option = {
        //标题
        title: {
        text: "学者关系网络",
        subtext: "通过鼠标和滚轮可以实现拖动和缩放",
        top: "top",
        left: "left",
        textStyle: {
            color: '#000000',
            fontSize:20
        }
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
            repulsion: 800,
            //加载动画
            layoutAnimation: true,
            //线的长度，根据线的value线性映射
            edgeLength: [70, 140],
        },
        symbol:"circle",
        // 鼠标滑过线是否聚焦
         focusNodeAdjacency: true,
        // 允许缩放和拖动
        roam: true,
        //加载图表数据
        data: local_data,
        links: local_links,
        categories:local_category,
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
    //设置option
    ec.setOption(option);
    window.onresize  = ec.resize
}



