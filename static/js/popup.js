$(document).ready(function() {
    //动态写入 弹出层
    $('body').append('<div id="floatingLayer" style="width:auto;display:none;"></div><div id="maskLayer" style="display:none;"></div>');

    if (jQuery.browser.msie && jQuery.browser.version === "6.0") {
        $("#floatingLayer").css("position", "absolute");
    } else {
        $("#floatingLayer").css("position", "fixed");
    }

});

CaiDianDialogScroll = function() {
    $("#floatingLayer").css("top", ($(window).height() - $("#floatingLayer").outerHeight()) / 2) + parseInt(GetScrollTop() || 0) + "px";

}

closePopupNow = function() {

    $("#maskLayer").hide();
    $("#floatingLayer").hide();
}

closePopup = function() {
    disablePopup(800, null);
}

//使用Jquery去除弹窗效果
disablePopup = function(fadeOut, callback) {

    $("#maskLayer").fadeOut(fadeOut);
    $("#floatingLayer").fadeOut(fadeOut, callback);

}

dialogPloy = function() {

    $("#floatingLayer").css("left", (($(window).width() - $("#floatingLayer").outerWidth()) / 2) + "px");
    if (jQuery.browser.msie && jQuery.browser.version === "6.0") {
        $("#floatingLayer").css("top", (($(window).height() - $("#floatingLayer").outerHeight()) / 2) + parseInt(GetScrollTop() || 0) + "px");
    } else {
        $("#floatingLayer").css("top", (($(window).height() - $("#floatingLayer").outerHeight()) / 2) + "px");
    }

}




timeClosePopup = function(message, time) {
    dialog("a", [{
        val: "a",
        title: message,
        className: "a",
        fadeOut: -1,
        width: 220
    }]);

    setTimeout(

    function() {
        closePopupNow();
    },
    time);
}

dialogMsg = function(data, f) {
    if (data.error) {
        share = data.message;
        timeClosePopup(data.message, 1000);

    } else {
        // share = f(data);
        dialog("share", [{
            val: "share",
            text: f(data),
            isPanel: true,
            fadeOut: -1,
            width: 360
        }]);

    }


}

dialogMsgAndReload = function(data, f, t) {
    var time = !t ? 1500 : t;
    if (data.error) {
        timeClosePopup(data.message, time);
        setTimeout('window.location.reload()', time);
    } else {
        if (f) {
            f(data);
        }
    }
}



dialog = function(res, obj) {

    //dialog-valid √, dialog-error ⅹ, dialog-warning !, dialog-loading …
    for (var i = 0; i < obj.length; i++) {
        var item = {
            val: obj[i].val || "",
            className: obj[i].className || "x",
            title: obj[i].title || "",
            text: obj[i].text || "",
            //hideHead: obj[i].hideHead || false,
            isPanel: obj[i].isPanel || false,
            isMaskLayerHide: obj[i].isMaskLayerHide || false,
            //hideConfirm: obj[i].hideConfirm || null,
            //hideClose: obj[i].hideClose || false,
            setTimeout: obj[i].setTimeout || 1500,
            fadeOut: obj[i].fadeOut || 800,
            returnVal: obj[i].returnVal || false,
            callback: obj[i].callback || null,
            width: obj[i].width || 0,
            top: obj[i].top || 0,
            left: obj[i].left || 0
        };

        if (res == item.val) {

            $("#floatingLayer").html("");
            $("#floatingLayer").removeClass().addClass("popup");

            if (item.isPanel) {

                $("#floatingLayer").html(item.text);

            } else {

                if (item.className == "l") {

                    var strAlert = "    <span class=\"loading\">" + item.title + "</span>  \r\n";

                    $("#floatingLayer").html(strAlert);

                    $("#floatingLayer").addClass("message");

                    item.width = 220;
                    item.fadeOut = -1;
                } else if (item.className == "a") {

                    var strAlert = "    <span class=\"\">" + item.title + "</span>  \r\n";

                    $("#floatingLayer").html(strAlert);

                    $("#floatingLayer").addClass("message");

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

                    $("#floatingLayer .btn_sml").click(function() {
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
                window.setTimeout(function() {
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