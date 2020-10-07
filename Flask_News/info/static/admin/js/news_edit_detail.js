$(function () {
    $(".news_edit").submit(function (e) {
        // 阻止表单默认提交行为
        e.preventDefault();
        // var news_title = $(".input_txt2").val();
        // var news_category_id = $('.sel_opt option:selected').val();
        // var news_digest = $(".input_multxt").val();
        // var news_image_url = $(".index_pic").attr("src");
        // var news_content = $(".input_area").val();
        // var id = $(".confirm").attr("data-news-id")

        // alert(news_title)
        // alert(news_category_id)
        // alert(news_digest)
        // alert(news_image_url)
        // alert(news_content)
        // alert(id)

        // var req_dict = {
        //     "news_image_url": news_image_url,
        //     "news_title": news_title,
        //     "news_category_id": news_category_id,
        //     "news_content": news_content,
        //     "news_digest": news_digest
        // }


        // TODO 新闻编辑提交
        $(this).ajaxSubmit({
            beforeSubmit: function (request) {
                // 在提交之前，对参数进行处理
                for (var i = 0; i < request.length; i++) {
                    var item = request[i]
                    if (item["name"] == "content") {
                        item["value"] = tinyMCE.activeEditor.getContent()
                    }
                }
            },
            url: "/admin/news_edit_detail",
            type: "post",
            // data: JSON.stringify(req_dict),
            // dataType: "json",
            // contentType: "application/json",
            headers: {
                "X-CSRFToken": getCookie('csrf_token')
            },
            success: function (resp) {
                if (resp.errno == "0") {
                    // 返回上一页，刷新数据
                    location.href = document.referrer;
                } else {
                    alert(resp.errmsg);
                }
            }
        })
    })
});

// 点击取消，返回上一页
function cancel() {
    history.go(-1);
}

// 获取cookie
function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}