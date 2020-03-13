//新关系网络
//中心学者姓名
var center_name=rela_center.data["name"];
//同学校学者姓名
var same_school=new_rela_partner.same_school_partner;
//同论文学者姓名
var same_paper=new_rela_partner.same_paper_partner;

$(document).ready(function() {
        var  myChart = echarts.init(document.getElementById("NewRelationNet"));
        //预装基本数据
        var graph={
            "nodes":[
                {
            "name": center_name,
            "category": "当前学者",
            "symbolSize": 70,
        },
        {
            "name": "学校",
            "category": "学校",
            "symbolSize": 40,
        },
        {
            "name": "论文",
            "category": "论文",
            "symbolSize": 40,
        },
            ],
            "links":[
                {
            "source": center_name,
            "target": "学校"
        },
        {
            "source": center_name,
            "target": "论文"
        },
            ]
        };
        //装载同学校数据
    for(i=0,len=same_school.length;i<len;i++){
        tmp={
            "name":same_school[i],
            "category": "学校",
            "symbolSize": 55,
            "draggable":true,
        };
        tmp2={
            "source": "学校",
            "target": same_school[i],
        };
        graph["nodes"].push(tmp);
        graph["links"].push(tmp2);
    }

    //装载同论文数据
    for(i=0,len=same_paper.length;i<len;i++){
        tmp={
            "name":same_paper[i],
            "category": "论文",
            "symbolSize": 55,
            "draggable":true,
        };
        tmp2={
            "source": "论文",
            "target": same_paper[i],
        };
        graph["nodes"].push(tmp);
        graph["links"].push(tmp2);
    }



const defaultCategory = "当前学者";
const graphTitle = "学者关系网络";
const currentGraph = {
    nodes: {},
    links: {},
};
const nodeMap = {};
// 页面加载时，第一次初始化图
function init() {
    // 根据定义的常量，产生currentGraph的默认数据
    // 遍历全部nodes和links，产生node映射map
    for (let i = 0; i < graph.nodes.length; i++) {
        if (graph.nodes[i].category === defaultCategory) {
            currentGraph.nodes[graph.nodes[i].name] = graph.nodes[i];
        }
        nodeMap[graph.nodes[i].name] = graph.nodes[i];
        nodeMap[graph.nodes[i].name]['links'] = {};
        nodeMap[graph.nodes[i].name]['nodes'] = {};
        nodeMap[graph.nodes[i].name]['hasAppend'] = false;
    }
    for (let i = 0; i < graph.links.length; i++) {
        let link = graph.links[i];
        if (nodeMap[link.source] !== undefined && nodeMap[link.target] !== undefined) {
            nodeMap[link.source].links[link.target] = link;
            nodeMap[link.source].nodes[nodeMap[link.target].name] = nodeMap[link.target];
        }
    }

    for (let i = 0; i < graph.nodes.length; i++) {
        graph.nodes[i].itemStyle = null;
        graph.nodes[i].label = {
            normal: {
                show: graph.nodes[i].symbolSize > 15
            }
        };
    }
    redrawGraph();
}
// 处理点击节点展开
function append(nodeName) {
    // 根据nodeName从nodeMap里拿出对应的nodes和links，并append到currentGraph.nodes currentGraph.links
    let node = nodeMap[nodeName];
    if (node.hasAppend === true || Object.keys(node.nodes).length === 0 || Object.keys(node.links).length === 0) {
         alert("无法继续展开");
        return
    }
    Object.values(node.nodes).forEach(n => {
        currentGraph.nodes[n.name] = n;
    });
    Object.values(node.links).forEach(l => {
        currentGraph.links[l.source + "_" + l.target] = l;
    });
    node.hasAppend = true;
    redrawGraph();
}
// 处理点击节点收缩
function remove(nodeName) {
    //根据nodeName从nodeMap里拿出对应的nodes和links，从currentGraph.nodes currentGraph.links删除当前节点的nodes和links并且递归
    let node = nodeMap[nodeName];
    Object.values(node.nodes).forEach(n => {
        delete currentGraph.nodes[n.name];
        if (n.hasAppend === true && Object.keys(n.nodes).length > 0) {
            remove(n.name);
        }
    });
    Object.values(node.links).forEach(l => {
        delete currentGraph.links[l.source + '_' + l.target];
    });
    // 设置flag 等于false
    node.hasAppend = false;

    redrawGraph();
}
// 根据更新后的option重新画图
function redrawGraph() {
    option.series[0].data = Object.values(currentGraph.nodes);
    option.series[0].links = Object.values(currentGraph.links);
    // console.log(option);
    myChart.setOption(option);
}
const option = {
    title: {
        text: graphTitle,
        subtext: "点击节点可以展开或折叠",
        top: "top",
        left: "left",
        textStyle: {
            color: '#000000',
            fontSize:20
        },
        subtextStyle:{
                color:'#242424',
                fontSize:16,
            }
    },
    tooltip: {
        show:true,
        formatter:'{b}'
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
    legend: [],
    animation: false,
    series: [{
        type: 'graph',
        layout: 'force',
        data: Object.values(currentGraph.nodes),
        links: Object.values(currentGraph.links),
        categories: [{
                name: '当前学者',
                itemStyle: {
                    color: '#3869af'
                },
            },
            {
                name: '学校',
                itemStyle: {
                    color: '#71b67d'
                },

            },
            {
                name: '论文',
                itemStyle: {
                    color: '#c23531'
                },
            },
        ],
        roam: true,
        focusNodeAdjacency: false,
        itemStyle: {
            normal: {
                borderColor: '#fff',
                borderWidth: 1,
                shadowBlur: 10,
                shadowColor: 'rgba(0, 0, 0, 0.3)'
            }
        },
        label: {
            position: 'inside',
            formatter: '{b}'
        },
        lineStyle: {
            normal: {
                color: 'source',
                width: 3,
                type: "solid",
            },
        },
        emphasis: {
            lineStyle: {
                width: 5
            }
        },
        force: {
            layoutAnimation: false,
            repulsion: 800
        }
    }]
};
    init();
    //处理点击事件
    myChart.on('click', function(params) {
        if (params.dataType === "node") {
            const node = nodeMap[params.data.name];
            if (node.hasAppend === true) {
                remove(node.name)
            } else {
                append(node.name);
            }
        }
    });




});
