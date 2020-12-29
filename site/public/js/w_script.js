$(function(){
    setInterval(function(){
        $.ajax({
            type: "GET",
            url: "/apps/winfos",
            datatype: "json",
            success: function(obj){
                obj = JSON.parse(obj);
                $("#nb_players").html(obj.nb_players);
                if (obj.start){
                    location.href = "play";
                }
            }
        });
    },5000);
});