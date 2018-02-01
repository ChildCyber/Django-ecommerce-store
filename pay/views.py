# -*- coding: utf-8 -*-
import os
import time

from django.conf import settings
from django.shortcuts import redirect, render

from alipay import AliPay


# Create your views here.
def ali():
    # 商户app_id
    app_id = settings.ALIPAY_APPID
    # 服务器异步通知页面路径 需http: // 格式的完整路径，不能加?id = 123 这类自定义参数，必须外网可以正常访问
    # 发post请求
    notify_url = "http://127.0.0.1:8000/pay/pay/"

    alipay = AliPay(
        appid=app_id,
        app_notify_url=notify_url,
        app_private_key_path=os.path.join(settings.BASE_DIR, "pay/app_private_key.pem"),
        alipay_public_key_path=os.path.join(settings.BASE_DIR, "pay/alipay_public_key.pem"),  # 支付宝的公钥
        debug=True,  # 默认False,
    )
    return alipay


def pay(request):
    if request.method == "GET":
        return render(request, 'pay/pay.html')
    else:
        subject = u"测试订单".encode("utf-8")
        money = float(request.POST.get('money'))
        alipay = ali()
        # 生成支付的url
        query_params = alipay.api_alipay_trade_page_pay(
            subject=subject,  # 商品简单描述
            out_trade_no="x2" + str(time.time()),  # 商户订单号
            total_amount=money,  # 交易金额(单位: 元 保留俩位小数)
        )

        pay_url = "https://openapi.alipaydev.com/gateway.do?{}".format(query_params)
        # 支付宝网关链接，去掉dev就是生产环境了。
        return redirect(pay_url)
