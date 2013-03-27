

$(document).ready(function () {
    $("#span_more_count").html(moreCount);

    $(window).scroll(function () {
        onPhotoViewWindowSrcoll();
    });

});

function mod(s, t) {
    return ((s % t) == 0 ? t : s % t);
}
function onPhotoViewWindowSrcoll() {

    fixedTopPhotoView();

    if (!isEnd) {
        var scrollTop = GetScrollTop();
        var winHeight = $(window).height();

        var ulTop = $(".pinBox").offset().top;
        var ulHeight = $(".pinBox").outerHeight();

        if (scrollTop + winHeight + 100 >= ulTop + ulHeight) {

            isEnd = true;
            pageIndex++;
            ajaxData.PageIndex = pageIndex;

            getPhotoViewMore();
        }
    }

}



function fixedTopPhotoView() {
    if (!(jQuery.browser.msie && jQuery.browser.version === "6.0")) {

        if ($(window).scrollTop() >= $(".viewDown").offset().top) {

            $(".userInfoBox").css({ "position": "fixed", "top": "0" })
        }
        else {
            $(".userInfoBox").css({ "position": "relative", "top": "0" })
        }
    }
}

function getPhotoViewMoreClick() {
    isEnd = false;

    $("#container_bottom_bar").hide();
    $("#container_bottom_recommend").hide();

    onPhotoViewWindowSrcoll();

    trackclick("bottomnext");
}

function getPhotoViewMore() {

    $(".photoBox").after("<p class=\"moreLoading\"><span class=\"loading_black\"></span>正在加载...</p>");

    $.post(ajaxUrl, ajaxData, function (result) {

        if (result.Success) {
            $(".moreLoading").remove();
            $(".photoBox").append(result.Data[1]);
            if (result.Data[0] == "false") {
                isEnd = false;

                if (pageIndex % 5 == 0) {
                    isEnd = true;

                    $("#container_bottom_bar").show();
                    $("#container_bottom_recommend").show();


                    var moreCount = recordCount - pageSize * pageIndex;
                    if (moreCount > 0) {
                        $("#span_more_count").html(moreCount);
                    }
                    else {
                        $(".showMorePhoto").html(coverUrl);
                    }
                }
            }
            else {

                $("#container_bottom_bar").show();
                $("#container_bottom_recommend").show();

                $(".showMorePhoto").html(coverUrl);
            }
        }
    });
}


var user;
function setCurrentUser(usr) {
    user = usr;
}
 
 function saveComment(photoId) { 
        
        var content=$("#txtComment"+photoId).val();
        var parentid = $("#txtComment" + photoId).attr("parent");

        if(content.length<=0)
        {
            alert("请输入评论内容");
            $("#txtComment"+photoId).focus();
                   
            return false;
        }

        $("#reply" + photoId + " > a").hide();
        $("#reply" + photoId).append("<span class=\"loading_black\"></span>");

        $.post(URL_AJAX_SAVE_COMMENT,
        {
            photoid: photoId,
            content: content,
            parentid: parentid
        },
        function (result) {
            if (result.Success) {
                var comment = result.Data;

                var html = "";

                html = html + "<li id=\"liComment" + comment.ID + "\">";
                html = html + "<a class=\"fl\" href=\"" + user.url + "\"><img width=\"24\" height=\"24\" alt=\"@user.Name\" src=\"" + user.avatar + "\"></a>";
                html = html + "<div class=\"box\">";
                html = html + "<h5><a href=\"" + user.url + "\">" + user.name + "</a><span>刚刚</span></h5>";
                html = html + " <p>" + content + "</p>";
                html = html + "</div>";
                html = html + "<a onclick=\"DeleteComment('" + photoId + "','" + comment.ID + "');\" href=\"javascript:void(0)\" class=\"replay\">删除</a>  ";
                html = html + "</li>";

                $("#comment" + photoId).find("ul").append(html);
                $("#txtComment" + photoId).val("");
                $("#txtComment" + photoId).attr("parent", "");

                var commentCount = parseInt($("#commentCount" + photoId).html());

                commentCount++;

                $("#commentCount" + photoId).html(commentCount);
            }
            else {
                alert(result.Message);
            }

            $("#reply" + photoId + " > a").show();
            $("#reply" + photoId + " > .loading_black").remove();

        });

    }
    function reComment(photoId, commentId, username) {

      
        $('#txtComment' + photoId).val('回复' + username + '说:');
        $('#txtComment' + photoId).attr("parent", commentId);
    }
    function hideComments(id){

        $("#comment" + id).slideUp("slow", function (){ $(this).remove(); });
    }

    function DeleteComment(photoId, commentId) {

        if (confirm("确定删除该评论")) {
            $.post(URL_AJAX_Delete_PHOTO_COMMENT,
                                        {
                                            CommentId: commentId
                                        },
                                        function (result) {

                                            if (result.Success) {


                                            }

                                            $("#liComment" + commentId).slideUp("fast", function () {

                                                $("#liComment" + commentId).remove();
                                            });

                                            var commentCount = parseInt($("#commentCount" + photoId).html());

                                            commentCount--;

                                            $("#commentCount" + photoId).html(commentCount);

                                        });
        }
    }

    function showComments(id) {


        if ($("#comment" + id).length > 0) {

            $("#comment" + id).slideUp("slow", function () { $(this).remove(); });
        }
        else {

            $.post(URL_AJAX_GET_PHOTO_COMMENT,
                                        {
                                            id: id

                                        },
                                        function (result) {

                                            if (result.Success) {
                                                var html = result.Data;
                                                $("#" + id).find(".aside").append(html);
                                            }

                                        });

        }
    }

    function GoPhotoEditPage(photoID, pageUrl) {

        var backID = "";

        var backObj = $("#" + photoID).prev();
        if (backObj.length > 0) {
            backID = backObj.attr("id");
        }
        else {
            backObj = $("#" + photoID).next();
            if (backObj.length > 0) {
                backID = backObj.attr("id");
            }
        }

        location.href = pageUrl + "&backID=" + backID;

    }

    