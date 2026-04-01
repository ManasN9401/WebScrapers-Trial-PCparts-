import json
import argparse
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich import box

def load_data(data_dir):
    items = []
    p = Path(data_dir)
    if not p.exists():
        return items
        
    for jsonl_file in p.glob("**/*.jsonl"):
        with open(jsonl_file, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    items.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return items

def search_items(items, query=None, max_price=None, retailer=None):
    results = items
    
    if query:
        query = query.lower()
        results = [i for i in results if query in i.get("name", "").lower()]
        
    if max_price is not None:
        results = [i for i in results if i.get("price_num", float('inf')) <= max_price]
        
    if retailer:
        retailer = retailer.lower()
        results = [i for i in results if retailer in i.get("retailer", "").lower()]
        
    return sorted(results, key=lambda x: x.get("price_num", 0))

def main():
    parser = argparse.ArgumentParser(description="Search scraped PC parts")
    parser.add_argument("-q", "--query", help="Text to search in component name")
    parser.add_argument("-m", "--max-price", type=float, help="Maximum price")
    parser.add_argument("-r", "--retailer", help="Filter by retailer")
    parser.add_argument("-d", "--data-dir", default="./data", help="Directory containing JSONL files")
    
    args = parser.parse_args()
    
    console = Console()
    with console.status("[bold green]Loading JSONL data...") as status:
        items = load_data(args.data_dir)
    
    if not items:
        console.print("[bold red]No data found! Run the Scrapy spiders first to generate JSONL data.[/bold red]")
        return
        
    results = search_items(items, args.query, args.max_price, args.retailer)
    
    table = Table(title=f"Search Results ({len(results)} items found)", box=box.ROUNDED)
    table.add_column("Price", justify="right", style="green", no_wrap=True)
    table.add_column("Part Name", style="cyan")
    table.add_column("Retailer", style="magenta")
    table.add_column("Stock", justify="center")
    
    for item in results:
        stock_status = "[green]Yes[/]" if item.get("in_stock") else "[red]Unknown/No[/]"
        table.add_row(
            item.get("price_str", "$0.00"),
            item.get("name", "Unknown"),
            item.get("retailer", "Unknown"),
            stock_status
        )
        
    console.print(table)

if __name__ == "__main__":
    main()
