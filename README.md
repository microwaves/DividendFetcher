# DividendFetcher

DividendFetcher is a Python script that fetches dividend information for stocks in a specified index. It retrieves the stock symbols from a Wikipedia page and uses the Yahoo Finance API to gather the dividend data. The script is capable of displaying the dividend yield, annual dividend, price-to-book (P/B) ratio, and Yahoo Finance profile link for each stock in a tabular format.

## Features

- Fetch dividend data for stocks in various indices
- Use multi-threading for better performance
- Display dividend yield, annual dividend, P/B ratio, and Yahoo Finance profile link
- Configurable index mappings using a config.yaml file

## Requirements

- Python 3.6+
- pandas
- yfinance
- tabulate
- tqdm
- wikipedia-api
- PyYAML

## Installation

1. Clone the repository:

```bash
git clone https://github.com/microwaves/DividendFetcher.git
```

2. Change the working directory:

```bash
cd DividendFetcher
```

3. Install the required packages:

```bash
pip install -r requirements.txt
```

4. Configure the index mappings in the `config.yaml` file.

## Configuration

DividendFetcher allows you to configure the index mappings using a `config.yaml` file. This file contains a dictionary that maps index ticker symbols to their respective Wikipedia URLs.

Here's an example of the `config.yaml` file structure:

```yaml
indices:
  ^GSPC: List of S&P 500 companies
  ^IXIC: NASDAQ-100
  ^DJI: Dow Jones Industrial Average
  ^FTSE: FTSE 100 Index
  ^GDAXI: DAX
  ^FCHI: CAC 40
  ^STOXX50E: EURO STOXX 50
  ^IBEX: IBEX 35
  ^AEX: AEX index
```

To add more index mappings, simply add a new entry in the `indices` dictionary with the format:

```yaml
INDEX_TICKER: WIKIPEDIA_PAGE_TITLE
```

where INDEX_TICKER is the index ticker symbol (e.g., ^GSPC, ^IXIC) and WIKIPEDIA_PAGE_TITLE is the title of the Wikipedia page containing the list of stock symbols for that index.

## Usage

```bash
python dividend_fetcher.py --index-ticker INDEX_TICKER [--threads NUM_THREADS]
```

- `INDEX_TICKER`: The ticker symbol of the index you want to fetch stock symbols from (e.g., ^GSPC, ^IXIC, ^DJI).
- `NUM_THREADS`: (Optional) The number of threads to use for fetching dividend data (default: 4).

## Example

Fetch dividend data for the S&P 500 index:

```bash
python dividend_fetcher.py --index-ticker ^GSPC --threads 8
```

## License

This project is licensed under the BSD License. See [LICENSE](LICENSE).