# __Time__ : 2020/10/7 下午4:04
# __Author__ : '__YDongY__'

import json

from ronglian_sms_sdk import SmsSDK
from info import constants


class CCP(object):
    def __new__(cls, *args, **kwargs):
        # 判断是否存在类属性_instance，_instance是类CCP的唯一对象，即单例
        if not hasattr(CCP, "_instance"):
            cls._instance = super(CCP, cls).__new__(cls, *args, **kwargs)
            cls._instance.rest = SmsSDK(constants.ACCOUNT_SID,
                                        constants.ACCOUNT_TOKEN,
                                        constants.APP_ID)
        return cls._instance

    def send_template_sms(self, to, datas, temp_id):
        """发送模板短信"""
        # @param to 手机号码
        # @param datas 内容数据 格式为数组 例如：{'12','34'}，如不需替换请填 ''
        # @param temp_id 模板Id
        result = self.rest.sendMessage(tid=temp_id, mobile=to, datas=datas)
        result = json.loads(result)
        # 如果云通讯发送短信成功，返回的字典数据 result 中 statuCode 字段的值为"000000"
        if result.get("statusCode") == "000000":
            # 返回0 表示发送短信成功
            return 0
        else:
            # 返回-1 表示发送失败
            return -1


if __name__ == '__main__':
    ccp = CCP()
    ccp.send_template_sms("17629034346", ["1234", "5"], 1)
