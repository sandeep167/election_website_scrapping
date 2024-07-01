"""import scrapy

class ParliamentaryConstituenciesSpider(scrapy.Spider):
    name = "parli_cons"
    allowed_domains = ["results.eci.gov.in"]
    start_urls = ["https://results.eci.gov.in/PcResultGenJune2024/index.htm"]

    def parse(self, response):
        self.logger.info(f"Fetching URL: {response.url}")

        # Extract state options
        state_options = response.css('#ctl00_ContentPlaceHolder1_Result1_ddlState option')

        # Iterate over each state option and construct the URL for party-wise results
        for option in state_options:
            state_value = option.css('::attr(value)').get()
            state_name = option.css('::text').get()
            if state_value and state_name:
                # Construct URL for party-wise results using state_value
                partywise_url = f"https://results.eci.gov.in/PcResultGenJune2024/partywiseresult-{state_value}.htm"
                self.logger.info(f"State Value: {state_value}, URL: {partywise_url}, State Name: {state_name}")
                # Yield a new request for each partywise_url, passing state_name as meta data
                yield scrapy.Request(url=partywise_url, meta={'state_name': state_name}, callback=self.parse_partywise_results)

    def parse_partywise_results(self, response):
        # Extract the state name from the meta data
        state_name = response.meta['state_name']
        self.logger.info(f"Scraping URL: {response.url} for State: {state_name}")

        # Yield each row of party-wise results
        rows = response.css('table.table tbody tr')
        for row in rows:
            party = row.css('td:nth-child(1)::text').get(default='').strip()
            won = row.css('td:nth-child(2) a::text').get(default='').strip()
            leading = row.css('td:nth-child(3)::text').get(default='').strip()
            total = row.css('td:nth-child(4)::text').get(default='').strip()

            yield {
                'state': state_name,
                'party': party,
                'won': won,
                'leading': leading,
                'total': total,
                'table_type': 'party_results'  # Marking as party-wise result
            }

    def closed(self, reason):
        self.logger.info(f"Spider closed: {reason}")

if __name__ == "__main__":
    from scrapy.crawler import CrawlerProcess
    import csv

    # Define settings for CSV export
    settings = {
        'FEEDS': {
            'state_wise_results.csv': {
                'format': 'csv',
                'fields': ['state', 'party', 'won', 'leading', 'total'],
                'overwrite': True,
            },
        },
        'LOG_LEVEL': 'INFO',
    }

    # Run the spider with defined settings
    process = CrawlerProcess(settings)
    process.crawl(ParliamentaryConstituenciesSpider)
    process.start()"""
