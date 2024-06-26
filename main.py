import time

from boss import CrawlProcess
from button_location import first_card
from tool.adb_event import center_scroll, tap

if __name__ == '__main__':
    crawl_process = CrawlProcess()

    crawl_process.switch_to_search()
    crawl_process.choose_condition()
    center_scroll(y=-100, slow_down=True)
    time.sleep(1)

    while True:
        time.sleep(0.25)
        tap(first_card[0], first_card[1])
        crawl_process.content_crawl()
        center_scroll(y=-530, slow_down=True)