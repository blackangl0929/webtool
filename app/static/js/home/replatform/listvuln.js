/**
 * Created by helit on 15/12/20.
 */
 $(document).ready(
    function get_vulns(){
        $.ajax({
                type: "GET",
                url: 'list',
                contentType: "application/json",
                async:false,
                success: function(data) {
                    for (var i = 0; i < data['count']; i++) {
                        var test=$("<tr id="+i+">");
                        var title=$("<th>").text(data['vulns'][i]['title']);
                        var type=$("<th>").text(data['vulns'][i]['type']);
                        var risk=$("<th>").text(data['vulns'][i]['risk']);
                        var v_edit=$("<button class=\"btn btn-default btn-sm fa fa-pencil\" href="+data['vulns'][i]['url']+">");
                        var v_delete=$("<button id=\"delete"+i+"\" type=\"button\" class=\"btn btn-default btn-sm fa fa-trash-o\" \h" +
                                "ref="+data['vulns'][i]['url']+">");
                        $("tbody").append(test);
                        $("tr#"+i+"").append(title,type,risk,v_edit,v_delete);
                    }
//{#                    var b_prev=$("<a id=\"prev\" type=\"button\" class=\"btn btn-default\" href="+data['prev']+">").text('«');#}
//{#                    var b_next=$("<a id=\"next\" type=\"button\" class=\"btn btn-default\" href="+data['next']+">").text('»');#}
//{#                    $("div#tools").append(b_prev,b_next);#}
                }, error: function () {
                    alert("加载失败");
                }
            });
        $("button.fa-trash-o").click(function () {
            var $select = $( this );
            var url = $select.attr("href");
            $.ajax({
                    url:url,
                    type:"DELETE",
                    async:false,
                    success: function (msg) {
                        if(msg.status == "success"){
                            alert("删除成功");
//{#                            get_vulns();#}
                        }else{
                            alert(msg.msg);
                        }
                    }
            });
        });
//{#        $("#prev").click(function() {#}
//{#            var prev = $('#prev').val().trim();#}
//{#            get_vulns(prev);#}
//{#        });#}
//{#        $("#next").click(function() {#}
//{#            var next = $('#next').val().trim();#}
//{#            get_vulns(next);#}
//{#        });#}
    }
    );