/**
 * Created by helit on 16/2/18.
 */
$(document).ready(function () {
    $("button#btn-addvuln").click(function () {
        var title = $("#title");
        var damage = $("#damage");
        var type  = $("#type");
        var overview = $("#overview");
        var ip = $("#ip");
        var poc = $("#poc");
        var risk = $("#risk");
        var remediation = $("#remediation");
        if(title.val() == ""){
            title.focus();
            alert('漏洞名称不能为空')
        }else{
            $.ajax({
                url:'',
                type:"POST",
                contentType: "application/json",
                data:JSON.stringify({
                    title:title.val().trim(),
                    damage:damage.val().trim(),
                    type:type.val().trim(),
                    overview:overview.val().trim(),
                    ip:ip.val().trim(),
                    poc:poc.val().trim(),
                    risk:risk.val().trim(),
                    remediation:remediation.val().trim()
                }),
                async:false,
                success: function (msg) {
                    if(msg.status == "success"){
                        alert(msg.msg);
                        window.history.back(-1);
                    }else{
                        alert(msg.msg);
                    }
                }
            });
        }
    });
    $("button#btn-editvuln").click(function () {
        var title = $("#title");
        var damage = $("#damage");
        var type  = $("#type");
        var overview = $("#overview");
        var ip = $("#ip");
        var poc = $("#poc");
        var risk = $("#risk");
        var remediation = $("#remediation");
        $.ajax({
            url:'',
            type:"PUT",
            contentType: "application/json",
            data:JSON.stringify({
                    title:title.val().trim(),
                    damage:damage.val().trim(),
                    type:type.val().trim(),
                    overview:overview.val().trim(),
                    ip:ip.val().trim(),
                    poc:poc.val().trim(),
                    risk:risk.val().trim(),
                    remediation:remediation.val().trim()
            }),
            async:false,
            success: function (msg) {
                if(msg.status == "success"){
                    alert(msg.msg);
                    window.history.back(-1);
                }else{
                    alert(msg.msg);
                }
            }
        });
    });
    $("button#cancel").click(function(){
        window.history.back(-1);
    });
}
);