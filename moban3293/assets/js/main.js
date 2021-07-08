var imageCodeId = ""
;(function () {
	

	'use strict';

	// Placeholder 
	var placeholderFunction = function() {
		$('input, textarea').placeholder({ customClass: 'my-placeholder' });
	}
	
	// Placeholder 
	var contentWayPoint = function() {
		var i = 0;
		$('.animate-box').waypoint( function( direction ) {

			if( direction === 'down' && !$(this.element).hasClass('animated-fast') ) {
				
				i++;

				$(this.element).addClass('item-animate');
				setTimeout(function(){

					$('body .animate-box.item-animate').each(function(k){
						var el = $(this);
						setTimeout( function () {
							var effect = el.data('animate-effect');
							if ( effect === 'fadeIn') {
								el.addClass('fadeIn animated-fast');
							} else if ( effect === 'fadeInLeft') {
								el.addClass('fadeInLeft animated-fast');
							} else if ( effect === 'fadeInRight') {
								el.addClass('fadeInRight animated-fast');
							} else {
								el.addClass('fadeInUp animated-fast');
							}

							el.removeClass('item-animate');
						},  k * 200, 'easeInOutExpo' );
					});
					
				}, 100);
				
			}

		} , { offset: '85%' } );
	};
	// On load
	$(function(){
		placeholderFunction();
		contentWayPoint();

	});

}());

// 发送短信验证码
function sendSMSCode() {
    // 校验参数，保证输入框有数据填写
    $(".get_code").removeAttr("onclick");
    var mobile = $("#phone").val();
    if (!mobile) {
        $("#register-err").html("请填写正确的手机号！");
        $("#register-err").show();
        $(".get_code").attr("onclick", "sendSMSCode();");
        return;
    }
    var imageCode = $("#imagecode").val();
    if (!imageCode) {
        $("#register-err").hide();
        $("#register-err").html("请填写验证码！");
        $("#register-err").show();
        $(".get_code").attr("onclick", "sendSMSCode();");
        return;
    }

    // 发送短信验证码
    var params = {
        "mobile": mobile,
        "image_code": imageCode,
        "image_code_id": imageCodeId
    };

    $.ajax({
        // 请求地址
        url: "/smscode",
        // 请求方式
        method: "POST",
        // 请求内容
        data: JSON.stringify(params),
        // 请求内容的数据类型
        contentType: "application/json",
        // 响应数据的格式
        dataType: "json",
        success: function (resp) {
            if (resp.errno == "0") {
                // 倒计时60秒，60秒后允许用户再次点击发送短信验证码的按钮
                var num = 60;
                // 设置一个计时器
                var t = setInterval(function () {
                    if (num == 1) {
                        // 如果计时器到最后, 清除计时器对象
                        clearInterval(t);
                        // 将点击获取验证码的按钮展示的文本回复成原始文本
                        $(".get_code").html("获取验证码");
                        // 将点击按钮的onclick事件函数恢复回去
                        $(".get_code").attr("onclick", "sendSMSCode();");
                    } else {
                        num -= 1;
                        // 展示倒计时信息
                        $(".get_code").html(num + "秒");
                    }
                }, 1000)
            } else {
                // 表示后端出现了错误，可以将错误信息展示到前端页面中
                $("#register-err").html(resp.errmsg);
                $("#register-err").show();
                // 将点击按钮的onclick事件函数恢复回去
                $(".get_code").attr("onclick", "sendSMSCode();");
                // 如果错误码是4004，代表验证码错误，重新生成验证码
                if (resp.errno == "4004") {
                      $('#captcha_img').click(function () {
                        //点击验证码图片 换新的图片,如果src的值没改变 不会重新请求
                        // {#$(this).prop('src', "/member/image_code?id=" + Math.random())#}
                        $(".get_pic_code").attr("src", "/member/image_code?id=" + Math.random())
                    })

                }
            }
        }
    })
}