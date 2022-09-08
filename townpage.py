from selenium import webdriver
from time import sleep, time

# Firefox のオプションを設定する
# (現在Windows(WSL2)のdockerだとchromeが使えないです)
options = webdriver.FirefoxOptions()

# Selenium Server に接続する
driver = webdriver.Remote(
    command_executor='http://localhost:4444/wd/hub',
    options=options,
)

# Selenium 経由でブラウザを操作する
driver.get('https://www.optim.co.jp/')
print(driver.current_url)

# ブラウザを終了する
sleep(5)
driver.quit()
