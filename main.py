from src.boss import CrawlProcess

if __name__ == '__main__':
    crawl_process = CrawlProcess()
    crawl_process.switch_to_search()
    crawl_process.choose_condition()
    crawl_process.content_crawl()
