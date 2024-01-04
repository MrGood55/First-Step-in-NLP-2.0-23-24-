from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import csv

url = "https://www.rbc.ru/life/tag/health"

# Опции для работы в тихом режиме (без открытия окна браузера)
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

driver = webdriver.Chrome(options=chrome_options)
driver.get(url)

# Подождем несколько секунд, чтобы страница полностью загрузилась
time.sleep(1)

# Определяем количество раз, которое нужно прокрутить вниз
num_iterations = 4  # Например, три раза, чтобы получить 80 новостей (если каждый раз подгружаются 20)

unique_titles = set()

for i in range(num_iterations):
    try:
        # Прокручиваем вниз
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)  # Подождем 1 секунду

        # Ищем все элементы с классом 'info-block-title'
        titles = driver.find_elements(By.CLASS_NAME, 'info-block-title')
        
        # Добавляем уникальные заголовки в множество
        unique_titles.update(title.text for title in titles)

        print(f"Iteration {i + 1}: {len(unique_titles)} unique titles collected")
    except Exception as E:
        print(f"Iteration {i + 1} is collapsed \nError is {E}")
        time.sleep(1)

# Закрываем браузер после использования
driver.quit()

print(f"Total unique titles collected: {len(unique_titles)}")

# Записываем уникальные заголовки в файл CSV
csv_filename = "titles_health_rbc_unique.csv"
with open(csv_filename, mode='w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Title'])
    for title in unique_titles:
        writer.writerow([title])

print(f"Unique titles have been successfully written to {csv_filename}.")
