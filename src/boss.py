from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy as aby

from config import boss_appPackage, appium_server_url, capabilities, boss_appActivity, job_key, order_require, \
    more_img_path, search_bar_bias
from src.save_to_excel import SaveToExcel
from tool.adb_event import stop_app, open_app, tap, edge_scroll, tap_element, horizon_swipe
from tool.appium_event import wait_for_element
from tool.image_event import element_match

import time


class CrawlProcess:
    def __init__(self):
        stop_app(boss_appPackage)
        self.driver = webdriver.Remote(
            appium_server_url,
            options=UiAutomator2Options().load_capabilities(capabilities)
        )
        open_app(boss_appPackage, boss_appActivity)
        self.save_to_excel = SaveToExcel()

    def __del__(self):
        try: self.driver.quit()
        except: pass

    def __exit__(self):
        try: self.driver.quit()
        except: pass

    def switch_to_search(self):
        wait_for_element(
            driver=self.driver,
            locator=aby.XPATH,
            value='//android.view.ViewGroup[@resource-id="com.hpbr.bosszhipin:id/cl_card_container"]'
        )

        search_bar = self.driver.find_element(
            by=aby.XPATH,
            value='//android.widget.FrameLayout[@resource-id="com.hpbr.bosszhipin:id/iv_head_bg"]'
        )
        location = search_bar.rect
        end_x = location['x'] + location['width'] + search_bar_bias[0]
        end_y = location['y'] + location['height'] + search_bar_bias[1]
        tap(end_x, end_y)

        wait_for_element(
            driver=self.driver,
            locator=aby.XPATH,
            value='//android.widget.TextView[@resource-id="com.hpbr.bosszhipin:id/tv_title" and @text="搜索发现"]'
        )

        element = self.driver.find_element(
            by=aby.XPATH,
            value='//android.widget.EditText[@resource-id="com.hpbr.bosszhipin:id/et_search"]'
        )
        element.send_keys(job_key)

        search_element = self.driver.find_element(
            by=aby.XPATH,
            value='//android.widget.TextView[@resource-id="com.hpbr.bosszhipin:id/tv_search"]'
        )
        tap_element(search_element.rect)
        wait_for_element(
            driver=self.driver,
            locator=aby.XPATH,
            value='//android.widget.TextView[@resource-id="com.hpbr.bosszhipin:id/tv_tab_label" and @text="综合排序"]'
        )

    def choose_condition(self):
        ##################### 选择排序方法 #####################
        tap_element(self.driver.find_element(
            by=aby.XPATH,
            value='//androidx.recyclerview.widget.RecyclerView[@resource-id="com.hpbr.bosszhipin:id/recyclerview_filter_new"]/android.view.ViewGroup[2]'
        ).rect)
        wait_for_element(
            driver=self.driver,
            locator=aby.XPATH,
            value='//android.widget.TextView[@resource-id="com.hpbr.bosszhipin:id/tv_title"]'
        )
        tap_element(self.driver.find_element(
            by=aby.XPATH,
            value=f'//android.widget.TextView[@resource-id="com.hpbr.bosszhipin:id/tv_sort_type" and @text="{order_require}"]'
        ).rect)
        ##################### 选择排序方法 #####################
        time.sleep(0.5)

    def content_crawl(self):
        tap_element(self.driver.find_element(
            by=aby.XPATH,
            value='(//android.view.ViewGroup[@resource-id="com.hpbr.bosszhipin:id/cl_card_container"])[1]'
        ).rect)

        count_crawl = 0
        while True:
            wait_for_element(
                driver=self.driver,
                locator=aby.XPATH,
                value='//android.widget.ImageView[@resource-id="com.hpbr.bosszhipin:id/iv_favor"]'
            )
            tap_element(self.driver.find_element(
                by=aby.XPATH,
                value='//android.widget.ImageView[@resource-id="com.hpbr.bosszhipin:id/iv_share"]'
            ).rect)
            tap_element(self.driver.find_element(
                by=aby.XPATH,
                value='//android.widget.TextView[@resource-id="com.hpbr.bosszhipin:id/tv_share_link"]'
            ).rect)
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
            except: pass

            # 经验
            job_exp = ''
            try:
                job_exp_element = self.driver.find_element(
                    by=aby.XPATH,
                    value='//android.widget.TextView[@resource-id="com.hpbr.bosszhipin:id/tv_required_work_exp"]'
                )
                job_exp = job_exp_element.text
            except: pass

            # 学历
            job_degree = ''
            try:
                job_degree_element = self.driver.find_element(
                    by=aby.XPATH,
                    value='//android.widget.TextView[@resource-id="com.hpbr.bosszhipin:id/tv_required_degree"]'
                )
                job_degree = job_degree_element.text
            except: pass

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
            except: pass

            edge_scroll(y=-1000, duration=100)
            edge_scroll(y=700, slow_down=True)
            more_button = element_match(more_img_path)
            if more_button[2] > 0.7:
                tap(more_button[0], more_button[1])
                edge_scroll(y=-1000, duration=100)
                edge_scroll(y=700, slow_down=True)

            # 工作详情
            job_content = ''
            try:
                job_content_element = self.driver.find_element(
                    by=aby.XPATH,
                    value='//android.widget.TextView[@resource-id="com.hpbr.bosszhipin:id/tv_description"]'
                )
                job_content = job_content_element.text
            except: pass


            # 附加地区
            try:
                job_are_map_element = self.driver.find_element(
                    by=aby.XPATH,
                    value='//android.widget.TextView[@resource-id="com.hpbr.bosszhipin:id/tv_location"]'
                )
                job_area = f'{job_area}/{job_are_map_element.text}'
            except: pass

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

            self.save_to_excel.save(
                job_name,
                job_salary,
                job_area,
                job_tags,
                job_company,
                job_company_tags,
                job_content,
                job_link
            )
            count_crawl += 1
            print('\n------------------------------------------------------------------------------------')
            print(f'职位：{job_name},薪资：{job_salary}\n,工作地区:{job_area}\n,岗位标签：{job_tags},\n,公司名：{job_company}\n,公司标签：{job_company_tags}\n,工作详情页：\n{job_content}\n,职位沟通链接：{job_link},\n已获取：{count_crawl}')
            print('------------------------------------------------------------------------------------\n')
            horizon_swipe()