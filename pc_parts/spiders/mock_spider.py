import scrapy
from datetime import datetime
from pc_parts.items import PcPartsItem

class MockSpider(scrapy.Spider):
    name = "mock"
    allowed_domains = ["localhost"]
    start_urls = ["http://localhost:8000/mock_store.html"]

    def parse(self, response):
        products = response.css(".product")
        
        for product in products:
            item = PcPartsItem()
            
            item["name"] = product.css("h2.name a::text").get(default="").strip()
            
            if "RTX" in item["name"]:
                item["part_type"] = "GPU"
            elif "Ryzen" in item["name"]:
                item["part_type"] = "CPU"
            else:
                item["part_type"] = "RAM"
                
            price_dollars = product.css(".price::text").get(default="$0.00").strip()
            item["price_str"] = price_dollars
            
            clean_price = price_dollars.replace("$", "").replace(",", "")
            try:
                item["price_num"] = float(clean_price)
            except ValueError:
                item["price_num"] = 0.0
                
            item["currency"] = "USD"
            item["retailer"] = "Irrelevant PC Parts"
            
            relative_url = product.css("h2.name a::attr(href)").get()
            item["url"] = response.urljoin(relative_url) if relative_url else ""
            
            item["timestamp"] = datetime.utcnow().isoformat() + "Z"
            
            stock_text = product.css(".stock-status span.avail::text").get(default="").lower()
            item["in_stock"] = "yes" in stock_text
            
            if item["name"]:
                yield item
