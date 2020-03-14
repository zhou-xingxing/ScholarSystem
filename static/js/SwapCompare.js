//从jinjia2传入对比学者的数据包括姓名、成功列表、引用列表、所有学者成果及引用的最小年份、最大年份
compare_all_name=compare_data.com_all_name;
compare_achivement_list=compare_data.com_achivement_list;
compare_achivement_list2=compare_data.com_achivement_list2;
compare_cited_list=compare_data.com_cited_list;
compare_achive_minyear=compare_data.com_achive_minyear;
compare_achive_maxyear=compare_data.com_achive_maxyear;
compare_cited_minyear=compare_data.com_cited_minyear;
compare_cited_maxyear=compare_data.com_cited_maxyear;
//共有成果数量时间
compare_achive_year=[];
for(i=compare_achive_minyear;i<=compare_achive_maxyear;i++){
    compare_achive_year.push(i);
}
// 共有引用数量时间
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
    };
    compare_paper_data.push(a)
}
$(function() {
    //切换对比模式的按钮响应事件，
    $("#comparescholar").click(function() {
        layer.open({
            type:1,
            title:"学者对比",
            area:["900px","700px"],
            content: $('#partnercompare')
        });
    });
    //响应对比合作学者每个按钮的点击事件--成果会议
     $("#partnerbtn1").click(function() {
        $("#partnerCompare1")[0].style.display = "block";
        $("#partnerCompare2")[0].style.display = "none";
        $("#partnerCompare3")[0].style.display = "none";
    });
      //响应对比合作学者每个按钮的点击事件--引用
    $("#partnerbtn2").click(function() {
        $("#partnerCompare1")[0].style.display = "none";
        $("#partnerCompare2")[0].style.display = "block";
        $("#partnerCompare3")[0].style.display = "none";
    });
    //响应对比合作学者每个按钮的点击事件--期刊会议
     $("#partnerbtn3").click(function() {
        $("#partnerCompare1")[0].style.display = "none";
        $("#partnerCompare2")[0].style.display = "none";
        $("#partnerCompare3")[0].style.display = "block";
    });
    //初始化echarts，对三个表格进行数据填充
        var  ec1 = echarts.init(document.getElementById('partnerCompare1'));
        var  ec2 = echarts.init(document.getElementById('partnerCompare2'));
        var  ec3 = echarts.init(document.getElementById('partnerCompare3'));
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
            series:compare_paper_data
};
        ec1.setOption(option1);
        ec2.setOption(option2);
        ec3.setOption(option3);
        window.addEventListener("resize",function (){
            ec1.resize();
            ec2.resize();
            ec3.resize();
            // ec4.resize();
        });
}
);