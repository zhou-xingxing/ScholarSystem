$(function () {
    //checkedlist为对比页面中选择需要增加的对比项。分别为成果、合作机构、合作学者、会议期刊
    checkedlist=[false,false,false,false];
    //index用于记录打开的弹窗序号
    var index=0;
    //visuallength记录比较的人数
    var visuallength = $(".visual1").length;
    //对比界面初始化 使可视化界面第一个按钮内容呈现其他内容影藏
    for(var i=0;i<visuallength;i++){
        $(".visual1")[i].style.display="block";
        $(".visual2")[i].style.display="none";
        $(".visual3")[i].style.display="none";
        $(".visual4")[i].style.display="none";
        $(".achivementwithhr")[i].style.display="none";
        $(".cooperatewithhr")[i].style.display="none";
        $(".partnerwithhr")[i].style.display="none";
        $(".meetingwithhr")[i].style.display="none";
    }
    //相应增加更多对比项的需求
    $(".addmore").click(function() {
        //复现之前选过的对比项
        var allchecked = $(".choicecheck");
        for(var i=0;i<allchecked.length;i++){
            allchecked[i].checked=checkedlist[i];
        }
        //打开选择增加对比项的窗口
        index=layer.open({
            type:1,
            title:"学者对比",
            area:["850px","500px"],
            content: $('.comparechoice')
        });
    });
    //响应可视化按钮的点击事件
    $(".visualbtn1").click(function () {
        for(var i=0;i<visuallength;i++){
            $(".visual1")[i].style.display="block";
            $(".visual2")[i].style.display="none";
            $(".visual3")[i].style.display="none";
            $(".visual4")[i].style.display="none";
        }        
    });
    $(".visualbtn2").click(function () {
        for(var i=0;i<visuallength;i++){
            $(".visual1")[i].style.display="none";
            $(".visual2")[i].style.display="block";
            $(".visual3")[i].style.display="none";
            $(".visual4")[i].style.display="none";
        }        
    });
    $(".visualbtn3").click(function () {
        for(var i=0;i<visuallength;i++){
            $(".visual1")[i].style.display="none";
            $(".visual2")[i].style.display="none";
            $(".visual3")[i].style.display="block";
            $(".visual4")[i].style.display="none";
        }        
    });
    $(".visualbtn4").click(function () {
        for(var i=0;i<visuallength;i++){
            $(".visual1")[i].style.display="none";
            $(".visual2")[i].style.display="none";
            $(".visual3")[i].style.display="none";
            $(".visual4")[i].style.display="block";
        }       
    });
    //确认选择增加对比按钮的点击按钮
    //逻辑是先用checkedlist保存用户点击的对比项，然后将用户选择的对比项display设为block
    $(".confirm").click(function () {
        var allchecked = $(".choicecheck");
        var checkedname=[];
        for(var i=0;i<allchecked.length;i++){
            if(allchecked[i].checked){
                checkedname.push(allchecked[i].value)
            }
            checkedlist[i]=allchecked[i].checked;
        }
        //console.log(checkedname);
        //console.log(checkedlist);
        alllength = $(".achivement").length;
        for(var i=0;i<alllength;i++){
            if(checkedlist[0]){
                $(".achivementwithhr")[i].style.display="block"
            }else{
                $(".achivementwithhr")[i].style.display="none"
            }
            if(checkedlist[1]){
                $(".cooperatewithhr")[i].style.display="block"
            }else{
                $(".cooperatewithhr")[i].style.display="none"
            }
            if(checkedlist[2]){
                $(".partnerwithhr")[i].style.display="block"
            }else{
                $(".partnerwithhr")[i].style.display="none"
            }
            if(checkedlist[3]){
                $(".meetingwithhr")[i].style.display="block"
            }  else{
                $(".meetingwithhr")[i].style.display="none"
            }
        }
        layer.close(index);
    })
});