$(document).ready(function () {
    //动态写入 弹出层
    $('body').append("<div id='floatingLayer' class='popup' style='width:auto;'></div><div id='maskLayer' class='popup_wrapper'><iframe style='width:100%; height:100%; z-index:1; filter:mask();'></iframe></div>");
    
    if (jQuery.browser.msie && jQuery.browser.version === "6.0") {
        // $(window).scroll(CaiDianDialogScroll);
        $("#floatingLayer").css("position", "absolute");
    } else {
        $("#floatingLayer").css("position", "fixed");
    }
    
    $("#floatingLayer").hide();
    $("#maskLayer").hide();
});

function CaiDianDialogScroll() {
    $("#floatingLayer").css("top", ($(window).height() - $("#floatingLayer").outerHeight()) / 2) + parseInt(GetScrollTop() || 0) + "px";
    //document.getElementById("divCaiDianDialog").style.marginLeft = document.body.scrollLeft;
}

function closePopupNow() {
    
    $("#maskLayer").hide();
    $("#floatingLayer").hide();
}

function closePopup() {
    disablePopup(800, null);
}

//使用Jquery去除弹窗效果
function disablePopup(fadeOut, callback) {
    
    $("#maskLayer").fadeOut(fadeOut);
    $("#floatingLayer").fadeOut(fadeOut, callback);
    
}

function dialogPloy() {
    
    $("#floatingLayer").css("left", (($(window).width() - $("#floatingLayer").outerWidth()) / 2) + "px");
    if (jQuery.browser.msie && jQuery.browser.version === "6.0") {
        $("#floatingLayer").css("top", (($(window).height() - $("#floatingLayer").outerHeight()) / 2) + parseInt(GetScrollTop() || 0) + "px");
    } else {
        $("#floatingLayer").css("top", (($(window).height() - $("#floatingLayer").outerHeight()) / 2) + "px");
    }
    
}

function dialog(res, obj) {
    
    //dialog-valid √, dialog-error ⅹ, dialog-warning !, dialog-loading …
    for (var i = 0; i < obj.length; i++) {
        var item = {
            val : obj[i].val || "",
            className : obj[i].className || "x",
            title : obj[i].title || "",
            text : obj[i].text || "",
            //hideHead: obj[i].hideHead || false,
            isPanel : obj[i].isPanel || false,
            isMaskLayerHide : obj[i].isMaskLayerHide || false,
            //hideConfirm: obj[i].hideConfirm || null,
            //hideClose: obj[i].hideClose || false,
            setTimeout : obj[i].setTimeout || 1500,
            fadeOut : obj[i].fadeOut || 800,
            returnVal : obj[i].returnVal || false,
            callback : obj[i].callback || null,
            width : obj[i].width || 0,
            top : obj[i].top || 0,
            left : obj[i].left || 0
        };
        
        if (res == item.val) {
            
            $("#floatingLayer").html("");
            $("#floatingLayer").removeClass().addClass("popup");
            
            if (item.isPanel) {
                
                $("#floatingLayer").html(item.text);
                
            } else {
                
                if (item.className == "l") {
                    
                    var strAlert = "    <span class=\"loading_s\">" + item.title + "</span>  \r\n";
                    
                    $("#floatingLayer").html(strAlert);
                    
                    $("#floatingLayer").addClass("loadingPop");
                    
                    item.width = 220;
                    item.fadeOut = -1;
                } else {
                    
                    var imgClass = "pop_message_error";
                    
                    switch (item.className) {
                    case "x":
                        imgClass = "pop_message_error";
                        break;
                    case "v":
                        imgClass = "pop_message_ok";
                        break;
                    }
                    
                    var strAlert = "    <div class='pop_sml'>  \r\n";
                    strAlert += "        <div class='" + imgClass + "'>  \r\n";
                    strAlert += "            <strong class=\"title\">" + item.title + "</strong>  \r\n";
                    strAlert += "  \r\n";
                    strAlert += "            <div class=\"content\">  \r\n";
                    strAlert += "    " + item.text + "  \r\n";
                    strAlert += "            </div>  \r\n";
                    strAlert += "        </div>  \r\n";
                    strAlert += "  \r\n";
                    strAlert += "        <div class='pop_handle'>  \r\n";
                    strAlert += "            <a href=\"javascript:void(0);\" class=\"btn_sml\">确认</a>  \r\n";
                    strAlert += "  \r\n";
                    strAlert += "            <div class=\"clear\"></div>  \r\n";
                    strAlert += "        </div>  \r\n";
                    strAlert += "    </div>  \r\n";
                    
                    $("#floatingLayer").html(strAlert);
                    
                    $("#floatingLayer .btn_sml").click(function () {
                        disablePopup(item.fadeOut, item.callback);
                    });
                }
            }
            
            if (item.width != 0) {
                $("#floatingLayer").css("width", item.width + "px");
            } else {
                $("#floatingLayer").css("width", "auto");
            }
            
            if (item.fadeOut != -1) {
                window.setTimeout(function () {
                    disablePopup(item.fadeOut, item.callback);
                }, item.setTimeout);
            }
            
            if (!item.isMaskLayerHide) {
                
                $("#maskLayer").css("display", "block");
                $("#maskLayer").css("height", $(document).height() + "px");
            } else {
                
                $("#maskLayer").hide();
            }
            
            $("#floatingLayer").css("left", (($(window).width() - $("#floatingLayer").outerWidth()) / 2) + "px");
            if (jQuery.browser.msie && jQuery.browser.version === "6.0") {
                $("#floatingLayer").css("top", (($(window).height() - $("#floatingLayer").outerHeight()) / 2) + parseInt(GetScrollTop() || 0) + "px");
            } else {
                $("#floatingLayer").css("top", (($(window).height() - $("#floatingLayer").outerHeight()) / 2) + "px");
            }
            
            $("#floatingLayer").show();
            
            if (item.left != 0) {
                
                var left = parseInt($("#floatingLayer").css("left"));
                left += item.left;
                
                $("#floatingLayer").css("left", left + "px");
            }
            
            if (item.top != 0) {
                
                var top = parseInt($("#floatingLayer").css("top"));
                top += item.top;
                
                $("#floatingLayer").css("top", top + "px");
            }
            
            return item.returnVal;
        }
    }
}
