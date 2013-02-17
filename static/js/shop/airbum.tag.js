$(document).ready(function () {
    weiboShare();
    buyBtn();
});



// 微博分享
function weiboShare() {
    var weiboShare = $('<div class=\"weiboShare\"><a href=\"javascript:void(0);\" onclick=\"SharePhotos();\">微博分享</a></div>').appendTo($("body"))
        .click(function () {
            ShareHtml('/m/DSC_3500.jpg');
            // dialog("l", [{ val: "l", title: "正在为你生成分享的图片，请稍候...", className: "l", fadeOut: -1, width: 220}]);
        });

}

function buyBtn(){
    $('.btnReplay').click(function(){
        dialog("l", [{ val: "l", title: "正在为您获取规格，请稍候...", className: "l", fadeOut: -1, width: 220}]);
        buyHtml();
        return false;
    });
}

function ShareHtml(uploadShareImage, linkText, pageUrl, sinaUrl, qqUrl, sohuUrl) {
    
    var share ='   <p><a class=\"btn_close\" href=\"javascript:void(0);\" onclick=\"closePopupNow();\">关闭</a></p>';
    share +='   <div class=\"shareSelectBox\">  \r\n';
    share +='      <div class=\"shareYourPhotosL\"><img width=\"300px\" src=\"" + uploadShareImage + "\" alt=\"\"/></div>  \r\n';
    share +='      <div class=\"shareYourPhotosR\"><h3>把上传的照片分享到</h3>  \r\n';
    share +='          <ul>  \r\n';

    share +='            <li><a target=\"_blank\" href=\"" + sinaUrl + "\"><img src=\"' + 'http://ui.caidian.com/default/sns/t.sina.png' + '\" height=\"50\" width=\"120\" alt=\"\"/></a></li>  \r\n';
    share +='            <li><a target=\"_blank\" href=\"" + qqUrl + "\"><img src=\"' + 'http://ui.caidian.com/default/sns/t.qq.png' + '\" height=\"50\" width=\"120\" alt=\"\"/></a></li>  \r\n';
    share +='            <li><a target=\"_blank\" href=\"" + sohuUrl + "\"><img src=\"' + 'http://ui.caidian.com/default/sns/t.sohu.png' + '\" height=\"50\" width=\"120\" alt=\"\"/></a></li>  \r\n';

    share +='          </ul>  \r\n';
    share +='          <h3>分享照片地址<span>(适用于论坛博客)</span></h3>  \r\n';
    share +='          <textarea><a href=\"" + pageUrl + "\" target=\"_blank\">" + linkText + "</a></textarea>  \r\n';
    share +='      </div>  \r\n';
    share +='   </div>  \r\n';

    dialog("share", [{ val: "share", text: share, isPanel: true, fadeOut: -1, width: 760}]);

    $("#floatingLayer").addClass("popup800");

}

function buyHtml(uploadShareImage, linkText, pageUrl, sinaUrl, qqUrl, sohuUrl) {
    
    var share ='   <p><a class=\"btn_close\" href=\"javascript:void(0);\" onclick=\"closePopupNow();\">关闭</a></p>';
    share +='   <div class=\"shareSelectBox\">  \r\n';
    share +='      <div class=\"buySpc\"><h3>请选择规格</h3>  \r\n';
    share +='        <table>  \r\n';
    share +='          <tr>  \r\n';
    share +='             <td>1.5磅：约16×16(cm)</td>  \r\n';
    share +='             <td>￥179.00 元</td>  \r\n';
    share +='             <td><a href="#" class="btnB sBtn">购买</a></td>  \r\n';
    share +='          </tr>  \r\n';
    share +='          <tr>  \r\n';
    share +='             <td>2.5磅：约18×18(cm)</td>  \r\n';
    share +='             <td>￥284.00 元</td>  \r\n';
    share +='             <td><a href="#" class="btnB sBtn">购买</a></td>  \r\n';
    share +='          </tr>  \r\n';
    share +='          <tr>  \r\n';
    share +='             <td>3.5磅：约20×20(cm)</td>  \r\n';
    share +='             <td>￥417.00 元</td>  \r\n';
    share +='             <td><a href="#" class="btnB sBtn">购买</a></td>  \r\n';
    share +='          </tr>  \r\n';
    share +='          <tr>  \r\n';
    share +='             <td>5.5磅：约26×26(cm)</td>  \r\n';
    share +='             <td>￥634.00 元</td>  \r\n';
    share +='             <td><a href="#" class="btnB sBtn">购买</a></td>  \r\n';
    share +='          </tr>  \r\n';
    share +='             <td>10.0磅：约36×36(cm)</td>  \r\n';
    share +='             <td>￥1073.00 元</td>  \r\n';
    share +='             <td><a href="#" class="btnB sBtn">购买</a></td>  \r\n';
    share +='          </tr>  \r\n';
    share +='        </table>  \r\n';
    share +='      </div>  \r\n';
    share +='   </div>  \r\n';

    dialog("share", [{ val: "share", text: share, isPanel: true, fadeOut: -1, width: 320}]);

    // $("#floatingLayer").addClass("popup800");

}