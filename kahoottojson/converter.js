$(function () {
    var inpfile = $("#ifile"),
        outhtml = $("#output_html"),
        mainobj = [],
        outjson = $("#output_json");
    inpfile.change(function (e) {
        var reader = new FileReader();
        reader.addEventListener("load", function () {
            outhtml.html(reader.result);
        });
        reader.readAsText(e.currentTarget.files[0], "text/html");
        $("#bouton").show();
       
    });
    $("#bouton").click(function(){

        $(".styles__Question-enothq-4").each(function (i, v) {
            mainobj.push({ "question": $(v).html().replace(/\n/g,"").replace(/\s{2,}/g," ") });
        });

        $(".styles__Image-enothq-5").each(function(i,v){
            var urlimg = $(v).attr("title");
            if (typeof urlimg != "undefined"){
                mainobj[i]["compl"] = "<img src=\"" + urlimg.replace(/&[\S\s]+$/,"") + "\"/>";
            }
        });

        $(".styles__Choices-enothq-12").each(function(i,v){
            mainobj[i]["choices"] = [];
            mainobj[i]["answer"] = [];
            for (var j = 0, c = v.childNodes.length, k = 0; j < c ; j++){
                if (v.childNodes[j].nodeType != 3){
                    console.log(v.childNodes[j])
                    mainobj[i]["choices"].push(v.childNodes[j].firstElementChild.firstElementChild.lastElementChild.innerHTML);
                    if (v.childNodes[j].firstElementChild.lastElementChild.firstElementChild.firstElementChild.id == "correct-icon"){
                        mainobj[i]["answer"].push(k);
                    }
                    k ++;
                }
            }
        });

        $(".styles__SecondsValue-enothq-11").each(function(i,v){
            mainobj[i]["time"] = parseInt($(v).html().replace(/\s*sec/gi,""));
        });
        console.log(mainobj)
        outjson.val(JSON.stringify(mainobj,null,6));
        $("#bouton").hide();
    });

});