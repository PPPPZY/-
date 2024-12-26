import csv
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 打开edge浏览器
driver = webdriver.Edge()
# 打开知网
driver.get('https://www.cnki.net/')
key = "6G"
# 传入关键字
WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '''//*[@id="txt_SearchText"]'''))).send_keys(
    key)
# 点击搜索
WebDriverWait(driver, 100).until(
    EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/div[1]/input[2]'))).click()
time.sleep(3)
# 点击切换中文文献
WebDriverWait(driver, 100).until(
    EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/div[2]/div/div/div/div/a[1]'))).click()
time.sleep(2)

# 点击博士论文
# WebDriverWait(driver, 100).until(
#     EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[1]/div/ul[1]/li[2]/a'))).click()
# time.sleep(2)


# 解析页详细信息
def parsePageDetail(webElement_list, key):
    for element in webElement_list:
        try:
            # 点击条目
            element.click()
            # 获取driver的句柄
            handles = driver.window_handles
            # driver切换至最新生产的页面
            driver.switch_to.window(handles[-1])
            # 标题
            title = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, '//div[@class="wx-tit"]/h1'))).text

            print('标题：', title)
            # 摘要
            abstract = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'abstract-text'))).text
            # print('摘要：', abstract)
            # 关键词
            keywords = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'keywords'))).text
            # print('关键词：', keywords)
            savePageResult(title, abstract, keywords, key)
        except:
            print('解析失败！')
            continue
        finally:
            # 如果有多个窗口，关闭第二个窗口， 切换回主页
            n2 = driver.window_handles
            if len(n2) > 1:
                driver.close()
                driver.switch_to.window(n2[0])


# 保存解析结果
def savePageResult(title, abstract, keywords, key):
    filemane = key + ".csv"
    with open(filemane, 'a', newline='', encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerow([title, abstract, keywords])


if __name__ == '__main__':
    # 总页数
    totalPage = 5
    # 开始时间
    startTime = datetime.now().minute
    # 循环解析每一页
    for curPage in range(1, totalPage + 1):
        # 等待加载完全，休眠3S
        time.sleep(3)
        webElement_list = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "fz14")))
        parsePageDetail(webElement_list, key)
        endTime = datetime.now().minute
        print(f'耗时{endTime - startTime}分钟')
        # 切换到下一页
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="PageNext"]'))).click()
