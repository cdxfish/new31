var $j = jQuery.noConflict();
var txtPlaceholder;
$j(document).ready(function($) {
    /*help*/
	$j("#lnb .menu > li").each(function(a){
		$j("#lnb .menu > li").eq(a).find("strong").each(function(b){
			$j("#lnb .menu > li").eq(a).find("strong").eq(b).click(function(){
				if($j("#lnb .menu > li").eq(a).hasClass("active"))
				{
					$j("#lnb .menu > li").removeClass("active");
					$j("#lnb .menu > li > ul").stop(true,true).slideUp("fast");
				}
				else
				{
					$j("#lnb .menu > li").removeClass("active");
					$j("#lnb .menu > li").eq(a).addClass("active");
					$j("#lnb .menu > li > ul").stop(true,true).slideUp("fast");
					$j("#lnb .menu > li").eq(a).find("ul").slideDown("fast");
				}
				
			});
		});
	});
	/*giftcard*/
	$j(".card-list li").each(function(index){
		$j(".card-list li").eq(index).mouseenter(function(){
			$j(this).find(".add").stop(true,false).animate({bottom:0},"fast");
		});
		$j(".card-list li").eq(index).mouseleave(function(){
			$j(this).find(".add").stop(true,false).animate({bottom:-60+"px"},"fast");
		});
	});
	/*point*/
	$j(".val-sv .sv").mouseenter(function(){
		$j(this).find(".exchange").stop(true,false).animate({bottom:0},"fast");
	});
	$j(".val-sv .sv").mouseleave(function(){
		$j(this).find(".exchange").stop(true,false).animate({bottom:-88+"px"},"fast");
	});

	/*
	$j(".product-list li").each(function(index){
		$j(".product-list li").eq(index).mouseenter(function(){
			$j(this).find(".exchange").stop(true,false).animate({bottom:0},"fast");
		});
		$j(".product-list li").eq(index).mouseleave(function(){
			$j(this).find(".exchange").stop(true,false).animate({bottom:-88+"px"},"fast");
		});
	});
	*/

	/*金俊杰 新添加展开JQUERY*/
	$j(".tags-hd").each(function(index){
		$j(".tags-hd").eq(index).click(function(){
			if($j(this).hasClass("active"))
			{
				$j(this).find("span").removeClass("develop-1");
				$j(this).find("span").addClass("develop-0");
				$j(".product-section").eq(index).slideUp("normal",function(){
					$j(".tags-hd").removeClass("active");
				});
			}
			else
			{
				$j(".tags-hd").removeClass("active");
				$j(this).addClass("active");
				$j(".tags-hd").find("span").removeClass("develop-0");
				$j(".tags-hd").find("span").removeClass("develop-1");
				$j(".tags-hd").find("span").addClass("develop-0");
				$j(this).find("span").removeClass("develop-0");
				$j(this).find("span").addClass("develop-1");
				$j(".product-section").slideUp("normal");
				$j(".product-section").eq(index).stop(true,true).slideDown("normal",function(){
					$j('html, body').animate({scrollTop:$j(this).offset().top-216}, 'normal');
				});
			}
		});
	});
	/*注册页面*/
	$j(".clickpswd").keydown(function(){
		$j(".password-check").css("display","inline-block");
	});
	$j(".signupin-content .form-item").each(function(index){
		$j(".signupin-content .form-item").eq(index).find(".x-input").focus(function(){
			txtPlaceholder = $j(this).attr("placeholder");
			$j(this).attr("placeholder","");
			$j(".signupin-content .form-item").eq(index).find(".fnote").show();
		});
		$j(".signupin-content .form-item").eq(index).find(".x-input").blur(function(){
			$j(".signupin-content .form-item").eq(index).find(".fnote").hide();
			$j(this).attr("placeholder",txtPlaceholder);
		});

		$j(".signupin-content .form-item").eq(index).find(".x-input").keydown(function(){
			$j(".signupin-content .form-item").eq(index).find(".fnote").hide();
		});
	});

    function Json_to_String(O) {
        var S = [];
        var J = "";
        if (Object.prototype.toString.apply(O) === '[object Array]') {
        for (var i = 0; i < O.length; i++)
        S.push(O2String(O[i]));
            J = '[' + S.join(',') + ']';
        }
        else if (Object.prototype.toString.apply(O) === '[object Date]') {
            J = "new Date(" + O.getTime() + ")";
        }
        else if (Object.prototype.toString.apply(O) === '[object RegExp]' || Object.prototype.toString.apply(O) === '[object Function]') {
            J = O.toString();
        }
        else if (Object.prototype.toString.apply(O) === '[object Object]') {
            for (var i in O) {
                O[i] = typeof (O[i]) == 'string' ? '"' + O[i] + '"' : (typeof (O[i]) === 'object' ? O2String(O[i]) : O[i]);
                S.push('"'+i.toString()+'":'+O[i].toString());
            }
            J = '{' + S.join(',') + '}';
        }
        return J;
    };

	var address = {
		content:"<div></div>",
		closeIcon:"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABYAAAAWCAMAAADzapwJAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAyJpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuMy1jMDExIDY2LjE0NTY2MSwgMjAxMi8wMi8wNi0xNDo1NjoyNyAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RSZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIENTNiAoV2luZG93cykiIHhtcE1NOkluc3RhbmNlSUQ9InhtcC5paWQ6OUQ3NDU5MDcyOTJCMTFFNDk3OTdGQzc4OTlBQTNEQ0IiIHhtcE1NOkRvY3VtZW50SUQ9InhtcC5kaWQ6OUQ3NDU5MDgyOTJCMTFFNDk3OTdGQzc4OTlBQTNEQ0IiPiA8eG1wTU06RGVyaXZlZEZyb20gc3RSZWY6aW5zdGFuY2VJRD0ieG1wLmlpZDo5RDNFN0IzNjI5MkIxMUU0OTc5N0ZDNzg5OUFBM0RDQiIgc3RSZWY6ZG9jdW1lbnRJRD0ieG1wLmRpZDo5RDNFN0IzNzI5MkIxMUU0OTc5N0ZDNzg5OUFBM0RDQiIvPiA8L3JkZjpEZXNjcmlwdGlvbj4gPC9yZGY6UkRGPiA8L3g6eG1wbWV0YT4gPD94cGFja2V0IGVuZD0iciI/PmMjQ2EAAAAGUExURf///0kZAyiAnZMAAAAzSURBVHjaYmBkwASMUIwpiinOiEaj8xixiuJSgcs8XLbjcitIDJsoA07R4RsOOABAgAEALGsAKpOSlPAAAAAASUVORK5CYII=",
		selectIcon:"data:image/gif;base64,R0lGODlhCgAGAKIAAPf08tfGvdXCufz7+93Nxv///wAAAAAAACH/C1hNUCBEYXRhWE1QPD94cGFja2V0IGJlZ2luPSLvu78iIGlkPSJXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQiPz4gPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iQWRvYmUgWE1QIENvcmUgNS4zLWMwMTEgNjYuMTQ1NjYxLCAyMDEyLzAyLzA2LTE0OjU2OjI3ICAgICAgICAiPiA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPiA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIiB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iIHhtbG5zOnhtcE1NPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvbW0vIiB4bWxuczpzdFJlZj0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL3NUeXBlL1Jlc291cmNlUmVmIyIgeG1wOkNyZWF0b3JUb29sPSJBZG9iZSBQaG90b3Nob3AgQ1M2IChXaW5kb3dzKSIgeG1wTU06SW5zdGFuY2VJRD0ieG1wLmlpZDo5MEM2RjA3NzJCRkMxMUU0OEJCQkIwQkVGOEREMzZEQiIgeG1wTU06RG9jdW1lbnRJRD0ieG1wLmRpZDo5MEM2RjA3ODJCRkMxMUU0OEJCQkIwQkVGOEREMzZEQiI+IDx4bXBNTTpEZXJpdmVkRnJvbSBzdFJlZjppbnN0YW5jZUlEPSJ4bXAuaWlkOjkwOEFEMEZFMkJGQzExRTQ4QkJCQjBCRUY4REQzNkRCIiBzdFJlZjpkb2N1bWVudElEPSJ4bXAuZGlkOjkwOEFEMEZGMkJGQzExRTQ4QkJCQjBCRUY4REQzNkRCIi8+IDwvcmRmOkRlc2NyaXB0aW9uPiA8L3JkZjpSREY+IDwveDp4bXBtZXRhPiA8P3hwYWNrZXQgZW5kPSJyIj8+Af/+/fz7+vn49/b19PPy8fDv7u3s6+rp6Ofm5eTj4uHg397d3Nva2djX1tXU09LR0M/OzczLysnIx8bFxMPCwcC/vr28u7q5uLe2tbSzsrGwr66trKuqqainpqWko6KhoJ+enZybmpmYl5aVlJOSkZCPjo2Mi4qJiIeGhYSDgoGAf359fHt6eXh3dnV0c3JxcG9ubWxramloZ2ZlZGNiYWBfXl1cW1pZWFdWVVRTUlFQT05NTEtKSUhHRkVEQ0JBQD8+PTw7Ojk4NzY1NDMyMTAvLi0sKyopKCcmJSQjIiEgHx4dHBsaGRgXFhUUExIREA8ODQwLCgkIBwYFBAMCAQAAIfkEAAAAAAAsAAAAAAoABgAAAxQYNNU1RMTVoLQLhPvmplXEOR1YJAA7",	
		selectClass:function(){return "width:240px; padding-left:10px; display:inline-block; height:30px; border:1px solid #eee; line-height:30px; color:#8c6a52; background:url("+this.selectIcon+") no-repeat 95% center; cursor:pointer"},
		width:512,
		height:294,
		sale_city:null,
		cityList:[{id:1,add:"上海"},{id:2,add:"北京"},{id:3,add:"天津"},{id:4,add:"杭州"},{id:5,add:"无锡"},{id:6,add:"苏州"},{id:7,add:"广州"},{id:8,add:"深圳"}],
		callback1:function(){
			var self = this;
			if(self.sale_city.first == undefined || self.sale_city.first == false){
				//没有弹出框
				self.sale_city.first = "ok";
				try{
					var encode_sale_city = encodeURIComponent(JSON.stringify(self.sale_city));
				}catch(e){
					var encode_sale_city = encodeURIComponent(Json_to_String(self.sale_city));
				}
				Cookie.dispose('sale_city');
				Cookie.write('sale_city',encode_sale_city,{duration: 365,domain:'.21cake.com'});
				window.location.reload();
			}
		},
		callback2:function(){
			var self = this;
			self.sale_city = Cookie.read("sale_city");
			/*
			try{
				self.sale_city = JSON.parse(decodeURIComponent(self.sale_city));
			}catch(e){
				self.sale_city = eval('('+decodeURIComponent(self.sale_city)+')'); //ie7以下
			}
			*/
			self.sale_city = $j.parseJSON(decodeURIComponent(self.sale_city));
			$j("body").delegate("#sele_city","click",function(){
				$j("#cityList_div").show();
			});

			$j("body").delegate("#cityList_div li","click",function(event){
				$j("#myCity").html(this.innerHTML);
				self.sale_city.id = this.value.toString();
				switch(self.sale_city.id){
					case '1':
						self.sale_city.name = "上海";
						self.sale_city.region_id = 22;
						break;
					case '2':
						self.sale_city.name = "北京";
						self.sale_city.region_id = 2;
						break;	
					case '3':
						self.sale_city.name = "天津";
						self.sale_city.region_id = 43;
						break;	
					case '4':
						self.sale_city.name = "杭州";
						self.sale_city.region_id = 3134;
						break;	
					case '5':
						self.sale_city.name = "无锡";
						self.sale_city.region_id = 1717;
						break;	
					case '6':
						self.sale_city.name = "苏州";
						self.sale_city.region_id = 1692;
						break;	
					case '7':
						self.sale_city.name = "广州";
						self.sale_city.region_id = 424;
						break;	
					case '8':
						self.sale_city.name = "深圳";
						self.sale_city.region_id = 524;
						break;	
				}
				$j("#cityList_div").hide();
				event.stopPropagation();
			});
			

			$j("body").delegate("#cityList_div","mouseleave",function(){
				$j(this).hide();
			});
			
			if(self.sale_city.first != undefined && self.sale_city.first != false){
				return "stop";
			}
			var self = this;
			var $border = $j("<div></div>");
				$border[0].style.cssText = "height:100%; padding:7px; background:rgba(0,0,0,0.3); background:transparent\\0; filter:progid:DXImageTransform.Microsoft.gradient(startColorstr=#70111111,endColorstr=#70111111);";
			
			var optionCity_arr = new Array();
			for(var i=0; i<self.cityList.length;i++){ //打印城市
				optionCity_arr.push("<li style='padding-left:10px;' value='"+self.cityList[i].id+"'>"+self.cityList[i].add+"</li>");
				/*
				if(self.sale_city.id == i+1){
					optionCity_arr.push("<li value='"+self.cityList[i].id+"'>&nbsp;&nbsp;"+self.cityList[i].add+"</li>");
				}else{
				}
				*/
			}
			
			var $content = $j(  "<div>"+
									"<p style='text-align:right'><img class='alert_cancel' style='cursor:pointer; visibility:hidden; padding:15px 15px 0 0;' src='"+self.closeIcon+"'/></p>"+
									"<img style='border-right:1px dotted #ccc; float:left; margin-right:25px;' src='/themes/21cake/images/icon/logo_2.png'/>"+
									"<div>"+
										"<p style='font-size:22px; margin-top:10px;'>欢迎来到21cake官网商城</p>"+
										"<p style='margin-top:30px;'>请选择您需要送货的城市</p>"+
									"</div>"+
									"<div style='margin-top:10px;'><span style='"+self.selectClass()+"' id='sele_city'>"+
										"<span id='myCity'>"+self.sale_city.name+"</span>"+ 
										"<ul id='cityList_div' style='position:absolute; display:none; width:250px; background:#fff; border:1px solid #eee; top:180px; +top:175px; left:204px;'>"+
											optionCity_arr.join("")+											
										"</ul>"+									
									"</span></div>"+
									"<button style='background:#432818; font-size:16px; margin-top:22px; border:0; color:#fff; padding:8px 20px;' class='alert_ok'>开始购物</button>"+
								"</div>");	

				$content[0].style.cssText = "background:#fff; display:block; height:100%";
				$border.append($content);
			return $border[0].outerHTML;
		}
		
	};
	cakeWeb.changeAdd(address); //弹出地址

  });

var cakeWeb = {};
cakeWeb.changeAdd = function(params){
		var $bgdiv = $j("<div style='filter:Alpha(opacity=50);' id='bgdiv'></div>");
		var $content = $j("<div id='content'></div>");
		var docHeight = $j(document).height();
		$bgdiv.css({"background":"rgba(0,0,0,0.5)", "zIndex":"200000", "position":"fixed", "top":"0", "width":"100%","height":"100%"});
		if($j.browser.msie && $j.browser.version <= 8){
			$bgdiv.css({"background":"#000"});
		}

		$content.css({"background":"rgba(0,0,0,0)","zIndex":"200001", "padding":"0", "position":"fixed", "top":"50%", "left":"50%", "marginTop":-(params.height>>1)+"px", "marginLeft":-(params.width>>1)+"px", width:params.width+"px", height:params.height+"px", "top":"50%", "left":"50%"});
		if(params.callback2 != undefined && params.callback2 != false && typeof(params.callback2 == "function")){
			params.content = params.callback2();
		}
		if(params.content == "stop"){
			return false;
		}
		$content.append(params.content);
		$bgdiv.appendTo("body");
		$content.appendTo("body");
		var close = function(){
			$bgdiv.remove();
			$content.remove();
		};
		var exec = function(){
			$bgdiv.remove();
			$content.remove();
	 		if(params.callback1 != undefined && params.callback1 != false && typeof(params.callback1) == "function" ){
	 			params.callback1();
			}else{
				alert("请加上关闭程序");
			}			
		}

		$j("body").delegate(".alert_cancel","click",function(){
			close();
		});
		$j("body").delegate(".alert_ok","click",function(){
			exec();
		});

};
