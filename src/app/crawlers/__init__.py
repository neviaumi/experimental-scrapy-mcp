from scrapy.utils.project import get_project_settings
from .pipelines import with_result_store, with_in_memory_storage_pipeline
from .spiders.diy_dot_com_spider import DiyDotComProductDetailSpider, DiyDotComProductSearchSpider

settings = get_project_settings()
