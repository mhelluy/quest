$(function(){
    setInterval(function(){
        $.ajax({
            type: "GET",
            url: "/apps/wnames",
            success: function(obj){
                obj = JSON.parse(obj);
                ul = $("ul");
                if (ul.html().replace(/( style="[\S\s]*"|\n)/g,"") != obj.listNames.replace(/\n/g,"")){
                    ul.html(obj.listNames);
                    ulLi = $("ul li");
                    $("#nb_players").html(ulLi.length);
                    ulLi.last().hide().show(2000);
                }
                if (obj.start){
                    location.href = "play";
                }
            }
        });
    },5000);
});