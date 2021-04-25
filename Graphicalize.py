import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("SSAutomation.ui")[0]
form_PSSW = uic.loadUiType("PickSellerSite.ui")[0]
form_PO = uic.loadUiType("PickOrder.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :
    orderNo = None
    orderMemberName = None
    receiverName = None

    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        #버튼에 기능연결
        self.FFCAutomationButton.clicked.connect(self.FFCAutomationButtonFunction)

    def FFCAutomationButtonFunction(self) :


        #PickSellerSiteWindow에 선택값이 도출될 때까지 다음 단계로 진행되지 않도록 EventLoop 사용
        pssw = PickSellerSiteWindow(self)
        pssw.exec_()    #모달형식으로 구현. 해당 다이얼로그가 끝나야 다음 코드 실행시작


class PickSellerSiteWindow(QDialog, form_PSSW) :
    def __init__(self, parent):
        super(PickSellerSiteWindow, self).__init__(parent)
        self.setupUi(self)
        self.setSiteCombobox()
        self.setOrderCombobox()

        self.OKButton.clicked.connect(self.OKButtonFunction)

        self.site = None
        self.orderno = None

    # 사이트콤보박스에 사이트목록 넣기
    def setSiteCombobox(self):
        self.Combo_Sites.addItem('adorama')
        self.Combo_Sites.addItem('amazon')
        self.Combo_Sites.addItem('ebay')
        self.Combo_Sites.addItem('newegg')

    # 주문콤보박스에 주문목록 넣기
    def setOrderCombobox(self):
        # 오더 콤보박스에 오더목록 넣기위해 스크래핑
        smartstorelogin_url = 'https://nid.naver.com/nidlogin.login?url=https%3A%2F%2Fsell.smartstore.naver.com%2F%23%2FnaverLoginCallback%3Furl%3Dhttps%253A%252F%252Fsell.smartstore.naver.com%252F%2523'
        smartstoredelevery_url = 'https://sell.smartstore.naver.com/#/naverpay/sale/delivery?summaryInfoType=DELIVERY_READY'
        smartstore_id = 'hdh5454'
        smartstore_pw = 'whdmsehgud8*'

        driver = webdriver.Chrome('chromedriver')

        # 스마트스토어 로그인
        driver.get(smartstorelogin_url)
        driver.find_element_by_name('id').send_keys(smartstore_id)
        driver.find_element_by_name('pw').send_keys(smartstore_pw)
        driver.find_element_by_id('log.login').click()

        # 스마트스토어 배송준비 접속
        driver.get(smartstoredelevery_url)
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.element_to_be_clickable((By.TAG_NAME, 'iframe')))

        driver.switch_to.frame('__naverpay')  # iframe으로 갖힌 xpath를 읽기위해서 프레임 변경
        orderNo = driver.find_elements_by_xpath('//*[@data-column-name="orderNo"]/div')[
                  1:]  # 주문번호 xpath도 도출되기 때문에 인덱스 0은 삭제함
        orderMemberName = driver.find_elements_by_xpath('//*[@data-column-name="orderMemberName"]/div')
        receiverName = driver.find_elements_by_xpath('//*[@data-column-name="receiverName"]/div')
        individualCustomUniqueCode = driver.find_elements_by_xpath('//*[@data-column-name="receiverName"]/div')

        for orderno, ordermemname in zip(orderNo, orderMemberName):
            self.Combo_Orders.addItem('주문번호 : ' + orderno.text + ' | 주문자명 : ' + ordermemname.text)

    def OKButtonFunction(self):
        self.site = self.Combo_Sites.currentText()
        self.orderno = self.Combo_Orders.currentText()
        #오더넘버말고 인덱스 받아서 인덱스로 관리하는게 편할듯
        #통관번호 매칭되는지 확인해야함

        ###############
        #여기서 배대지 다 입력하면 될듯
        ###############

        self.close()


if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass()

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()

