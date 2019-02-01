#encoding=utf-8
import requests
import json
from utils.ParseExcel import ParseExcel
from config.public_data import *
from utils.HttpClient import HttpClient
from action.get_rely import GetKey
from action.data_store import RelyDataStore
from action.check_result import CheckResult
from action.write_test_result import write_result

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def main():

	parseE = ParseExcel()
	parseE.loadWorkBook(file_path)
	sheetObj = parseE.getSheetByName(u"API")
	activeList = parseE.getColumn(sheetObj, API_active)
	print activeList
	for idx, cell in enumerate(activeList[1:], 2):
		if cell.value == "y":
			# 需要执行的接口所在行的行对象
			rowObj = parseE.getRow(sheetObj, idx)
			apiName = rowObj[API_apiName - 1].value
			requestUrl = rowObj[API_requestUrl - 1].value
			requestMethod = rowObj[API_requestMothod - 1].value
			paramsType = rowObj[API_paramsType - 1].value
			apiTestCaseFileName = rowObj[API_apiTestCaseFileName - 1].value

			# 下一步读用例sheet表，准备执行测试用例
			caseSheetObj = parseE.getSheetByName(apiTestCaseFileName)
			caseActiveObj = parseE.getColumn(caseSheetObj, CASE_active)
			for c_idx, col in enumerate(caseActiveObj[1:], 2):
				if col.value == "y":
					# 说明此case行需要执行
					caseRowObj = parseE.getRow(caseSheetObj, c_idx)
					requestData = caseRowObj[CASE_requestData - 1].value
					relyData = caseRowObj[CASE_relyData - 1].value
					dataStore = caseRowObj[CASE_dataStore - 1].value
					checkPoint = caseRowObj[CASE_checkPoint - 1].value
					headers = caseRowObj[CASE_headers - 1].value
					print headers
					if relyData:
						# 发送接口请求之前，先做依赖数据的处理
						requestData = "%s" %GetKey.get(eval(requestData), eval(relyData))
					# 拼接接口请求参数，发送接口请求
					httpC = HttpClient()
					# print requestMethod, requestUrl, paramsType, requestData
					response = httpC.request(requestMethod = requestMethod,
								  requestUrl = requestUrl,
								  paramsType = paramsType,
								  requestData = requestData,
								  headers=headers
								  )
					print response.text
					if response.status_code == 200:
						responseData = response.json()#对比json
						responseText = response.text
						# 存储依赖数据
						if dataStore:
							RelyDataStore.do(eval(dataStore),apiName, c_idx - 1, eval(requestData),responseData)
						# 比对结果
						errorKey = CheckResult.check(responseData, eval(checkPoint))
						print type(responseData)
						write_result(parseE, caseSheetObj,responseText, errorKey, c_idx)#讲返回的报文体填入结果
					else:
						responseData = response.json()
						responseText = response.text
						print "错误json%s"%responseData
						errorKey = CheckResult.check(responseData, eval(checkPoint))
						print responseData,type(eval(checkPoint))
						write_result(parseE, caseSheetObj, responseText,errorKey,c_idx)
						print errorKey

						print responseData
				else:
					print "用例被忽略执行"
		else:
			print "接口被设置忽略执行"

if __name__ == '__main__':
	main()

