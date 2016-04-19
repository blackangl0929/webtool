/**
 * Created by helit on 16/1/25.
 */
$(document).ready(function () {
    $("button#btn-addreport").click(function () {
        var name = $("#name");
        var type = $("#type");
        var ip  = $("#ip");
        var date = $("#date");
        var author = $("#author");
        var start_time = $("#start_time");
        var end_time = $("#end_time");
        if(name.val() == ""){
            name.focus();
            alert('报告名称不能为空')
        }else{
            $.ajax({
                url:'',
                type:"POST",
                contentType: "application/json",
                data:JSON.stringify({
                    name:name.val().trim(),
                    type:type.val().trim(),
                    ip:ip.val().trim(),
                    date:date.val().trim(),
                    author:author.val().trim(),
                    start_time:start_time.val().trim(),
                    end_time:end_time.val().trim(),
                }),
                async:false,
                success: function (msg) {
                    if(msg.msg == "success"){
                        alert("add success");
                        window.location=(/report/)
                    }else{
                        alert(msg.msg);
                    }
                }
            });
        }
    });
    $("button#btn-editreport").click(function () {
        //var title = $("#title");
        var name = $("#name");
        var type = $("#type");
        var ip  = $("#ip");
        var date = $("#date");
        var author = $("#author");
        var start_time = $("#start_time");
        var end_time = $("#end_time");
        $.ajax({
            url:'',
            type:"PUT",
            contentType: "application/json",
            data:JSON.stringify({
                    name:name.val().trim(),
                    type:type.val().trim(),
                    ip:ip.val().trim(),
                    date:date.val().trim(),
                    author:author.val().trim(),
                    start_time:start_time.val().trim(),
                    end_time:end_time.val().trim(),
            }),
            async:false,
            success: function (msg) {
                if(msg.status == "success"){
                    alert(msg.msg);
                    window.location=(/report/)
                }else{
                    alert(msg.msg);
                }
            }
        });
    });
}
);
