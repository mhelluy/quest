$(function(){
    setInterval(function(){
        $.ajax({
            type: "GET",
            url: "/apps/pwait",
            datatype: "json",
            success: function(obj){
                obj = JSON.parse(obj);
                if (obj.isReady){
                    location.reload();
                }
            }
        });
    },100);
});