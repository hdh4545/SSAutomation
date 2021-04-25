from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

smartstorelogin_url = 'https://nid.naver.com/nidlogin.login?url=https%3A%2F%2Fsell.smartstore.naver.com%2F%23%2FnaverLoginCallback%3Furl%3Dhttps%253A%252F%252Fsell.smartstore.naver.com%252F%2523'
smartstoredelevery_url = 'https://sell.smartstore.naver.com/#/naverpay/sale/delivery?summaryInfoType=DELIVERY_READY'
smartstore_id = 'hdh5454'
smartstore_pw = 'whdmsehgud8*'

driver = webdriver.Chrome('chromedriver')

#스마트스토어 로그인
driver.get(smartstorelogin_url)
driver.find_element_by_name('id').send_keys(smartstore_id)
driver.find_element_by_name('pw').send_keys(smartstore_pw)
driver.find_element_by_id('log.login').click()

#스마트스토어 배송준비 접속
driver.get(smartstoredelevery_url)
wait = WebDriverWait(driver, 10)
element = wait.until(EC.element_to_be_clickable((By.TAG_NAME, 'iframe')))

# iframes = driver.find_elements_by_tag_name('iframe')
# print('현재 페이지에 iframe은 %d개가 있습니다.' % len(iframes))

driver.switch_to.frame('__naverpay')    #iframe으로 갖힌 xpath를 읽기위해서 프레임 변경
orderNo = driver.find_elements_by_xpath('//*[@data-column-name="orderNo"]/div')[1:]
orderMemberName = driver.find_elements_by_xpath('//*[@data-column-name="orderMemberName"]/div')
receiverName = driver.find_elements_by_xpath('//*[@data-column-name="receiverName"]/div')
print(orderNo[0].text)
print(orderMemberName[0].text)
print(receiverName[0].text)

# print(driver.find_element_by_xpath('//*[@data-column-name="orderMemberName"]/div/text()').extract_first())


