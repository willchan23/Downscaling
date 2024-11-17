import time
from time import sleep
import os
import requests
import subprocess
# 从selenium导入webdriver
from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import platform
from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException, UnexpectedAlertPresentException, \
    WebDriverException, TimeoutException
import traceback, sys
import argparse
import yaml
import ddddocr
from datetime import datetime, timedelta


def yw_check(driver, res=None):  # ocr识别验证码并登录

    driver.find_element(By.ID, 'yw0_button').click()
    time.sleep(0.5)
    img = driver.find_element(By.ID, 'yw0')
    ocr = ddddocr.DdddOcr()
    if res is None:
        res = ocr.classification(img.screenshot_as_png)
    text_box = driver.find_element(By.NAME, 'verifyCode')
    text_box.clear()
    text_box.send_keys(res)


def put_in_cart(s, e):
    start_date = driver.find_element(By.ID, "dateS")
    end_date = driver.find_element(By.ID, "dateE")
    start_date.clear()
    end_date.clear()
    start_date.send_keys(s.strftime('%Y-%m-%d %H'))
    end_date.send_keys(e.strftime('%Y-%m-%d %H'))

    while True:
        for i in range(1, len(driver.window_handles)):
            try:
                driver.switch_to.window(driver.window_handles[-1])  # 切换到最新的窗口句柄
                if driver.current_window_handle != driver.window_handles[0]:
                    driver.close()
            except Exception:
                pass
        driver.switch_to.window(driver.window_handles[0])
        driver.switch_to.window(driver.window_handles[0])
        yw_check(driver)
        driver.find_element(By.ID, 'submit').click()
        try:
            driver.switch_to.window(driver.window_handles[-1])
        except WebDriverException:
            pass
        else:
            try:  # 处理弹出的警告框，应该是验证码错误呢
                time.sleep(3)

                # try:
                driver.switch_to.alert.accept()  # 接收后自动又跳转到返回页面

                # except NoAlertPresentException:
                #     driver.close()
                #     driver.switch_to.window(driver.window_handles[0])
                time.sleep(3)
                driver.switch_to.window(driver.window_handles[0])
                driver.find_element(By.ID, 'yw0_button').click()  # 换一个验证码，然后继续循环
            except NoAlertPresentException:
                # while driver.find_element(By.XPATH,r"/html/body/div[6]/form/div[2]/div/div[3]/table/tbody/tr[1]/th[1]/input").is_enabled()==0:
                #     driver.refresh()
                try:
                    fd_button = driver.find_element(By.XPATH,
                                                    r"/html/body/div[6]/form/div[2]/div/div[3]/table/tbody/tr[1]/th[1]/input")
                except NoSuchElementException:
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    put_in_cart(s, e)
                    return
                else:
                    if fd_button is not None:
                        break

    # next_button = driver.find_element(By.XPATH,r'/html/body/div[6]/form/div[2]/div/div[4]/ul/li[10]/a')
    try:
        # while driver.find_element(By.XPATH,r'/html/body/div[6]/form/div[2]/div/div[4]/ul/li[10]/a').is_enabled():#判断下一页是否能选中
        while True:
            print('able1')
            time.sleep(2)

            driver.find_element(By.XPATH,
                                r"/html/body/div[6]/form/div[2]/div/div[3]/table/tbody/tr[1]/th[1]/input").click()  # 全选
            driver.find_element(By.XPATH,
                                r"/html/body/div[6]/form/div[2]/div/div[5]/input").click()  # 加入我的数据框
            time.sleep(2)
            # if driver.switch_to.alert.
            try:
                driver.switch_to.alert.accept()  # 针对于当打开弹框中有两个按钮,弹框确定
                time.sleep(2)
                driver.find_element(By.XPATH, r'/html/body/div[6]/form/div[2]/div/div[4]/ul/li[6]/a').click()
                time.sleep(3)
            except NoAlertPresentException:
                pass
            else:
                try:
                    time.sleep(2)
                    while driver.find_element(By.XPATH,
                                              r'/html/body/div[1]/div[1]/div/div[2]/div/div/div/div/span').is_enabled():
                        print('this is a Sliding verification')
                        slider = driver.find_element(By.XPATH,
                                                     r'/html/body/div[1]/div[1]/div/div[2]/div/div/div/div/span')
                        # 创建操作链
                        action_chains = ActionChains(driver)
                        # 将鼠标移动到滑块上
                        action_chains.move_to_element(slider)
                        # 模拟按下鼠标左键并保持不松开
                        action_chains.click_and_hold()
                        # 移动鼠标使滑块达到目标位置
                        action_chains.move_by_offset(300, 0)
                        # 松开鼠标左键
                        action_chains.release()
                        # 执行操作链
                        action_chains.perform()
                        time.sleep(3)
                        # driver.
                except NoSuchElementException:
                    pass
    except NoSuchElementException:
        pass
    driver.close()
    driver.switch_to.window(driver.window_handles[0])


if __name__ == '__main__':

    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--user-agent=Mozilla/5.0 HAHA')
    options.add_experimental_option("detach", True)
    ############
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_argument("--disable-blink-features=AutomationControlled")
    ############
    options.set_capability('pageLoadStrategy', 'none')
    options.set_capability("unhandledPromptBehavior", "accept")
    # options.add_argument('--headless')  # 浏览器隐式启动
    url = "https://data.cma.cn/dataService/cdcindex/datacode/NAFP_CLDAS2.0_RT.html"
    # driver_path = os.path.expanduser("~/chrome/chromedriver.exe")
    driver_path = None
    print('driver is going to init!')
    driver = webdriver.Chrome(service=Service(driver_path) if driver_path else None, options=options)
    # driver = webdriver.Edge()
    driver.implicitly_wait(3)
    driver.set_page_load_timeout(5)
    print('driver is inited!')
    driver.get(url)
    # login
    time.sleep(2)
    driver.find_element(By.ID, 'toLoginPage').click()
    time.sleep(2)
    loginpage = driver.find_element(By.ID, 'loginWeb-page')
    driver.execute_script("arguments[0].click();", loginpage)
    # driver.find_element(By.XPATH, r'/html/body/div[5]/div/div/div/div[2]/div[1]/div[3]').click()
    driver.find_element(By.ID, 'userName-page').send_keys('769944031@qq.com')
    driver.find_element(By.ID, 'password-page').send_keys('Ecnugeo369')
    while True:
        yw_check(driver)  # 验证码输入
        time.sleep(2)

        login = driver.find_element(By.ID, 'loginPage-page')  # 登录
        driver.execute_script("arguments[0].click();", login)
        try:
            time.sleep(1)
            driver.switch_to.alert.accept()
            driver.find_element(By.ID, 'yw0_button').click()
        except NoAlertPresentException:
            break

    now_date = datetime(year=2023, month=8, day=1, hour=0)
    end_date = datetime(year=2024, month=1, day=1, hour=0)
    ### GST
    # 11/11 from 2023/1/1/0 - 2023/8/1/0
    # 11/14 from 2023/8/1/0 - 2023/12/1/0
    # input_xpath[0]是选择时间分辨率为1h，input_xpath[1]是选择空间范围为所有范围
    input_xpath = [
        r"/html/body/div[@class='content']/div[@id='sub-body-contentDiv']/div[@class='search-center']/form[@id='queryForm']/div[@class='search-center-left search-center-129']/div[@class='element-choosetwo clearfix'][1]/div[@class='search-center-left-cont clearfix']/div[@class='choosetwo-cont clearfix']/div[1]/input[@id='selectone1']",
        r"/html/body/div[@class='content']/div[@id='sub-body-contentDiv']/div[@class='search-center']/form[@id='queryForm']/div[@class='search-center-left search-center-129']/div[@class='site-choose clearfix ']/h4[@class='title']/div[@class='searchTSTiFuItAl']/div[@id='ALLSelCl']"]
    # metrics_xpath是确定需要的数据参数
    metrics_xpath = [
        r"/html/body/div[@class='content']/div[@id='sub-body-contentDiv']/div[@class='search-center']/form[@id='queryForm']/div[@class='search-center-left search-center-129']/div[@class='element-choosetwo clearfix'][2]/div[@class='search-center-left-cont clearfix']/div[@class='choosetwo-cont clearfix']/div[" + str(
            i) + r"]/input[@id='selectone1']"
        for i in [12]]  ## 地表温度GST ground_surface_temperature

    # for i in [1,2,3,4,5,6]]
    # for i in [1, 2, 3, 4, 5, 6, 7, 8, 12, 13, 14] ,[1,2,3,4,5,6,12]
    for xpath in input_xpath + metrics_xpath:
        driver.find_element(By.XPATH, xpath).click()

    while now_date < end_date:
        e = now_date + timedelta(days=2)
        if e > end_date:
            e = end_date
        print(now_date.strftime('%Y-%m-%d %H') + ' to ' + e.strftime('%Y-%m-%d %H'))
        put_in_cart(now_date, e)
        date_delay = timedelta(days=2)
        now_date += date_delay

    driver.close()
