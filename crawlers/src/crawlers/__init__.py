from scrapy.utils.project import get_project_settings

from .spiders.diy_dot_com_spider import DiyDotComProductDetailSpider, DiyDotComProductSearchSpider

settings = get_project_settings()
