//从jinjia2传入数据
compare_all_name=compare_data.com_all_name
compare_achivement_list=compare_data.com_achivement_list
compare_achivement_list2=compare_data.com_achivement_list2
compare_cited_list=compare_data.com_cited_list
compare_achive_minyear=compare_data.com_achive_minyear
compare_achive_maxyear=compare_data.com_achive_maxyear
compare_cited_minyear=compare_data.com_cited_minyear
compare_cited_maxyear=compare_data.com_cited_maxyear

// compare_all_name=['周东华', '何潇']
// compare_achivement_list=[{'其他': '11', '专著': '17', '其他会议数': '126', '北大核心期刊': '147', 'CSCD期刊数': '142', '中国科技核心': '156', 'SCI期刊数': '85', 'EI期刊数': '135', 'SCIE期刊数': '138', '其他期刊数': '120'}, {'其他': '3', '专著': '3', '北大核心期刊': '13', 'CSCD期刊数': '14', '中国科技核心': '13', 'SCI期刊数': '24', 'EI期刊数': '43', 'SCIE期刊数': '39', '其他期刊数': '32'}]
// compare_achivement_list2=[[{'year': 1990, 'num': 5}, {'year': 1991, 'num': 5}, {'year': 1992, 'num': 6}, {'year': 1993, 'num': 3}, {'year': 1994, 'num': 6}, {'year': 1995, 'num': 4}, {'year': 1996, 'num': 4}, {'year': 1997, 'num': 3}, {'year': 1998, 'num': 9}, {'year': 1999, 'num': 11}, {'year': 2000, 'num': 16}, {'year': 2001, 'num': 18}, {'year': 2002, 'num': 20}, {'year': 2003, 'num': 27}, {'year': 2004, 'num': 32}, {'year': 2005, 'num': 31}, {'year': 2006, 'num': 31}, {'year': 2007, 'num': 29}, {'year': 2008, 'num': 24}, {'year': 2009, 'num': 30}, {'year': 2010, 'num': 27}, {'year': 2011, 'num': 26}, {'year': 2012, 'num': 19}, {'year': 2013, 'num': 40}, {'year': 2014, 'num': 21}, {'year': 2015, 'num': 35}, {'year': 2016, 'num': 33}, {'year': 2017, 'num': 49}, {'year': 2018, 'num': 19}, {'year': 2019, 'num': 5}], [{'year': 2007, 'num': 3}, {'year': 2008, 'num': 8}, {'year': 2009, 'num': 4}, {'year': 2010, 'num': 8}, {'year': 2011, 'num': 5}, {'year': 2012, 'num': 6}, {'year': 2013, 'num': 15}, {'year': 2014, 'num': 20}, {'year': 2015, 'num': 17}, {'year': 2016, 'num': 24}, {'year': 2017, 'num': 18}, {'year': 2018, 'num': 1}]]
//
// compare_cited_list=[[{'year': 1991, 'num': 5}, {'year': 1992, 'num': 4}, {'year': 1993, 'num': 3}, {'year': 1994, 'num': 8}, {'year': 1995, 'num': 12}, {'year': 1996, 'num': 3}, {'year': 1997, 'num': 13}, {'year': 1998, 'num': 15}, {'year': 1999, 'num': 18}, {'year': 2000, 'num': 48}, {'year': 2001, 'num': 123}, {'year': 2002, 'num': 138}, {'year': 2003, 'num': 184}, {'year': 2004, 'num': 216}, {'year': 2005, 'num': 217}, {'year': 2006, 'num': 417}, {'year': 2007, 'num': 450}, {'year': 2008, 'num': 724}, {'year': 2009, 'num': 668}, {'year': 2010, 'num': 896}, {'year': 2011, 'num': 1030}, {'year': 2012, 'num': 1056}, {'year': 2013, 'num': 1298}, {'year': 2014, 'num': 1273}, {'year': 2015, 'num': 1056}, {'year': 2016, 'num': 680}, {'year': 2017, 'num': 638}, {'year': 2018, 'num': 172}], [{'year': 2004, 'num': 1}, {'year': 2005, 'num': 0}, {'year': 2006, 'num': 2}, {'year': 2007, 'num': 7}, {'year': 2008, 'num': 20}, {'year': 2009, 'num': 12}, {'year': 2010, 'num': 17}, {'year': 2011, 'num': 16}, {'year': 2012, 'num': 8}, {'year': 2013, 'num': 12}, {'year': 2014, 'num': 51}, {'year': 2015, 'num': 52}, {'year': 2016, 'num': 47}, {'year': 2017, 'num': 53}, {'year': 2018, 'num': 15}]]
//
// // paper_search_list=[]
// compare_achive_minyear=1990
// compare_achive_maxyear=2019
// compare_cited_minyear=1991
// compare_cited_maxyear=2018

//共有成果数量时间
compare_achive_year=[]
for(i=compare_achive_minyear;i<=compare_achive_maxyear;i++){
    compare_achive_year.push(i);
}
// 共有引用数量时间
compare_cited_year=[]
for(i=compare_cited_minyear;i<=compare_cited_maxyear;i++){
    compare_cited_year.push(i);
}


//加载第一个对比图表数据-学术成果
compare_achive_data=[]
for(i=0;i<compare_all_name.length;i++){
    dd=[]
    //先把共有时间内数量都填空
    for(j=compare_achive_minyear;j<=compare_achive_maxyear;j++){
        dd.push(null)
    }
    //再把有数据的填上
    for(j=0;j<compare_achivement_list2[i].length;j++){
        k=compare_achivement_list2[i][j]
        dd[k['year']-compare_achive_minyear]=k['num']
    }
    a={
        name:compare_all_name[i],
        type:'line',
        data:dd,
    }
    compare_achive_data.push(a)
}

//加载第二个对比图表数据-引用数量
compare_cited_data=[]
for(i=0;i<compare_all_name.length;i++){
    dd=[]
    //先把共有时间内数量都填空
    for(j=compare_cited_minyear;j<=compare_cited_maxyear;j++){
        dd.push(null)
    }
    //再把有数据的填上
    for(j=0;j<compare_cited_list[i].length;j++){
        k=compare_cited_list[i][j]
        dd[k['year']-compare_cited_minyear]=k['num']
    }
    a={
        name:compare_all_name[i],
        type:'line',
        data:dd,
    }
    compare_cited_data.push(a)
}


//加载第三个对比图表数据-期刊
compare_paper_name=['北大核心期刊','其他期刊数','其他会议数', '其他', '中国科技核心', '专著','SSCI期刊数', 'SCI期刊数', 'SCIE期刊数', 'EI期刊数','CSSCI期刊数','CSCD期刊数']
compare_paper_data=[]
for(i=0;i<compare_all_name.length;i++){
    dd=[]
    //把有数据的填上
    for(j=0;j<compare_paper_name.length;j++){
        name_key=compare_paper_name[j]
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
    }
    compare_paper_data.push(a)
}



$(function() {
    //初始化echarts
        var  ec1 = echarts.init(document.getElementById('partnerCompare1'))
        var  ec2 = echarts.init(document.getElementById('partnerCompare2'))
        var  ec3 = echarts.init(document.getElementById('partnerCompare3'))
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
        $("#comparescholar").click(function() {
            layer.open({
                type:1,
                title:"学者对比",
                area:["900px","700px"],
                content: $('#partnercompare')
            });
        })
})







