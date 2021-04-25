# from selenium import webdriver
#
# driver = webdriver.Chrome('chromedriver')
#
# driver.get('https://nid.naver.com/nidlogin.login?url=https%3A%2F%2Fsell.smartstore.naver.com%2F%23%2FnaverLoginCallback%3Furl%3Dhttps%253A%252F%252Fsell.smartstore.naver.com%252F%2523')
# driver.find_element_by_name('id').send_keys('hdh5454')
# driver.find_element_by_name('pw').send_keys('whdmsehgud8*')
# driver.find_element_by_id('log.login').click()



########################################################################


import gspread
from oauth2client.service_account import ServiceAccountCredentials

#무슨 api쓸지 scope에 담아
scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive',
]

json_file_name = 'ssautomation-982798f8cc3e.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scope)
gc = gspread.authorize(credentials)
spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1_MldxRro1qK-OXy7HgQDEWR2ZiTyU9dbcAnCkANeGTY/edit#gid=57693791'
# 스프레스시트 문서 가져오기
doc = gc.open_by_url(spreadsheet_url)
# 시트 선택하기
worksheet = doc.worksheet('장부')
empty_row = worksheet.acell('B12').value #다음 빈 행




worksheet.insert_row(['4/22','맥스'],int(empty_row))