import time
import numpy as np
import pickle
from selenium.webdriver import Firefox, ActionChains

driver = Firefox(executable_path='WebDriver/geckodriver')
driver.get('http://www.douban.com/')
time.sleep(6)
driver.switch_to.frame(0)
driver.find_element_by_class_name('account-tab-account').click()
time.sleep(3)
driver.find_element_by_id('username').send_keys('username')
driver.find_element_by_id('password').send_keys('password')
driver.find_element_by_class_name('account-form-field-submit').click()
time.sleep(6)
driver.switch_to.default_content()
driver.switch_to.frame(0)
driver.switch_to.frame('tcaptcha_iframe')
imgBack = driver.find_element_by_id('cdn1').get_attribute("src")
imgJigsaw = driver.find_element_by_id('cdn2').get_attribute('src')
button = driver.find_element_by_id('tcaptcha_drag_button')
reload = driver.find_element_by_id('reload')

# drag the button for Jigsaw puzzle
# the speed of drag should be identify by jquery.easing ->
# reference: https://www.aneasystone.com/archives/2018/03/python-selenium-geetest-crack.html
def ease_out_expo(x):
    if x == 1:
        return 1
    else:
        return 1 - pow(2, -10 * x)

def get_tracks(distance, seconds, ease_func):
    tracks = [0]
    offsets = [0]
    for t in np.arange(0.0, seconds, 0.1):
        ease = globals()[ease_func]
        offset = round(ease(t / seconds) * distance)
        tracks.append(offset - offsets[-1])
        offsets.append(offset)
    return offsets, tracks

def drag_and_drop(browser, button, offset):
    offsets, tracks = get_tracks(offset, 6, 'ease_out_expo')
    ActionChains(browser).click_and_hold(button).perform()
    for x in tracks:
        ActionChains(browser).move_by_offset(x, 0).perform()
    ActionChains(browser).pause(0.5).release().perform()

drag_and_drop(driver, button, 170)  # for this case, the distance could be 170, or you may drag by hand

# save the cookie for next using
pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))
