from logging import getLogger

from misskeycrawler.crawler.crawler import Crawler

logger = getLogger(__name__)


def main():
    horizontal_line = "-" * 80
    logger.info(horizontal_line)
    logger.info("Misskey crawler -> start")
    crawler = Crawler()
    crawler.run()
    logger.info("Misskey crawler -> done")
    logger.info(horizontal_line)


if __name__ == "__main__":
    main()
