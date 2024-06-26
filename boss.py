import time

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy as aby

from button_location import home_search_button, job_search_button, order_button, order_button_latest, \
    order_button_close, share_button, share_button_link, back_button, first_card
from config import boss_appPackage, appium_server_url, capabilities, boss_appActivity, job_key
from tool.adb_event import stop_app, open_app, tap, center_scroll, image_match
from tool.appium_event import wait_for_element


class CrawlProcess():
    def __init__(self):
        stop_app(boss_appPackage)
        self.driver = webdriver.Remote(
            appium_server_url,
            options=UiAutomator2Options().load_capabilities(capabilities)
        )
        open_app(boss_appPackage, boss_appActivity)

    def __del__(self):
        try:
            self.driver.quit()
        except:
            pass

    def switch_to_search(self):
        wait_for_element(
            driver=self.driver,
            locator=aby.XPATH,
            value='//android.widget.FrameLayout[@resource-id="com.hpbr.bosszhipin:id/iv_head_bg"]'
        )

        time.sleep(0.25)
        tap(home_search_button[0], home_search_button[1])

        wait_for_element(
            driver=self.driver,
            locator=aby.XPATH,
            value='//android.widget.TextView[@resource-id="com.hpbr.bosszhipin:id/tv_title" and @text="搜索发现"]'
        )

    def choose_condition(self):
        try:
            # 关闭消息窗口
            self.driver.find_element(
                by=aby.XPATH,
                value='//android.widget.ImageView[@resource-id="com.hpbr.bosszhipin:id/iv_delete"]'
            ).click()
        except:
            pass

        element = self.driver.find_element(
            by=aby.XPATH,
            value='//android.widget.EditText[@resource-id="com.hpbr.bosszhipin:id/et_search"]'
        )
        element.send_keys(job_key)
        tap(job_search_button[0], job_search_button[1])

        wait_for_element(
            driver=self.driver,
            locator=aby.XPATH,
            value='//android.widget.TextView[@resource-id="com.hpbr.bosszhipin:id/tv_tab_label" and @text="综合排序"]'
        )
        tap(order_button[0], order_button[1])
        wait_for_element(
            driver=self.driver,
            locator=aby.XPATH,
            value='//android.widget.TextView[@resource-id="com.hpbr.bosszhipin:id/tv_title"]'
        )
        tap(order_button_latest[0], order_button_latest[1])
        tap(order_button_close[0], order_button_close[1])
        time.sleep(2)

    def content_crawl(self):
        wait_for_element(
            driver=self.driver,
            locator=aby.XPATH,
            value='//android.widget.TextView[@resource-id="com.hpbr.bosszhipin:id/tv_job_name"]'
        )

        tap(share_button[0], share_button[1])
        time.sleep(0.25)
        tap(share_button_link[0], share_button_link[1])
        time.sleep(0.25)
        job_link = self.driver.get_clipboard_text()

        # 职位
        job_name_element = self.driver.find_element(
            by=aby.XPATH,
            value='//android.widget.TextView[@resource-id="com.hpbr.bosszhipin:id/tv_job_name"]'
        )
        job_name = job_name_element.text

        # 薪资
        job_salary_element = self.driver.find_element(
            by=aby.XPATH,
            value='//android.widget.TextView[@resource-id="com.hpbr.bosszhipin:id/tv_job_salary"]'
        )
        job_salary = job_salary_element.text

        # 地区
        job_area = ''
        try:
            job_are_element = self.driver.find_element(
                by=aby.XPATH,
                value='//android.widget.TextView[@resource-id="com.hpbr.bosszhipin:id/tv_required_location"]'
            )
            job_area = job_are_element.text
        except:
            pass

        # 经验
        job_exp = ''
        try:
            job_exp_element = self.driver.find_element(
                by=aby.XPATH,
                value='//android.widget.TextView[@resource-id="com.hpbr.bosszhipin:id/tv_required_work_exp"]'
            )
            job_exp = job_exp_element.text
        except:
            pass

        # 学历
        job_degree = ''
        try:
            job_degree_element = self.driver.find_element(
                by=aby.XPATH,
                value='//android.widget.TextView[@resource-id="com.hpbr.bosszhipin:id/tv_required_degree"]'
            )
            job_degree = job_degree_element.text
        except:
            pass

        job_require = f'{job_exp}/{job_degree}'

        # 工作相关标签
        job_tags = ''
        try:
            job_tags_parent_elements = self.driver.find_element(
                by=aby.XPATH,
                value='//android.view.ViewGroup[@resource-id="com.hpbr.bosszhipin:id/fl_content_above"]'
            )
            job_tags_elements = job_tags_parent_elements.find_elements(by=aby.XPATH, value='//*')

            for each in job_tags_elements: job_tags = f'{job_tags}/{each.text}'
        except:
            pass

        # 附加地区
        try:
            job_are_map_element = self.driver.find_element(
                by=aby.XPATH,
                value='//android.widget.TextView[@resource-id="com.hpbr.bosszhipin:id/tv_location"]'
            )
            job_area = f'{job_area}/{job_are_map_element.text}'
        except:
            pass

        center_scroll(y=5)

        # 工作公司
        job_company = ''
        try:
            job_company_element = self.driver.find_element(
                by=aby.XPATH,
                value='//android.widget.TextView[@resource-id="com.hpbr.bosszhipin:id/tv_com_name"]'
            )
            job_company = job_company_element.text
        except: pass

        # 工作公司标签
        job_company_tags = ''
        try:
            job_company_tags_element = self.driver.find_element(
                by=aby.XPATH,
                value='//android.widget.TextView[@resource-id="com.hpbr.bosszhipin:id/tv_com_info"]'
            )
            job_company_tags = job_company_tags_element.text

            job_tags_extent_parent_element = self.driver.find_element(
                by=aby.XPATH,
                value='//android.view.ViewGroup[@resource-id="com.hpbr.bosszhipin:id/fl_company_tag"]'
            )
            job_tags_extent_elements = job_tags_extent_parent_element.find_elements(
                by=aby.XPATH,
                value='//android.widget.TextView[contains(@resource-id,"com.hpbr.bosszhipin:id/tv_label")]'
            )
            for each in job_tags_extent_elements:
                job_company_tags = f'{job_company_tags}/{each.text}'
        except: pass

        # 工作详情
        job_content = ''
        try:
            more_button_location = image_match('./more.png')
            if -1 != more_button_location[1] and -1 != more_button_location[1]:
                tap(more_button_location[0], more_button_location[1])

            job_content_element = self.driver.find_element(
                by=aby.XPATH,
                value='//android.widget.TextView[@resource-id="com.hpbr.bosszhipin:id/tv_description"]'
            )
            job_content = job_content_element.text
        except: pass

        # 防止滑动过度没有工作公司信息
        if '' == job_company:
            try:
                center_scroll(y=5)
                job_company_element = self.driver.find_element(
                    by=aby.XPATH,
                    value='//android.widget.TextView[@resource-id="com.hpbr.bosszhipin:id/tv_com_name"]'
                )
                job_company = job_company_element.text
            except: pass

        # 防止滑动过度没有工作公司标签
        if '' == job_company_tags:
            try:
                job_company_tags_element = self.driver.find_element(
                    by=aby.XPATH,
                    value='//android.widget.TextView[@resource-id="com.hpbr.bosszhipin:id/tv_com_info"]'
                )
                job_company_tags = job_company_tags_element.text

                job_tags_extent_parent_element = self.driver.find_element(
                    by=aby.XPATH,
                    value='//android.view.ViewGroup[@resource-id="com.hpbr.bosszhipin:id/fl_company_tag"]'
                )
                job_tags_extent_elements = job_tags_extent_parent_element.find_elements(
                    by=aby.XPATH,
                    value='//android.widget.TextView[contains(@resource-id,"com.hpbr.bosszhipin:id/tv_label")]'
                )

                for each in job_tags_extent_elements: job_company_tags = f'{job_company_tags}/{each.text}'
            except: pass

        print(f'job_name:{job_name},job_salary:{job_salary},\
            job_require:{job_require},job_area:{job_area},\
            job_content:\n{job_content}\n,job_company:{job_company},\
            job_company_tags:{job_company_tags},\njob_link:{job_link}'
        )
        tap(back_button[0], back_button[1])
        time.sleep(0.25)