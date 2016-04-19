/**
 * Created by helit on 16/2/1.
 */
$(document).ready(function () {
    $("button#rep-addvuln").click(function () {
        var vulns = [];
        var items = $('[name = "vuln"]:checkbox:checked');

        for (var i = 0; i < items.length; i++) {
             // 如果i+1等于选项长度则取值后添加空字符串，否则为逗号
             vulns = (vulns + items.get(i).value) + (((i + 1)== items.length) ? '':',');
        }
        if(vulns==""){
            alert('你没有勾选漏洞');
        } else{
            $.ajax({
                url:'',
                type:"POST",
                contentType: "application/json",
                data:JSON.stringify({vulns : vulns}) ,
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
}
);
