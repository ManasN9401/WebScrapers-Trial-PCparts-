import scrapy
from datetime import datetime
from pc_parts.items import PcPartsItem


class MicrocenterSpider(scrapy.Spider):
    name = "microcenter"
    allowed_domains = ["microcenter.com"]
    # Starting with GPUs for example
    start_urls = ["https://www.microcenter.com/category/4294966937/video-cards"]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                meta={
                    "playwright": True,
                    "playwright_include_page": True,
                },
                callback=self.parse
            )

    async def parse(self, response):
        page = response.meta["playwright_page"]
        
        # MicroCenter structures their product list under .product_wrapper
        products = response.css(".product_wrapper")
        
        for product in products:
            item = PcPartsItem()
            item["part_type"] = "GPU"
            
            # The name is generally inside an <a> tag inside .normal
            item["name"] = product.css(".normal a::text").get(default="").strip()
            
            # The price is normally split into .price and .cents
            price_dollars = product.css(".price::text").get(default="0").strip()
            price_cents = product.css(".price .cents::text").get(default="00").strip()
            item["price_str"] = f"${price_dollars}.{price_cents}"
            
            try:
                # Convert price string like "1,599" to float 1599.0
                item["price_num"] = float(price_dollars.replace(",", "")) + (float(price_cents) / 100)
            except ValueError:
                item["price_num"] = 0.0
                
            item["currency"] = "USD"
            item["retailer"] = "Micro Center"
            
            relative_url = product.css(".normal a::attr(href)").get()
            item["url"] = response.urljoin(relative_url) if relative_url else ""
            
            item["timestamp"] = datetime.utcnow().isoformat() + "Z"
            
            # Check for stock status
            stock_text = product.css(".inventoryCnt::text").get(default="").lower()
            item["in_stock"] = "in stock" in stock_text or "available" in stock_text
            
            if item["name"]:
                yield item

        # Handle pagination (find the 'next >' button)
        next_page = response.css(".pagination .next a::attr(href)").get()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                meta={"playwright": True, "playwright_include_page": True},
                callback=self.parse
            )

        # Debug why no elements were found by taking a screenshot
        await page.screenshot(path="../data/microcenter_debug.png", full_page=True)
        # We must close the playwright page according to scrapy-playwright docs
        await page.close()
