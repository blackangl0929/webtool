/**
 * Created by helit on 16/1/25.
 */
/**
 * Created by helit on 15/12/20.
 */
 $(document).ready(
    function get_reports(){
        $.ajax({
                type: "GET",
                url: 'list',
                contentType: "application/json",
//{#                data:  pageIndex,#}
                async:false,
                success: function(data) {
                    for (var i = 0; i < 10; i++) {
                        var test=$("<tr id="+i+">");
                        var title=$("<th>").text(data['reports'][i]['name']);
                        var type=$("<th>").text(data['reports'][i]['type']);
                        var risk=$("<th>").text(data['reports'][i]['author']);
                        var v_edit=$("<a class=\"btn btn-default btn-sm fa fa-pencil\" href="+data['reports'][i]['url']+">");
                        var v_export=$("<button id=\"export"+i+"\" type=\"button\" class=\"btn btn-default btn-sm fa fa-floppy-o\" \h" +
                                "ref="+data['reports'][i]['url']+">");
                        var v_delete=$("<button id=\"delete"+i+"\" type=\"button\" class=\"btn btn-default btn-sm fa fa-trash-o\" \h" +
                                "ref="+data['reports'][i]['url']+">");
                        $("tbody").append(test);
                        $("tr#"+i+"").append(title,type,risk,v_edit,v_export,v_delete);
                    }
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
        $("button.fa-floppy-o").click(function () {
            var $select = $( this );
            var url = $select.attr("href");
            $.ajax({
                    url:url+'/export',
                    type:"GET",
                    async:false,
                    success: function (msg) {
                        if(msg.status == "success"){
                            alert(msg.msg);
                        }else{
                            alert(msg.msg);
                        }
                    }
            });
        });
    }
    );