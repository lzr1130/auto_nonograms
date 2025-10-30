import time
import json
import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

from solver import solve_nonogram, print_grid

SIZE = 20  # 支持 5, 10, 15, 20, 25
RANDOM_WAIT = True
LOGIN = False
SLEEP_MIN = 0.2
SLEEP_MAX = 0.3

ITERATE = 12

# 目标 URL
url = "https://cn.puzzle-nonograms.com/"
driver = webdriver.Chrome()
cookie_to_add = json.load(open('cookie.json', 'r'))

print(f"打开网页: {url}")

driver.get(url)

if LOGIN:
    # 登录状态下打开网页
    sleep(2)
    print("添加 cookie 并刷新页面")
    driver.add_cookie(cookie_to_add)
    driver.get(url)

wait = WebDriverWait(driver, 10)

# 点击 15*15 挑战
print(f"点击 {SIZE}*{SIZE}")
if SIZE == 5:
    element_to_click = wait.until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[1]/ul/li[1]/a'))
    )
    element_to_click.click()
elif SIZE == 10:
    element_to_click = wait.until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[1]/ul/li[2]/a'))
    )
    element_to_click.click()
elif SIZE == 15:
    element_to_click = wait.until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[1]/ul/li[3]/a'))
    )
    element_to_click.click()
elif SIZE == 20:
    element_to_click = wait.until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[1]/ul/li[4]/a'))
    )
    element_to_click.click()
elif SIZE == 25:
    element_to_click = wait.until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[1]/ul/li[5]/a'))
    )
    element_to_click.click()
else:
    raise ValueError("只支持 5, 10, 15, 20, 25 大小的 Nonogram")


for i in range(ITERATE):

    # 点击新题目
    print("点击新题目")
    element_to_click = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="btnNew"]'))
    )
    element_to_click.click()

    # 读取题目要求
    print("读取题目要求")
    start = time.time()
    colomns = []
    for i in range(1, SIZE + 1):
        colomn = []
        for j in range(1, 8):
            try:
                element = driver.find_element(By.XPATH, f'/html/body/div[2]/div[3]/div[2]/form/div[3]/div[1]/div/table/tbody/tr/td/div/div/div[1]/div/div[1]/div[{i}]/div[{j}]')
                if element.text != '':
                    colomn.append(int(element.text))
            except:
                break
        colomns.append(colomn)
    rows = []
    for i in range(1, SIZE + 1):
        row = []
        for j in range(1, 8):
            try:
                element = driver.find_element(By.XPATH, f'/html/body/div[2]/div[3]/div[2]/form/div[3]/div[1]/div/table/tbody/tr/td/div/div/div[1]/div/div[2]/div[{i}]/div[{j}]')
                if element.text != '':
                    row.append(int(element.text))
            except:
                break
        rows.append(row)
    end = time.time()
    print(f"读取完成，耗时 {end - start:.5f} 秒")
    print("列要求:", colomns)
    print("行要求:", rows)

    # 求解
    print("开始求解")
    start = time.time()
    solution = solve_nonogram(rows, colomns)
    end = time.time()
    print(f"求解完成，耗时 {end - start:.5f} 秒")
    for row in solution:
        print(row)
    # print_grid(solution)

    # 填写答案
    if RANDOM_WAIT:
        print(f"开始填写答案(随机等待{SLEEP_MIN}-{SLEEP_MAX}s防止操作过快)")
    else:
        print(f"开始填写答案(极速冲刺)")
    for r in range(SIZE):
        for c in range(SIZE):
            if solution[r][c] == 1:
                element_to_click = driver.find_element(By.XPATH, f'/html/body/div[2]/div[3]/div[2]/form/div[3]/div[1]/div/table/tbody/tr/td/div/div/div[1]/div/div[3]/div[{r+1}]/div[{c+1}]')
                element_to_click.click()
                if RANDOM_WAIT:
                    time.sleep(random.uniform(SLEEP_MIN, SLEEP_MAX))
    print("填写完成")
    sleep(2)
sleep(100)
driver.quit()
