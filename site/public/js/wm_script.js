$(function(){
    $("#start").click(function(){
        $.ajax({
            type: "POST",
            url: "/apps/mactions",
            data: {
                "setvar":JSON.stringify({
                    "status": 1
                })
            },
            success: function(){
                location.href = "play";
            }
        });
    });
}); 