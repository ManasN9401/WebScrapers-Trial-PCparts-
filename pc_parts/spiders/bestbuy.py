import scrapy
from datetime import datetime
from pc_parts.items import PcPartsItem


class BestbuySpider(scrapy.Spider):
    name = "bestbuy"
    allowed_domains = ["bestbuy.com"]
    # Starting with GPUs for example
    start_urls = ["https://www.bestbuy.com/site/computer-cards-components/video-graphics-cards/abcat0507002.c?id=abcat0507002"]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                meta={
                    "playwright": True,
                    "playwright_include_page": True,
                    # Handle anti-bot waiting for rendering
                },
                callback=self.parse
            )

    async def parse(self, response):
        page = response.meta["playwright_page"]
        
        products = response.css(".sku-item")
        
        for product in products:
            item = PcPartsItem()
            item["part_type"] = "GPU"
            
            item["name"] = product.css(".sku-title a::text").get(default="").strip()
            
            price_dollars = product.css(".priceView-hero-price span[aria-hidden='true']::text").get(default="0").strip()
            item["price_str"] = price_dollars
            
            # Remove $ and commas from price
            clean_price = price_dollars.replace("$", "").replace(",", "")
            try:
                item["price_num"] = float(clean_price)
            except ValueError:
                item["price_num"] = 0.0
                
            item["currency"] = "USD"
            item["retailer"] = "Best Buy"
            
            relative_url = product.css(".sku-title a::attr(href)").get()
            item["url"] = response.urljoin(relative_url) if relative_url else ""
            
            item["timestamp"] = datetime.utcnow().isoformat() + "Z"
            
            # In stock often doesn't have "Sold Out" button text disabled
            stock_text = product.css(".add-to-cart-button::text").get(default="").lower()
            item["in_stock"] = "add to cart" in stock_text
            
            if item["name"]:
                yield item

        next_page = response.css(".paging-list .next a::attr(href)").get()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                meta={"playwright": True, "playwright_include_page": True},
                callback=self.parse
            )

        # Scrapy-Playwright requires us to close pages if requested in meta
        await page.close()
