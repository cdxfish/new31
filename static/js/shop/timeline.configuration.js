






function showSharePage(pageUrl, pageTitle, photoUrl) {

    $.post(URL_AJAX_GET_SHARE_PAGE_HTML, { pageUrl: pageUrl, pageTitle: pageTitle, photoUrl: photoUrl }, function (result) {
                
            if(result.Success){
                var html = result.Data;

                    dialog("share", [{ val: "share",text: html, isPanel: true, fadeOut: -1, width: 600 } ]);
            }else{
                    
                alert(result.Message);
                return false;
            }
        });
    }

//    function shareTimeLine(pageUrl,pageTitle,imageIDs) {
//        dialog("l", [{ val: "l", title: "正在为你生成拼图，请稍候...", className: "l", fadeOut: -1, width: 220}]);
//        $.post(URL_AJAX_SHARE_TIMELINE, { ImageIDs: imageIDs }, function (res) {
//            if (res.Success) {
//                showSharePage(pageUrl, pageTitle, res.Data.imageUrl);
//            }else{
//               alert(res.Message);
//               closePopupNow();
//            }
//        });
//   }

//   function sharePhotos(pageUrl,pageTitle,imageIDs) {
//       dialog("l", [{ val: "l", title: "正在为你生成拼图，请稍候...", className: "l", fadeOut: -1, width: 220}]);
//        $.post(URL_AJAX_SHARE_PHOTOS, { ImageIDs: imageIDs }, function (res) {
//            if (res.Success) {
//                showSharePage(pageUrl, pageTitle, res.Data.imageUrl);
//            }else{
//               alert(res.Message);
//               closePopupNow();
//            }
//        });
//    }




$(".bgBox .bg").load(function () {

    setTimeout(function () {

        ImageScrollUp();

    }, 500);


});

function ImageScrollUp() {
    var imgHeight = $(".bgBox .bg").height();
    var top = 0 - imgHeight + 300 + 24;

    if (top < -50) {
        var time = 70 * Math.abs(top);

        $(".bgBox .bg").animate({ "margin-top": top }, time, "linear", function () {

            setTimeout(function () {
                ImageScrollDown(time);
            }, 3000);

        });
    }
}

function ImageScrollDown(time) {
    $(".bgBox .bg").animate({ "margin-top": 0 }, time, "linear", function () {

        setTimeout(function () {
            ImageScrollUp();
        }, 3000);

    });
}