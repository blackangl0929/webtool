/**
 * Created by helit on 15/12/20.
 */
$(document).ready(function () {
    $("button#btn-addvuln").click(function () {
        var title = $("#title");
        var type = $("#type");
        var risk  = $("#risk");
        var overview = $("#overview");
        var poc = $("#poc");
        var damage = $("#damage");
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
                    type:type.val().trim(),
                    risk:risk.val().trim(),
                    overview:overview.val().trim(),
                    poc:poc.val().trim(),
                    damage:damage.val().trim(),
                    remediation:remediation.val().trim()
                }),
                async:false,
                success: function (msg) {
                    if(msg.msg == "success"){
                        alert("add success");
                        window.location=(/vuln/)
                    }else{
                        alert(msg.msg);
                    }
                }
            });
        }
    });
    $("button#btn-editvuln").click(function () {
        //var title = $("#title");
        var type = $("#type");
        var risk  = $("#risk");
        var overview = $("#overview");
        var poc = $("#poc");
        var damage = $("#damage");
        var remediation = $("#remediation");
        $.ajax({
            url:'',
            type:"PUT",
            contentType: "application/json",
            data:JSON.stringify({
                type:type.val().trim(),
                risk:risk.val().trim(),
                overview:overview.val().trim(),
                poc:poc.val().trim(),
                damage:damage.val().trim(),
                remediation:remediation.val().trim()
            }),
            async:false,
            success: function (msg) {
                if(msg.status == "success"){
                    alert(msg.msg);
                    window.location=(/vuln/)
                }else{
                    alert(msg.msg);
                }
            }
        });
    });
}
);
