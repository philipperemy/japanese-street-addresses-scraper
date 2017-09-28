from time import sleep

import numpy as np
from selenium import webdriver

driver = webdriver.Chrome('/usr/local/bin/chromedriver')

driver.get('https://www.google.fr/maps')

search_box_input = driver.find_element_by_id('searchboxinput')

search_box_input.send_keys('Tokyo 東京')

driver.find_element_by_id('searchbox-searchbutton').click()

# for i in range(6):
#     driver.find_element_by_id('widget-zoom-in').click()
#     print('zoomed once.')
#     sleep(5)

# search_box_input.submit()

print(driver.current_url)

sleep(5)

# https://stackoverflow.com/questions/27948420/click-at-at-an-arbitrary-position-in-web-browser-with-selenium-2-python-binding
# driver.execute_script("return window.innerWidth")
# driver.execute_script("return window.innerHeight")
# https://developer.mozilla.org/en-US/docs/Web/API/Document/width
# document.body.clientHeight
#

# driver.execute_script("el = document.querySelector('div > h1');var boundaries = el.getBoundingClientRect(); return [boundaries.top, boundaries.right, boundaries.bottom, boundaries.left]")
while True:
    a, b = np.random.randint(low=0, high=807, size=2)

    homeLink = driver.find_element_by_css_selector('canvas')

    from selenium.webdriver.common.action_chains import ActionChains

    action = ActionChains(driver)
    action.move_to_element_with_offset(homeLink, 400, 400)  # move 150 pixels to the right to access Help link
    action.click()
    action.perform()

    # driver.execute_script('el = document.elementFromPoint({}, {}); el.click();'.format(a, b))
    sleep(0.5)
    print('click')
