// JavaScript Document
if (typeof(xDialog)!='undefined')
{
	var dialog = new xDialog;
}
function cheklog(o)
{
	var mov=/^([0-9]{11})?$/;
	if(!mov.test(o.uname.value)||o.uname.value==''){
		alert("请正确填写用户名");return false;
	}
	if(o.pwd.value=='')
	{
		alert('请填写密码')
		return false;
	}
	/*if(o.code.value='')
	{
		alert('请填写验证码')
		return false;
	}*/
}

function chekph(o)
{
	var mov=/^([0-9]{11})?$/;
	if(!mov.test(o.uname.value)){
		alert("请填写手机号");return false;
	}
	/*if(o.code.value=='')
	{
		alert('请填写验证码')
		return false
	}*/
}


function chekreg(o)
{
	var mov=/^([0-9]{11})?$/;
	if(!mov.test(o.uname.value)){
		alert("请填写用户名");return false;
	}
	if(o.pwd.value=='')
	{
		alert('请填写密码')
		return false;
	}
	if(o.pwd.value!=o.spwd.value)
	{
		alert('密码与确证密码不一致')
		return false
	}
	if(o.mname.value=='')
	{
		alert('请填写姓名')
		return false
	}
	/*if(o.code.value=='')
	{
		alert('请填写验证码')
		return false
	}*/
}

function chekmoney()
{
	var pr=$("input[name='pr']:checked").val();
	var num=$("#num").val()
	var t=accMul(pr,num)
	$("#money").html('￥'+t)
	$("#prs").val(t)
	var sid=$("input[name='pr']:checked").attr("id")
	var stitle=$("input[name='pr']:checked").attr("title")
	var sf=$("input[name='pr']:checked").attr("alt")
	var opr=$("input[name='pr']:checked").attr("data-url")
	$("#sid").val(sid)
	$("#stitle").val(stitle)
	$("#feight").val(sf)
	$("#oprice").val(opr)
}

//乘法函数，用来得到精确的乘法结果 
//说明：javascript的乘法结果会有误差，在两个浮点数相乘的时候会比较明显。这个函数返回较为精确的乘法结果。 
//调用：accMul(arg1,arg2) 
//返回值：arg1乘以arg2的精确结果 
function accMul(arg1,arg2){ 
    var m=0,s1=arg1.toString(),s2=arg2.toString(); 
    try{m+=s1.split(".")[1].length}catch(e){} 
    try{m+=s2.split(".")[1].length}catch(e){} 
    return Number(s1.replace(".",""))*Number(s2.replace(".",""))/Math.pow(10,m) 
} 

//给Number类型增加一个mul方法，调用起来更加方便。 
Number.prototype.mul = function (arg){ 
    return accMul(arg, this); 
} 

function addcar(cid,aid)
{
	$.post("/include/shop/shop.php",{action:'addcar',channel:cid,id:aid},function(data){
		alert(data)
		})
}


function dopointSubmit( url,fobj ){
	if( fobj ){
		fobj.action = url;
		fobj.submit();
	}
}
function ChangeCounts(id,s,counts)
{
	$.get('/include/shop/shop.server.php',{Shopid:id,sid:s,BuyCounts:counts},function(data){
		Base = data.split("||");
		if(Base[0] == 'Err'){
			alert(Base[1]);
		}else{
			$('#counts'+id+'_'+s).html(Base[0]);
			$('#xiaoji'+id+'_'+s).html("￥"+ Base[1]);
			var zj = 0;
			var jy = 0;
			var yh = parseFloat($("#YouHui"+id+'_'+s).html());
			var points=parseInt($("#points"+id+'_'+s).html());
			if( counts < 0 ){
				zj = parseFloat($('#Heji').html())-yh;
			}else{
				zj = parseFloat($('#Heji').html())+ yh;
			}
			$('#Heji').html(zj);
		}
	});
}

function logs()
{
	$.post("/server.php",{action:'logs'},function(data){
			if(data!='')
			{
				$("#lmsg").html(data)
			}
		})
}

function chekedit(o)
{
	if(o.pwd.value!='')
	{
		if(o.pwd.value!=o.spwd.value)
		{
			alert('密码与确认密码不一致')
			return false;
		}
	}
	var mail = /^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$/;
	if(!mail.test(o.email.value)){
		alert("请填写邮箱");return false;
	}
	if(o.birth.value=='')
	{
		alert('请填写出生日期')
		return false
	}
	if(o.answer.value=='')
	{
		alert('请填写答案')
		return false
	}
}

function chkShopcar(o){
	if(o.sname.value.length < 2|| o.sname.value.length>10){
		alert("请正确填写收货人");return false;
	}
	if(o.city.value==0)
	{
		alert('请选择市区')
		return false
	}
	if(o.area.value==0)
	{
		alert('请选择区域')
		return false;
	}
	if( o.address.value.length ==''){
		alert("请正确填写收货地址");return false;
	}
	var tel_r = /^(\d+)(-(\d+))+$/;
	var mov=/^([0-9]{11})?$/;
	if(!mov.test(o.tel.value)){
		alert("请正确填写手机");return false;
	}
	if(o.detail.value.length > 100){
		alert("备注不能超过100个汉字。");return false;
	}
	if(o.sdate.value=='')
	{
		alert('请选择送达时间')
		return false
	}
}

function chekq(o)
{
	onum = $("#onum").val()
	code = $("#code").val()
	if(onum=='')
	{
		alert('请填写订单号')
		return false;
	}
	/*if(code=='')
	{
		alert('请填写验证码')
		return false
	}*/
	$.post("server.php",{action:'query',o:onum,c:code},function(data){
		if(data!='')
		{
			arr=data.split('|')
			if(arr[0]>0)
			{
				$("#result").html(arr[1])
				$("#code").val('')
			}
			else
			{
				alert(arr[1])
			}
		}
	})
}

function chekt(o)
{
	if(o.contact.value=='')
	{
		alert('请填写申请人')
		return false
	}
	if(o.mobile.value.length!=11)
	{
		alert('请填写手机')
		return false
	}
	if(o.tdate.value=='')
	{
		alert('请填写品尝时间')
		return false
	}
	if(o.address.value=='')
	{
		alert('请填写品尝时间')
		return false
	}
	if(o.tnum.value=='')
	{
		alert('请填写品尝人数')
		return false;
	}
}

function sdates()
{
	return WdatePicker({minDate:'%y-%M-#{%d}'});
}

function areas(o,i)
{
	$.post("/server.php",{action:'area',id:o,s:i},function(data){
		$("#area").html(data)	
	})
}

function smoney()
{
	var v=$("#area").val()
	$.post("/server.php",{action:'money',id:v},function(data){
		$("#spr").val(data)
		$("#pr").html(data)
		var pv	= parseFloat($("#p").html());
		var pis	= parseFloat($("#pis").html());
		$("#total").html(pv+parseFloat(data)-pis)
	})
}

function onpoints(o)
{
	var v=o.value;
	var t=/^[0-9]*[1-9][0-9]*$/
	if(t.test(v))
	{
		$.post("/server.php",{action:'getp'},function(data){
			if(parseFloat(v)>parseFloat(data))
			{
				alert('已超过您的可用积分');
				o.value=data;
				$("#pis").html(data);
				smoney()
			}
			else
			{
				$("#pis").html(v);
				smoney()
			}
		})
	}
	else
	{
		o.value='0'
		alert('请填写整数');
	}
}
function scar()
{
	$.post("/server.php",{action:'scar'},function(data){
		$("#scar").html(data)
		})
}

function addr()
{
	$.post("/server.php",{action:'loadaddr'},function(data){
		$("#addr").html(data)
		})
}

function del(i)
{
	if(confirm('确定删除'))
	{
		$.post("/server.php",{action:'del_addr',id:i},function(data){
			addr()
			})	
	}
}

function setaddr(o)
{
	var i=o.value;
	$.post("/server.php",{action:'getaddr',id:i},function(data){
		if(data!='')
		{
			arr=data.split("||")
			$("#sname").val(arr[0])
			$("#city").val(arr[2])
			areas(arr[2],arr[3])
			$("#address").val(arr[4])
			$("#tel").val(arr[5])
			
			
			$.post("/server.php",{action:'money',id:arr[3]},function(data){
				$("#spr").val(data)
				$("#pr").html(data)
				var pv	= parseFloat($("#p").html());
				var pis	= parseFloat($("#pis").html());
				$("#total").html(pv+parseFloat(data)-pis)
			})
		}
	})	
}

function recharge(o)
{
	var v=$("input[name='id']:checked").val()	
	if(v==null)
	{
		alert('请选择充值金额');
		return false;
	}
}

function charge(o)
{
	var i=o.value;
	$.post("/server.php",{action:'charge',id:i},function(data){
			$("#prs").val(data)
		})
}

function getcmd(str)
{
	$.post("/server.php",{action:"cmd",ids:str},function(data){
		$("#cmd").html(data)
		})
}
