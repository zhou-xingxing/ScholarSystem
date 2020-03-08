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
})