# PC Parts Scraper

A Scrapy-based web scraper project for educational purposes, designed to demonstrate web scraping techniques in a controlled environment.

## Overview

This workspace contains a Scrapy spider that scrapes PC component data (GPUs, CPUs, RAM) from a local mock website. The project is set up as a learning environment for understanding how web scrapers work and the security measures that websites employ to prevent automated data extraction.

## Project Structure

```
pc_parts_scraper/
├── pc_parts/
│   ├── spiders/
│   │   ├── mock_spider.py      # Spider that scrapes the local mock store
│   │   ├── bestbuy.py          # Spider template for Best Buy
│   │   └── microcenter.py      # Spider template for Micro Center
│   ├── items.py                # Data item definitions
│   ├── pipelines.py            # Data processing pipelines
│   ├── middlewares.py          # Request/response middlewares
│   └── settings.py             # Scrapy configuration
├── mock_server/
│   └── mock_store.html         # Fake e-commerce website for testing
├── scrapy.cfg                  # Scrapy project configuration
└── README.md                   # This file
```

## What Are Web Scrapers?

Web scrapers are automated programs that extract data from websites by:

1. **Sending HTTP requests** to web servers to retrieve HTML pages
2. **Parsing the HTML** to locate specific elements containing desired data
3. **Extracting information** from those elements (text, attributes, etc.)
4. **Storing the data** in structured formats (JSON, CSV, databases)

This project uses [Scrapy](https://scrapy.org/), a popular Python framework that handles HTTP requests, HTML parsing with CSS selectors, and data export.

## Why Web Scraping Has Become Difficult

Modern websites employ numerous security measures to detect and block automated scrapers:

### Common Anti-Bot Defenses

| Defense | Description |
|---------|-------------|
| **Rate Limiting** | Restricts requests from single IPs in short time windows |
| **CAPTCHAs** | Challenges that are easy for humans but hard for bots |
| **JavaScript Rendering** | Content loaded dynamically, requiring headless browsers |
| **Fingerprinting** | Analyzes browser characteristics to detect non-human traffic |
| **IP Blocking** | Blacklists IPs exhibiting bot-like behavior |
| **Honeypot Traps** | Hidden links that only bots would follow |
| **User-Agent Analysis** | Blocks requests from known scraper libraries |
| **Behavioral Analysis** | Tracks mouse movements, click patterns, timing |

### Services That Protect Websites

- **Cloudflare** - DDoS protection with bot detection challenges
- **Akamai** - Enterprise-grade bot management
- **DataDome** - Real-time bot detection and blocking
- **PerimeterX** - Behavioral analysis and fingerprinting
- **Imperva** - Web application firewall with bot mitigation

## Educational Purpose

This project provides a **safe, legal environment** to learn web scraping without:
- Violating terms of service
- Risking legal action under the CFAA or similar laws
- Harming real websites or their infrastructure
- Dealing with complex anti-bot measures initially

The included `mock_spider.py` scrapes data from `mock_store.html`, a fake e-commerce site that mimics real product listing pages.

## Running the Spider

### Prerequisites

```bash
# Activate the virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Start the Mock Server

In a separate terminal, serve the mock HTML file:

```bash
cd mock_server
python -m http.server 8000
```

### Run the Spider

```bash
scrapy crawl mock -o output.json
```

### Output Example

```json
[
  {
    "name": "NVIDIA GeForce RTX 5090 Founders Edition",
    "part_type": "GPU",
    "price_str": "$1,999.99",
    "price_num": 1999.99,
    "currency": "USD",
    "retailer": "Irrelevant PC Parts",
    "in_stock": true
  }
]
```

## Configuration

Key settings in `pc_parts/settings.py`:

- **USER_AGENT**: Mimics a real Chrome browser to avoid simple UA blocking
- **DOWNLOAD_DELAY**: 3 seconds between requests to avoid rate limiting
- **PLAYWRIGHT**: Headless Chromium for JavaScript-rendered content
- **ROBOTSTXT_OBEY**: Set to `False` for educational testing

## Ethical Considerations

When scraping websites in the real world:

1. **Always read `robots.txt`** - Respect the site's crawling policies
2. **Check Terms of Service** - Some sites explicitly prohibit scraping
3. **Rate limit yourself** - Don't overwhelm servers with requests
4. **Scrape only public data** - Never attempt to access authenticated content
5. **Consider the impact** - Your scraper shouldn't degrade site performance
6. **Use official APIs when available** - Many sites provide structured data access

## Disclaimer

This project is for **educational purposes only**. The techniques demonstrated should only be used on:
- Websites you own
- Websites with explicit permission
- Sites that allow scraping in their terms of service

Unauthorized access to computer systems may violate laws including the Computer Fraud and Abuse Act (CFAA) in the United States or similar legislation in other jurisdictions.
