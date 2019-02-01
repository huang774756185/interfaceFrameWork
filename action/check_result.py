#encoding=utf-8
import re
import demjson
import json

class CheckResult(object):
    def __init__(self):
        pass

    @classmethod
    def check(self, responseObj, checkPoint):
        errorKey = {}
        for key, value in checkPoint.items():
            if isinstance(value, (str, unicode,int)):
                print "value=%s"%value
                #说明是等值校验
                print type(json.dumps( demjson.encode(responseObj)))
                if  responseObj[key] != value:

                    errorKey[key] = responseObj[key]
            elif isinstance(value, dict):
                #说明是需要通过正则表达式去校验
                sourceData = responseObj[key] #接口返回的真实值
                if value.has_key("value"):
                    # 说明是通过正则校验
                    regStr = value["value"]
                    rg = re.match(regStr, "%s" %sourceData)
                    if not rg:
                        errorKey[key] = sourceData
                elif value.has_key("type"):
                    # 说明是校验数据类型
                    typeS = value["type"]
                    if typeS == "N":
                        # 说明是整形
                        if not isinstance(sourceData,(int, long)):
                            errorKey[key] = sourceData
                            print u"类型为%s"%sourceData
        return errorKey

if __name__ == '__main__':
    r = {u'message': u'\u5185\u90e8\u5f02\u5e38', u'code': 500, u'result': None}
    c = {u'code': 200}
    print CheckResult.check(r, c)




