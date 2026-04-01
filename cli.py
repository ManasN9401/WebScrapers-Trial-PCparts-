import typer
from rich.console import Console
from rich.table import Table
import subprocess
import json
from pathlib import Path

app = typer.Typer(help="CLI for PC Parts Scraper")
console = Console()

@app.command()
def scrape(retailer: str = typer.Option(..., help="Retailer to scrape (amazon, bestbuy, microcenter)"), 
           query: str = typer.Option(..., help="Search query for parts")):
    """
    Scrape a retailer for PC parts based on a search query.
    """
    console.print(f"[bold green]Starting scraping job for {retailer} with query '{query}'...[/bold green]")
    try:
        # Run scrapy spider via subprocess
        # Pass query as a spider argument
        command = ["scrapy", "crawl", retailer, "-a", f"query={query}"]
        subprocess.run(command, check=True)
        console.print("[bold green]Scraping completed successfully![/bold green]")
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]Scraping failed: {e}[/bold red]")

@app.command()
def search(max_price: float = typer.Option(None, help="Maximum price to filter by"),
           name_contains: str = typer.Option(None, help="Filter by name content")):
    """
    Search and display local scraped computer parts.
    """
    data_file = Path("scraped_data.jsonl")
    if not data_file.exists():
        console.print("[bold red]No scraped data found. Run the 'scrape' command first.[/bold red]")
        return
        
    table = Table(title="Scraped PC Parts")
    table.add_column("Retailer", style="cyan", no_wrap=True)
    table.add_column("Name", style="magenta")
    table.add_column("Price", justify="right", style="green")
    table.add_column("Stock Status", style="yellow")
    table.add_column("URL", style="blue")

    with open(data_file, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip(): continue
            item = json.loads(line)
            
            price = item.get("price")
            # Filter logic
            if max_price is not None and price is not None:
                try:
                    # Strip symbols like $ and commas
                    clean_price = float(str(price).replace("$", "").replace(",", ""))
                    if clean_price > max_price:
                        continue
                except ValueError:
                    pass
            
            if name_contains is not None and name_contains.lower() not in item.get("name", "").lower():
                continue

            table.add_row(
                item.get("retailer", "Unknown"),
                item.get("name", "Unknown")[:50] + "..." if len(item.get("name", "")) > 50 else item.get("name", ""),
                str(price),
                item.get("stock_status", "Unknown"),
                item.get("url", "Unknown")[:30] + "..."
            )
            
    console.print(table)

if __name__ == "__main__":
    app()
