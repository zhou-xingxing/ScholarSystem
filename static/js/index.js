$(function () {
    localStorage.clear();
    //高级按钮的隐藏
    $('#collapseTwo').collapse('hide');
    $('#collapseThree').collapse('hide');
    //为搜索插入热键
    $(document).keydown(function (e) {
        if (e.keyCode === 13){
            var  myselect=document.getElementById("select_type").value;
            var keyword = document.getElementById("data2search_result").value;
            localStorage.value = keyword;
            location.href = "../Search_result?keyword="+keyword+"&type="+myselect;
        }
    });
    //搜索按钮响应事件，获取关键字和搜索类型进行搜索
    document.getElementById("searchbtn").onclick=function () {
        if(window.localStorage) {
            var  myselect=document.getElementById("select_type").value;
            var keyword = document.getElementById("data2search_result").value;
            localStorage.value = keyword;
            location.href = "../Search_result?keyword="+keyword+"&type="+myselect;
        }else{
            alert('浏览器不支持')
        }
    };
    //首页对比学者增加按钮的响应事件，当多于四个不允许增加
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

    });
    //点击学者对比按钮的弹窗响应事件，初始化弹窗内容为compareDialog
    $("#compare").click(function() {
         document.getElementById("scholarInfoIinput").innerHTML="<div class=\"Dialogdiv\">\n" +
            "                学者姓名：<input type=\"text\" class=\"compareDialogInput1\" id=\"nameinput\" placeholder='必填'>\n" +
            "                学者机构：<input type=\"text\" class=\"compareDialogInput2\" id=\"schoolinput\" placeholder='必填'>\n" +
            "                学者学院：<input type=\"text\" class=\"compareDialogInput3\" placeholder=\"非必填\" id=\"collegeinput\">\n" +
            "            </div>";
        layer.open({
            type:1,
            title:"学者对比",
            area:["850px","500px"],
            content: $('#compareDialog')
        });
    });
    //开始对比按钮的事件响应获取对比的信息并将信息作为超链接参数传递给对别页面
    $("#startcompare").click(function () {
        var allscholarname = $(".compareDialogInput1");
        var allscholarschool = $(".compareDialogInput2");
        var allscholarcollege = $(".compareDialogInput3");
        var href = "../scholarcompare?";
        var flag=1;
        if (allscholarname.length ==1){
            alert("对比人数不少于一人且不多余四人");
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
    });
    <!--点击高级搜索后 展示出三个隐藏的input  3.6 bwm-->
     $(document).ready(function () {
            $("#advanced_soso1").on("click", function () {
                $("#soso2").toggle();
                $("#soso1").toggle();
            });
        });
      $(document).ready(function () {
            $("#advanced_soso2").on("click", function () {
                $("#soso1").toggle();
                $("#soso2").toggle();
                //$("#data2search_result").toggleClass("input2");
            });
        });
});