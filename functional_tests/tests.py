from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):

        self.browser = webdriver.Chrome()

    def tearDown(self):

        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element(By.ID, 'id_list_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):

        # 用户张三听说有一个在线待办事项应用，他打开了该应用的首页
        self.browser.get('http://localhost:8000')

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
        time.sleep(1)
        self.check_for_row_in_list_table('1: Buy flowers')

        # 页面中又显示了一个文本输入框，可以输入其他待办事项
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Give a gift to Lisi')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # 页面再次更新，清单中显示了这两个待办事项
        self.assertIn('1: Buy flowers')
        self.assertIn('2: Give a gift to Lisi')

        # 用户看到网站为她生成了一个唯一的URL

        self.fail('Finish the test!')



if __name__=='__main__':
    unittest.main()
