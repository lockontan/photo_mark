import time
import os
from selenium import webdriver

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def sendMail(outbox, inboxList, workpath, zipName):
    # 发件邮箱
    qqnumber = outbox.replace('@qq.com', '')

    option = webdriver.ChromeOptions()

    # 静默模式
    # option.add_argument('headless')

    # 打开chrome浏览器
    chromedriverPath = os.path.join(os.getcwd(), 'chromedriver.exe')
    driver = webdriver.Chrome(chrome_options=option, executable_path=chromedriverPath)

    driver.get('https://mail.qq.com/')

    # driver.set_page_load_timeout(5)
    # try:
    #     driver.get('https://mail.qq.com/')
    # except:
    #     driver.execute_script("window.stop()")

    #最大化谷歌浏览器
    # driver.maximize_window()

    # 登录邮箱
    wait = WebDriverWait(driver, 10)
    wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"//iframe[@id='login_frame']")))
    wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@uin=" + qqnumber +"]"))).click()

    # 点击写信
    WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, "//a[@id='composebtn']"))).click()
    wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"//iframe[@id='mainFrame']")))
    
    for q in inboxList:
        # 收件邮箱
        reMail = q
        # 附件地址
        filePath = os.path.join(os.path.dirname(workpath), q.replace('@qq.com', ''), zipName + '.zip')

        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@aria-label='收件人']"))).send_keys(reMail)
            wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='compose_toolbtn qmEditorAttachBig']"))).click()

            # 返回父iframe
            time.sleep(1)
            driver.switch_to.default_content()

            # 附件上传 iframe
            wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'ftnupload_attach_QMDialog__dlgiframe_')))
            wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='UploadFile']"))).send_keys(filePath)
            WebDriverWait(driver, 6000).until(EC.element_to_be_clickable((By.XPATH, "//span[@class='right icon_att icon_att_finish ctrl_finish']")))
            # 点击确认
            driver.find_element_by_xpath('//a[@ck="confirm"]').click()

            # 返回mainFrame
            time.sleep(1)
            driver.switch_to.frame('mainFrame')
            # 发送邮件
            wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@name='sendbtn']"))).click()
            
            # 判断结果
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="address_0"]'))).text == reMail
            
            print('！！！！！！' + reMail + '发送成功！！！！！！')            
            
            if reMail != inboxList[len(inboxList) - 1]:
                driver.find_elements_by_id('btnagainl')[0].click()

        except Exception as result:
            print('！！！！！！' + reMail +'发送失败！！！！！！')

# sendMail('276104371@qq.com', ['2998011437@qq.com', '863246160@qq.com'], 'E:\hane\py', '玩.zip')