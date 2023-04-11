import argparse
import pandas as pd
import yfinance as yf
from tabulate import tabulate
from tqdm import tqdm
import concurrent.futures
import wikipediaapi
import yaml

def load_config():
    with open('config.yaml', 'r') as f:
        return yaml.safe_load(f)

CONFIG = load_config()
INDEX_NAME_MAP = CONFIG['index_mapping']

def get_wikipedia_page_url(index_name):
    wiki_wiki = wikipediaapi.Wikipedia('en')
    page = wiki_wiki.page(index_name)

    if not page.exists():
        raise ValueError("Index Not Found")
    
    return page.fullurl

def fetch_symbols(url):
    tables = pd.read_html(url, header=0)
    
    for table in tables:
        if 'Symbol' in table.columns:
            symbols = table['Symbol'].tolist()
            break
        elif 'Ticker symbol' in table.columns:
            symbols = table['Ticker symbol'].tolist()
            break
        elif 'Ticker' in table.columns:
            symbols = table['Ticker'].tolist()
            break
    else:
        raise KeyError("Symbol column not found in the Wikipedia table")

    return symbols

def fetch_single_stock_dividend_data(symbol):
    stock = yf.Ticker(symbol)
    info = stock.info
    dividend_yield = info.get('dividendYield', None)
    annual_dividend = info.get('trailingAnnualDividendRate', None)
    pb_ratio = info.get('priceToBook', None)
    profile_url = f'https://finance.yahoo.com/quote/{symbol}'

    if dividend_yield and annual_dividend and pb_ratio:
        return {
            'symbol': symbol,
            'dividend': annual_dividend,
            'dividend_yield': dividend_yield * 100,
            'pb_ratio': pb_ratio,
            'profile_url': profile_url
        }
    return None

def fetch_dividend_data(stock_symbols, threads):
    stock_data = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {executor.submit(fetch_single_stock_dividend_data, symbol): symbol for symbol in stock_symbols}
        for future in tqdm(concurrent.futures.as_completed(futures), total=len(stock_symbols), desc='Fetching dividend data', unit='stocks'):
            result = future.result()
            if result:
                stock_data.append(result)

    return stock_data

def display_dividend_data(stock_data):
    sorted_data = sorted(stock_data, key=lambda x: x['dividend_yield'], reverse=True)
    table_data = [(d['symbol'], d['dividend'], f"{d['dividend_yield']:.2f}%", d['pb_ratio'], d['profile_url']) for d in sorted_data]
    headers = ['Stock Symbol', 'Dividend (Currency)', 'Dividend Yield', 'P/B Ratio', 'Yahoo Finance Profile']
    print(tabulate(table_data, headers=headers, tablefmt='pretty'))

def main(index_ticker, threads):
    if index_ticker not in INDEX_NAME_MAP:
        print("Index Not Found")
        return

    index_name = INDEX_NAME_MAP[index_ticker]
    try:
        wikipedia_url = get_wikipedia_page_url(index_name)
        symbols = fetch_symbols(wikipedia_url)
        dividend_data = fetch_dividend_data(symbols, threads)
        display_dividend_data(dividend_data)
    except ValueError as e:
        print(e)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fetch dividend data for stocks from a specified index')
    parser.add_argument('--index-ticker', type=str, required=True, help='Index ticker to fetch stock symbols from (e.g., "^GSPC", "^IXIC", "^DJI").')
    parser.add_argument('--threads', type=int, default=4, help='Number of threads to use for fetching dividend data (default: 4)')
    args = parser.parse_args()

    main(args.index_ticker, args.threads)