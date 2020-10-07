var currentCid = 1; // 当前分类 id
var cur_page = 1; // 当前页
var total_page = 1;  // 总页数
var data_querying = true;   // 是否正在向后台获取数据
//保存图片验证码编号：全局变量
// var imageCodeId = "";

// $(document).ready(function () {
//
//     $('.register_btn').click(function () {
//         generateImageCode();
//         // $("[name='checkbox']").removeAttr("checked");
//     })
//     $("#mobile").focus(function () {
//         $("#login-mobile-err").hide();
//     })
//
//     $("#register_mobile").focus(function () {
//         $("#register-mobile-err").hide();
//     });
//     $("#imagecode").focus(function () {
//         $("#register-image-code-err").hide();
//     });
//     $("#smscode").focus(function () {
//         $("#register-sms-code-err").hide();
//     });
//     $("#password").focus(function () {
//         $("#register-password-err").hide();
//         $("#login-password-err").hide()
//     });
//
//
//     //注册
//     $('.register_form_con').submit(function (e) {
//         e.preventDefault();
//         var mobile = $('#register_mobile').val();
//         var sms_code = $('#smscode').val();
//         var password = $('#register_password').val();
//         var check = $('input[type=checkbox]:checked').val();
//
//         if (mobile == "" || sms_code == "" || password == "") {
//             $("#register-mobile-err").show();
//             $("#register-image-code-err").show();
//             $('#register-password-err').show();
//             return
//         }
//         if (check != "on") {
//             alert("请同意使用条款！");
//             return;
//         }
//
//         var data = {
//             mobile: mobile,
//             sms_code: sms_code,
//             password: password,
//             check: check
//         }
//         var req_data = JSON.stringify(data);
//         $.ajax({
//             url: '/user/register',
//             data: req_data,
//             type: "post",
//             contentType: "application/json",
//             dataType: "json",
//             headers: {
//                 "X-CSRFTOKEN": getCookie("csrf_token")
//             },//将csrf_token值放在请求头，放便csrf进行验证
//             success: function (resp) {
//                 if (resp.errno == "0") {
//                     alert(resp.errmsg);
//                     $('#register_mobile').val("");
//                     $('#imagecode').val("");
//                     $('#smscode').val("");
//                     $('#register_password').val("");
//                     $(".register_form_con").hide()
//                 } else {
//                     alert(resp.errmsg)
//                 }
//             }
//         })
//     })
//
//     //登录
//     $('.login_form_con').submit(function (e) {
//         e.preventDefault();
//         var mobile = $("#mobile").val();
//         var password = $("#password").val();
//         if (mobile == "" || password == "") {
//             $("#login-mobile-err").show();
//             $("#login-password-err").show()
//             return
//         }
//         var data = {
//             mobile: mobile,
//             password: password,
//         }
//         var req_data = JSON.stringify(data);
//
//         $.ajax({
//             url: "/user/login",
//             data: req_data,
//             type: "post",
//             contentType: "application/json",
//             dataType: "json",
//             headers: {
//                 "X-CSRFTOKEN": getCookie("csrf_token")
//             },//将csrf_token值放在请求头，放便csrf进行验证
//             success: function (resp) {
//                 if (resp.errno == "0") {
//                     $(".login_form_con").hide()
//                 } else {
//                     alert(resp.errmsg)
//                 }
//             }
//         })
//     })
//
//
// })

//js读取cookie的方法
// function getCookie(name) {
//     var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
//     //三目运算符
//     // r[1] if r else undefined
//     return r ? r[1] : undefined;
// }

// function sendSMSCode() {
//     var mobile = $('#register_mobile').val();
//     var imageCode = $('#imagecode').val();
//     if (mobile == "" || imageCode == "") {
//         $("#register-mobile-err").show();
//         $("#register-image-code-err").show();
//         return
//     }
//     $.get("/sms_code/" + mobile, {image_code: imageCode, image_code_id: imageCodeId},
//         function (resp) {
//             if (resp.errno != "0") {
//                 $('#register-sms-code-err').html(resp.errmsg);
//                 $('#register-sms-code-err').show();
//                 $(".get_code").attr("onclick", "sendSMSCode();")
//                 generateImageCode();
//
//             } else {
//                 var $time = $(".get_code");
//                 var duration = 60;
//                 var intervalid = setInterval(function () {
//                     $time.html(duration + "秒");
//                     if (duration === 1) {
//                         clearInterval(intervalid);
//                         $time.html('获取验证码');
//                         $(".phonecode-a").attr("onclick", "sendSMSCode();");
//                     }
//                     duration = duration - 1;
//                 }, 1000, 60);
//             }
//         }, 'json')
// }

// function generateUUID() {
//     var d = new Date().getTime();
//     if (window.performance && typeof window.performance.now === "function") {
//         d += performance.now(); //use high-precision timer if available
//     }
//     var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
//         var r = (d + Math.random() * 16) % 16 | 0;
//         d = Math.floor(d / 16);
//         return (c == 'x' ? r : (r & 0x3 | 0x8)).toString(16);
//     });
//     return uuid;
// }

// function generateImageCode() {
//     //形成图片验证码的后端地址，设置到页面中，让浏览器请求验证码图片
//     //编号唯一：时间戳、uuid（全局唯一标识符）
//     imageCodeId = generateUUID();
//     var url = "/image_code/" + imageCodeId;
//     $(".get_pic_code").attr("src", url)
// }

$(function () {

    updateNewsData()
    // 首页分类切换
    $('.menu li').click(function () {
        //获取分类编号
        var clickCid = $(this).attr('data-cid')
        //上个分类选择状态移除
        $('.menu li').each(function () {
            $(this).removeClass('active')
        })
        //将当前选中的分类置为选中状态
        $(this).addClass('active')

        //判断当前是否点击的不是当前编号
        if (clickCid != currentCid) {
            // 记录当前分类id
            currentCid = clickCid

            // 重置分页参数
            cur_page = 1
            total_page = 1
            updateNewsData()
        }
    })

    //页面滚动加载相关
    $(window).scroll(function () {

        // 浏览器窗口高度
        var showHeight = $(window).height();

        // 整个网页的高度
        var pageHeight = $(document).height();

        // 页面可以滚动的距离
        var canScrollHeight = pageHeight - showHeight;

        // 页面滚动了多少,这个是随着页面滚动实时变化的
        var nowScroll = $(document).scrollTop();

        if ((canScrollHeight - nowScroll) < 200) {
            // TODO 判断页数，去更新新闻数据
            if (!house_data_querying) {
                // 将`是否正在向后端查询新闻数据`的标志设置为真
                house_data_querying = true;
                // 如果当前页面数还没到达总页数
                if (cur_page < total_page) {
                    // 向后端发送请求，查询下一页新闻数据
                    updateNewsData();
                } else {
                    house_data_querying = false;
                }
            }
        }
    })
})

function updateNewsData() {
    // TODO 更新新闻数据
    var params = {
        "page": cur_page,
        "cid": currentCid,
        'limit': 10
    }
    $.get("/newsList", params, function (resp) {

        // 设置 `数据正在查询数据` 变量为 false，以便下次上拉加载
        house_data_querying = false

        if (resp) {

            // 记录总页数
            total_page = resp.totalPage

            // 如果当前页数为1，则清空原有数据
            if (cur_page == 1) {
                $(".list_con").html('')
            }
            // 当前页数递增
            cur_page += 1
            // 显示数据
            for (var i = 0; i < resp.news_list.length; i++) {
                var news = resp.news_list[i]
                if (!news.author) {
                    var content = '<li>'
                    content += '<a href="/news/detail/' + news.id + '" class="news_pic fl"><img src="' + news.index_image_url + '?imageView2/1/w/170/h/170"></a>'
                    content += '<a href="/news/detail/' + news.id + '" class="news_title fl">' + news.title + '</a>'
                    content += '<a href="/news/detail/' + news.id + '" class="news_detail fl">' + news.digest + '</a>'
                    content += '<div class="author_info fl">'
                    content += '<div class="source fl">来源：' + news.source + '</div>'
                    content += '<div class="time fl">' + news.create_time + '</div>'
                    content += '</div>'
                    content += '</li>'
                } else {
                    var content = '<li>'
                    content += '<a href="/news/detail/' + news.id + '" class="news_pic fl"><img src="' + news.index_image_url + '?imageView2/1/w/170/h/170"></a>'
                    content += '<a href="/news/detail/' + news.id + '" class="news_title fl">' + news.title + '</a>'
                    content += '<a href="/news/detail/' + news.id + '" class="news_detail fl">' + news.digest + '</a>'
                    content += '<div class="author_info fl">'
                    content += '<div class="author fl">'
                    if (news.author.avatar_url == null) {
                        content += '<img src="../../static/news/images/person.png" alt="author">' + '<a href="#">' + news.author.nick_name + '</a></div>'
                    } else {
                        content += '<img src="' + news.author.avatar_url + '" alt="author">' + '<a href="#">' + news.author.nick_name + '</a></div>'
                    }
                    content += '<div class="time fl">' + news.create_time + '</div>'
                    content += '</div>'
                    content += '</li>'
                }

                $(".list_con").append(content)
            }
        }
    })


}
