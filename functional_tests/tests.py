from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
import unittest
from django.test import LiveServerTestCase
from selenium.common.exceptions import WebDriverException

MAX_WAIT = 10

# unittest.TestCase
class NewVisitorTest(LiveServerTestCase):

    def setUp(self):

        self.browser = webdriver.Chrome()

    def tearDown(self):

        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        # table = self.browser.find_element(By.ID, 'id_list_table')
        # rows = table.find_elements(By.TAG_NAME, 'tr')
        # self.assertIn(row_text, [row.text for row in rows])
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element(By.ID,'id_list_table')
                rows = table.find_elements(By.TAG_NAME,'tr')
                self.assertIn(row_text,[row.text for row in rows])
                return
            except (AssertionError,WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)


    def test_can_start_a_list_and_retrieve_it_later(self):

        # 用户张三听说有一个在线待办事项应用，他打开了该应用的首页
        # self.browser.get('http://localhost:8000')
        self.browser.get(self.live_server_url)

        # 用户注意到网页的标题和头部都包含 "To-Do" 这个词
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('To-Do', header_text)

        # 应用有一个输入待办事项的文本输入框，用户注意到它的提示信息为 "Enter a to-do item"
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # 用户在文本输入框中输入了 "Buy flowers"
        inputbox.send_keys('Buy flowers')

        # 用户按下回车键后，页面更新了，待办事项表格中显示了 "1: Buy flowers"
        inputbox.send_keys(Keys.ENTER)
        # time.sleep(1)
        # self.check_for_row_in_list_table('1: Buy flowers')
        self.wait_for_row_in_list_table('1: Buy flowers')

        # 页面中又显示了一个文本输入框，可以输入其他待办事项
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Give a gift to Lisi')
        inputbox.send_keys(Keys.ENTER)
        # time.sleep(1)

        # 页面再次更新，清单中显示了这两个待办事项
        # self.check_for_row_in_list_table('1: Buy flowers')
        # self.check_for_row_in_list_table('2: Give a gift to Lisi')
        self.wait_for_row_in_list_table('1: Buy flowers')
        self.wait_for_row_in_list_table('2: Give a gift to Lisi')

        # 用户看到网站为她生成了一个唯一的URL

    def test_mutiple_userss_can_start_lists_at_different_urls(self):
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element(By.ID,'id_new_item')
        inputbox.send_keys('Buy flowers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy flowers')

        zhangsan_list_url = self.browser.current_url
        self.assertRegex(zhangsan_list_url,'/lists/.+')

        self.browser.quit()
        self.browser = webdriver.Chrome()

        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertNotIn('Buy flowers',page_text)
        self.assertNotIn('BGive a gift to Lisi',page_text)

        inputbox = self.browser.find_element(By.ID,'id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        wangwu_list_url = self.browser.current_url
        self.assertRegex(wangwu_list_url,'/lists/.+')
        self.assertNotEqual(wangwu_list_url,zhangsan_list_url)

        page_text = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertNotIn('Buy flowers',page_text)
        self.assertIn('Buy milk',page_text)

    def test_layout_and_styling(self):
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )

        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1:testing')
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )



# if __name__=='__main__':
#     unittest.main()
