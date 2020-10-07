function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}


$(function () {

    $(".focused").click(function () {
        // TODO 取消关注当前新闻作者
        var user_id = $(this).attr("data-user-id")
        action = "noattention"
        var req_dict = {
            user_id: user_id,
            action: action,
        }
        $.ajax({
            url: "/user/user_like",
            type: "post",
            dataType: "json",
            data: JSON.stringify(req_dict),
            contentType: "application/json",
            headers: {
                "X-CSRFToken": getCookie("csrf_token")
            },
            success: function (resp) {
                if (resp.errno = "0") {
                    $(".author_card").remove();
                } else {
                    alert(resp.errmsg)
                }
            }
        })
    })
})