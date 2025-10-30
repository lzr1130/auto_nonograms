import time
import json
import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

from solver import solve_nonogram, print_grid

# Set the size of the Nonogram and other parameters
SIZE = 20  # Supported sizes: 5, 10, 15, 20, 25
RANDOM_WAIT = True  # Whether to use random wait times to simulate human behavior
LOGIN = False  # Whether login is required
SLEEP_MIN = 0.2  # Minimum random wait time
SLEEP_MAX = 0.3  # Maximum random wait time
ITERATE = 12  # Number of puzzles to solve

# Target URL
url = "https://www.puzzle-nonograms.com/"
driver = webdriver.Chrome()
cookie_to_add = json.load(open('cookie.json', 'r'))  # Load cookies from file

print(f"Opening webpage: {url}")
driver.get(url)

if LOGIN:
    # If login is required, add cookies and refresh the page
    sleep(2)
    print("Adding cookies and refreshing the page")
    driver.add_cookie(cookie_to_add)
    driver.get(url)

# Wait for the page to load
wait = WebDriverWait(driver, 10)

# Click the challenge button corresponding to the selected SIZE
print(f"Selecting {SIZE}*{SIZE}")
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
    raise ValueError("Only Nonogram sizes 5, 10, 15, 20, 25 are supported")

# Loop to solve puzzles
for i in range(ITERATE):

    # Click the "New Puzzle" button
    print("Clicking 'New Puzzle'")
    element_to_click = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="btnNew"]'))
    )
    element_to_click.click()

    # Read puzzle requirements
    print("Reading puzzle requirements")
    start = time.time()
    colomns = []  # Store column requirements
    for i in range(1, SIZE + 1):
        colomn = []
        for j in range(1, 8):  # Each column can have up to 7 numbers
            try:
                element = driver.find_element(By.XPATH, f'/html/body/div[2]/div[3]/div[2]/form/div[3]/div[1]/div/table/tbody/tr/td/div/div/div[1]/div/div[1]/div[{i}]/div[{j}]')
                if element.text != '':
                    colomn.append(int(element.text))
            except:
                break
        colomns.append(colomn)
    rows = []  # Store row requirements
    for i in range(1, SIZE + 1):
        row = []
        for j in range(1, 8):  # Each row can have up to 7 numbers
            try:
                element = driver.find_element(By.XPATH, f'/html/body/div[2]/div[3]/div[2]/form/div[3]/div[1]/div/table/tbody/tr/td/div/div/div[1]/div/div[2]/div[{i}]/div[{j}]')
                if element.text != '':
                    row.append(int(element.text))
            except:
                break
        rows.append(row)
    end = time.time()
    print(f"Requirements read, time taken: {end - start:.5f} seconds")
    print("Column requirements:", colomns)
    print("Row requirements:", rows)

    # Solve the Nonogram
    print("Solving the puzzle")
    start = time.time()
    solution = solve_nonogram(rows, colomns)  # Call the solver function
    end = time.time()
    print(f"Puzzle solved, time taken: {end - start:.5f} seconds")
    for row in solution:
        print(row)
    # print_grid(solution)

    # Fill in the solution
    if RANDOM_WAIT:
        print(f"Filling in the solution (random wait {SLEEP_MIN}-{SLEEP_MAX}s to avoid fast operations)")
    else:
        print(f"Filling in the solution (fast mode)")
    for r in range(SIZE):
        for c in range(SIZE):
            if solution[r][c] == 1:  # If the solution indicates a filled cell
                element_to_click = driver.find_element(By.XPATH, f'/html/body/div[2]/div[3]/div[2]/form/div[3]/div[1]/div/table/tbody/tr/td/div/div/div[1]/div/div[3]/div[{r+1}]/div[{c+1}]')
                element_to_click.click()
                if RANDOM_WAIT:
                    time.sleep(random.uniform(SLEEP_MIN, SLEEP_MAX))  # Random wait
    print("Solution filled")
    sleep(2)

# Wait for a while before closing the browser
sleep(100)
driver.quit()
