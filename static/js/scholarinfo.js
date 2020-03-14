 $(function() {
     //个人信息主页可视化内容按钮的控制，分别为成果 引用 期刊会议、论文关键词
     //初始化为成果可见
    $("#8_main1")[0].style.display = "block";
    $("#8_main2")[0].style.display = "none";
    $("#8_main3")[0].style.display = "none";
    $("#8_main4")[0].style.display = "none";
    //合作学者对比按钮的控制，分别对比合作学者的成果、引用、期刊会议
    $("#partnerCompare1")[0].style.display = "block";
    $("#partnerCompare2")[0].style.display = "none";
    $("#partnerCompare3")[0].style.display = "none";
    //关系网络按钮的控制按钮
    $("#RelationNet")[0].style.display = "block";
    //新关系网络按钮的控制按钮--按照论文学校对比
    $("#NewRelationNet")[0].style.display = "none";
    //响应可视化每个按钮的点击事件
    $("#datatypeselectbtn1").click(function() {
        $("#8_main1")[0].style.display = "block";
        $("#8_main2")[0].style.display = "none";
        $("#8_main3")[0].style.display = "none";
        $("#8_main4")[0].style.display = "none";
    });
    //响应可视化每个按钮的点击事件
    $("#datatypeselectbtn2").click(function() {
        $("#8_main1")[0].style.display = "none";
        $("#8_main2")[0].style.display = "block";
        $("#8_main3")[0].style.display = "none";
        $("#8_main4")[0].style.display = "none";
    });
    //响应可视化每个按钮的点击事件
     $("#datatypeselectbtn3").click(function() {
        $("#8_main1")[0].style.display = "none";
        $("#8_main2")[0].style.display = "none";
        $("#8_main3")[0].style.display = "block";
        $("#8_main4")[0].style.display = "none";
    });
     //响应可视化每个按钮的点击事件
     $("#datatypeselectbtn4").click(function() {
        $("#8_main1")[0].style.display = "none";
        $("#8_main2")[0].style.display = "none";
        $("#8_main3")[0].style.display = "none";
        $("#8_main4")[0].style.display = "block";
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
      //关系网络每个按钮的点击事件
      $("#nettypeselectbtn1").click(function() {
        $("#RelationNet")[0].style.display = "block";
        $("#NewRelationNet")[0].style.display = "none";

    });
       //关系网络每个按钮的点击事件
     $("#nettypeselectbtn2").click(function() {
        $("#RelationNet")[0].style.display = "none";
        $("#NewRelationNet")[0].style.display = "block";
    });
      //推荐学者的点击事件
     //逻辑为当点击推荐学者时，传入当前学者的id，根据与该学者的相似度，
     // 异步请求推荐学者数据，并返回，呈现在主页
     $(".recommendscholar").click(function () {
         var scholarid = document.getElementById("ContentPlaceHolder1_LabelORCID").innerText;
        $.ajax({
            url:'/recommend',
            type:'GET',
            data:{'user':scholarid },
            success:function(data){
                console.log(data);
                data = eval(data);
                var item;
                $(".reclist")[0].innerHTML="";
                $.each(data,function(i,result){
                    item=result[1];
                    $(".reclist")[0].append(item);
                });
                $(".reclist")[0].style.display="block"
            }
        })
    });
     //推荐学者换一换按钮的响应事件，与上述逻辑基本相同
    $(".change").click(function () {
        var num = parseInt($(".change").val());
        var scholarid = document.getElementById("ContentPlaceHolder1_LabelORCID").innerText;
        num+=3;
        if(num==30){
            num=0;
        }
        $(".change")[0].value = num;
        $.ajax({
            url:'/refresh',
            type:'GET',
            data:{'user':scholarid,'type':num},
            success:function(data){
                console.log(data);
                data = eval(data);
                var item;
                $(".reclist")[0].innerHTML="";
                $.each(data,function(i,result){
                    item=result[1];
                    $(".reclist")[0].append(item);
                });
                $(".reclist")[0].style.display="block"
            }
        })
    });
});

var changenum = 0; //全局变量，点击推荐学家可以被重置为0
function recommend()
{
    var scholarid = document.getElementById("ContentPlaceHolder1_LabelORCID").innerText;
    $.ajax({
        url: '/recommend',
        type: 'GET',
        data: {'user': scholarid},
        dataType:"json",
        success: function (data)
        {
            console.log(data);
            data = eval(data);
            var item='';
            $.each(data, function (i, result) {
                item += '<p><a class="myrecommend" title="'+ result[2] + result[3] +'" href="/scholarinfo?scholarid=' + result[0] + '">' + result[1]+'</a></p>';
            });
            $('#reclist').html(item);
            $('#reclist').css({"display":"block"});
            $('#changelist').css({"display":"block"});
            $('#recommendscholar').css({"text-shadow":"none"});
        }
    });
    changenum=0;
}

function change_scholar()
{
    var scholarid = document.getElementById("ContentPlaceHolder1_LabelORCID").innerText;
    changenum+=3;
    if(changenum==30)
    {
         changenum=0;
    }
    $.ajax({
        url:'/refresh',
        type:'GET',
        data:{'user':scholarid,'type':changenum},
        success:function(data)
        {
            console.log(data);
            data = eval(data);
            var item = '';
            $.each(data,function(i,result){
             item += '<p><a class="myrecommend" title="' + result[2] + result[3]  +'" href="/scholarinfo?scholarid=' + result[0] + '">' + result[1]+'</a></p>';
            });
         $('#reclist').html(item);
         $('#reclist').css({"display":"block"});
        }});
}