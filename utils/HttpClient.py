#encoding=utf-8
import requests
import json

class HttpClient(object):
    def __init__(self):
        pass


    def request(self, requestMethod, requestUrl, paramsType,
               requestData = None, headers = None, cookies = None):
        if requestMethod.lower() == "post":
            if paramsType == "form":
                response = self.__post(url = requestUrl, data=json.dumps(eval(requestData)),
                                       headers = eval(headers), cookies=cookies)
                return response
            elif paramsType == "json":
                response = self.__post(url=requestUrl, json=json.dumps(eval(requestData)),
                                       headers=headers, cookies=cookies)
                return response
        elif requestMethod == "get":
            if paramsType == "url":
                request_url = "%s%s" %(requestUrl, requestData)
                response = self.__get(url = request_url, headers=headers, cookies=cookies)
                return response
            elif paramsType == "params":
                response = self.__get(url=requestUrl, params = requestData,
                                      headers = headers, cookies = cookies)
                return response

    def __post(self, url, data=None, json=None,  headers =None ,**kwargs):
        response = requests.post(url = url, data = data, json= json,headers=headers)
        return response

    def __get(self, url, params = None, **kwargs):
        response = requests.get(url = url, params = params)
        return response

if __name__ == '__main__':
    hc = HttpClient()
    datal={
      "categry": 3,
      "subCategry": 31,
      "name": "string",
      "label": "string",
      "shortName": "string",
      "expectedAmount": 0,
      "financier": "string",
      "investmentArea": "string",
      "managerId": "string",
      "productCode": "string",
      "investmentSubject": "string",
      "investmentTargets": "string",
      "investorNumLimit": 0,
      "repaymentSource": "string",
      "riskControl": "string",
      "riskLevel": 0,
      "term": "string",
      "termDescription": "string",
      "builtTime": "2019-01-29T06:33:56.891Z",
      "productDirector": "string",
      "consignee": "string",
      "consigneeIntroduction": "string",
      "financierIntroduction": "string",
      "highlights": "string",
      "contract": "string",
      "otherAttachment": "string",
      "productIntroduction": "string",
      "prospectus": "string",
      "publicityTable": "string",
      "smsIntroduction": "string",
      "raiseAccountName": "string",
      "raiseBank": "string",
      "raiseAccount": "string",
      "raiseRemark": "string",
      "subscriptionFee": "string",
      "buyStart": 0,
      "subscriptionDesc": "string",
      "increaseAmt": 0,
      "otherFee": "string",
      "openDay": "string",
      "openDayRemark": "string",
      "createUserName": "string",
      "createTime": "2019-01-29T06:33:56.891Z",
      "createUserId": "string",
      "updateUserName": "string",
      "updateTime": "2019-01-29T06:33:56.891Z",
      "updateUserId": "string"
}
    headers = {'Content-Type': 'application/json'}
    type(datal)
    res=hc.request(requestMethod="post" ,
                   paramsType="form",requestUrl ="http://192.168.17.101:41200/api/product/bond",
                   requestData=json.dumps(datal),headers=headers)

    print res.url
    print res.headers
    print res.text

















