$(function () {
    checkedlist=[false,false,false,false];
    var index=0;
    var visuallength = $(".visual1").length;
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
    $(".addmore").click(function() {
        var allchecked = $(".choicecheck");
        for(var i=0;i<allchecked.length;i++){
            allchecked[i].checked=checkedlist[i];
        }
        index=layer.open({
            type:1,
            title:"学者对比",
            area:["850px","500px"],
            content: $('.comparechoice')
        });
    });
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
    $(".confirm").click(function () {
        var allchecked = $(".choicecheck");
        var checkedname=[];
        for(var i=0;i<allchecked.length;i++){
            if(allchecked[i].checked){
                checkedname.push(allchecked[i].value)
            }
            checkedlist[i]=allchecked[i].checked;
        }
        console.log(checkedname);
        console.log(checkedlist);
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