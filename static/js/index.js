$(function () {
    localStorage.clear()
    $(document).keydown(function (e) {
        if (e.keyCode === 13){
            var  myselect=document.getElementById("select_type").value;
            var keyword = document.getElementById("data2search_result").value;
            localStorage.value = keyword;
            location.href = "../Search_result?keyword="+keyword+"&type="+myselect;
        }
    })
    document.getElementById("searchbtn").onclick=function () {
        if(window.localStorage) {
            var  myselect=document.getElementById("select_type").value;
            var keyword = document.getElementById("data2search_result").value;
            localStorage.value = keyword;
            location.href = "../Search_result?keyword="+keyword+"&type="+myselect;
        }else{
            alert('浏览器不支持')
        }
    }
    $("#addone").click(function () {
        var allscholarname = $(".compareDialogInput1");
        if (allscholarname.length>=4){
            alert("最多只能同时对比四个学者");
        } else{
            $("#scholarInfoIinput").append('<div class="Dialogdiv">' +
           ' 学者姓名：<input type="text" class="compareDialogInput1" id="nameinput" placeholder="必填">' +
           ' 学者机构：<input type="text" class="compareDialogInput2" id="schoolinput" placeholder="必填">' +
           ' 学者学院：<input type="text" class="compareDialogInput3" id="collegeinput" placeholder="非必填"></div>');
        }

    })
    $("#compare").click(function() {
         document.getElementById("scholarInfoIinput").innerHTML="<div class=\"Dialogdiv\">\n" +
            "                学者姓名：<input type=\"text\" class=\"compareDialogInput1\" id=\"nameinput\" placeholder='必填'>\n" +
            "                学者机构：<input type=\"text\" class=\"compareDialogInput2\" id=\"schoolinput\" placeholder='必填'>\n" +
            "                学者学院：<input type=\"text\" class=\"compareDialogInput3\" placeholder=\"非必填\" id=\"collegeinput\">\n" +
            "            </div>"
        layer.open({
            type:1,
            title:"学者对比",
            area:["850px","500px"],
            content: $('#compareDialog')
        });
    })
    $("#startcompare").click(function () {
        var allscholarname = $(".compareDialogInput1")
        var allscholarschool = $(".compareDialogInput2")
        var allscholarcollege = $(".compareDialogInput3")
        var href = "../compare?";
        var flag=1;
        if (allscholarname.length ==1){
            alert("对比人数不少于一人且不多余四人")
            flag=0;
        }
        for(var i=0;i<allscholarname.length;i++){
            if(!allscholarname[i].value){
                alert("姓名未填完整");
                flag=0;
                break;
            }
            if (!allscholarschool[i].value){
                alert("机构未填完整");
                flag=0;
                break;
            }
            if(i==0){
                href+="name1="+allscholarname[i].value+"&school1="+allscholarschool[i].value+"&college1="+allscholarcollege[i].value;
            }else{
                href+="&name"+String(i+1)+"="+allscholarname[i].value+"&school"+String(i+1)+"="+allscholarschool[i].value+"&college"+String(i+1)+"="+allscholarcollege[i].value;
            }
        }
        if(flag){
            href+="&length="+String(allscholarname.length);
            window.location.href=href;
        }
    })
})