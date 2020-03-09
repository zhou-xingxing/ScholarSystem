 $(function() {
    $("#8_main1")[0].style.display = "block";
    $("#8_main2")[0].style.display = "none";
    $("#8_main3")[0].style.display = "none";
    $("#8_main4")[0].style.display = "none";
    $("#partnerCompare1")[0].style.display = "block";
    $("#partnerCompare2")[0].style.display = "none";
    $("#partnerCompare3")[0].style.display = "none";
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
    $("#comparescholar").click(function() {
            layer.open({
                type:1,
                title:"学者对比",
                area:["900px","700px"],
                content: $('#partnercompare')
            });
    })
     $(".recommendscholar").click(function () {
        $.ajax({
            url:'/recommend',
            type:'GET',
            data:{'user':'CN-B973QRIJ' },
            success:function(data){
                console.log(data)
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
    })
    $(".change").click(function () {
        var num = parseInt($(".change").val())
        num+=3;
        $(".change")[0].value = num;
        $.ajax({
            url:'/refresh',
            type:'GET',
            data:{'user':'CN-B973QRIJ','type':num},
            success:function(data){
                console.log(data)
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
    })
})