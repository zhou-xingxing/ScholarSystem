 $(function() {
    $("#8_main1")[0].style.display = "block";
    $("#8_main2")[0].style.display = "none";
    $("#8_main3")[0].style.display = "none";
    $("#8_main4")[0].style.display = "none";
    $("#partnerCompare1")[0].style.display = "block";
    $("#partnerCompare2")[0].style.display = "none";
    $("#partnerCompare3")[0].style.display = "none";
    $("#RelationNet")[0].style.display = "block";
    $("#NewRelationNet")[0].style.display = "none";
    $("#datatypeselectbtn1").click(function() {
        $("#8_main1")[0].style.display = "block";
        $("#8_main2")[0].style.display = "none";
        $("#8_main3")[0].style.display = "none";
        $("#8_main4")[0].style.display = "none";
    });
    $("#datatypeselectbtn2").click(function() {
        $("#8_main1")[0].style.display = "none";
        $("#8_main2")[0].style.display = "block";
        $("#8_main3")[0].style.display = "none";
        $("#8_main4")[0].style.display = "none";
    });
     $("#datatypeselectbtn3").click(function() {
        $("#8_main1")[0].style.display = "none";
        $("#8_main2")[0].style.display = "none";
        $("#8_main3")[0].style.display = "block";
        $("#8_main4")[0].style.display = "none";
    });
     $("#datatypeselectbtn4").click(function() {
        $("#8_main1")[0].style.display = "none";
        $("#8_main2")[0].style.display = "none";
        $("#8_main3")[0].style.display = "none";
        $("#8_main4")[0].style.display = "block";
    });
     $("#partnerbtn1").click(function() {
        $("#partnerCompare1")[0].style.display = "block";
        $("#partnerCompare2")[0].style.display = "none";
        $("#partnerCompare3")[0].style.display = "none";

    });
    $("#partnerbtn2").click(function() {
        $("#partnerCompare1")[0].style.display = "none";
        $("#partnerCompare2")[0].style.display = "block";
        $("#partnerCompare3")[0].style.display = "none";

    });
     $("#partnerbtn3").click(function() {
        $("#partnerCompare1")[0].style.display = "none";
        $("#partnerCompare2")[0].style.display = "none";
        $("#partnerCompare3")[0].style.display = "block";

    });
      $("#nettypeselectbtn1").click(function() {
        $("#RelationNet")[0].style.display = "block";
        $("#NewRelationNet")[0].style.display = "none";

    });
     $("#nettypeselectbtn2").click(function() {
        $("#RelationNet")[0].style.display = "none";
        $("#NewRelationNet")[0].style.display = "block";
    });
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