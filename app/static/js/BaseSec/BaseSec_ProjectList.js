//增加
  $(".btn-primary").click(function(){
    if($("table tr").hasClass("addtr")){
	alert("先完成操作！！！");
	}else{
     $("table tr:last").after(' <tr class="addtr"><td><input type="text" name="names" value="" /></td>'+' <td><input type="text" name="sexs" value="" /></td>'+'<td><input type="text" name="ages" value="" /></td>' +'<td> <a href="javascript:;" class="btn save btn-info btn-lg">保存</a>  <a href="javascript:;" class="btn off btn-info btn-lg">取消</a> </td>'+' </tr>');
       }


  })




  //保存
  $(document).on("click",".save",function(){

   var name =$(this).parent().parent().find('input[name="names"]').val();
   var sex =$('input[name="sexs"]').val();
   var age =$('input[name="ages"]').val();

      var n="";
      n+='<td>'+name+'</td>';
        n+=' <td>'+sex+'</td>';
       n+='  <td>'+age+'</td>';
		n+=' <td>';
		n+='  <a href="javascript:;" class="btn edit btn-info btn-lg"><span class="icon-edit"></span>修改</a>';
		n+=' </td>';
       $(this).parent().parent().removeClass("addtr");
      $(this).parent().parent().html(n);
  })

   //修改
  $(document).on("click",".edit",function(){
  if($("table tr").hasClass("addtr")){
	alert("先完成操作！！！");
	}else{
   var name =$(this).parent().parent().find('td').eq(0).text();
   var sex =$(this).parent().parent().find('td').eq(1).text();
   var age =$(this).parent().parent().find('td').eq(2).text();

    var n="";
      n+='<td><input type="text" name="names" value="'+name+'" /></td>';
        n+=' <td><input type="text" name="sexs" value="'+sex+'" /></td>';
       n+='  <td><input type="text" name="ages" value="'+age+'" /></td>';
		n+=' <td>';
		n+='  <a href="javascript:;" class="btn save btn-info btn-lg">保存</a>';
		n+='  <a href="javascript:;" class="btn off btn-info btn-lg">取消</a>';
		n+=' </td>';
       $(this).parent().parent().addClass("addtr");
      $(this).parent().parent().html(n);
	  }

  })

  $(document).on("click",".off",function(){

   window.location.reload();
  })