import scrapy

class ResultsSpider(scrapy.Spider):
    name = "parli_result_state_wise"
    allowed_domains = ["results.eci.gov.in"]
    start_urls = ["https://results.eci.gov.in/PcResultGenJune2024/index.htm"]

    def parse(self, response):
        self.logger.info(f"Fetching URL: {response.url}")

        # Extract state options
        state_options = response.css('#ctl00_ContentPlaceHolder1_Result1_ddlState option')

        # Iterate over each state option and construct the URL
        for option in state_options:
            state_value = option.css('::attr(value)').get()
            state_name = option.css('::text').get()
            if state_value and state_name:
                # Construct URL for party-wise results using state_value
                partywise_url = f"https://results.eci.gov.in/PcResultGenJune2024/partywiseresult-{state_value}.htm"
                self.logger.info(f"State Value: {state_value}, URL: {partywise_url}, State Name: {state_name}")
                # Yield a new request for each partywise_url
                yield scrapy.Request(url=partywise_url, callback=self.parse_partywise_results)

    def parse_partywise_results(self, response):
        # Extract the state name from the <h2> tag
        state_name = response.css('h2 span strong::text').get()
        self.logger.info(f"Scraping URL: {response.url} for State: {state_name}")

        # Extract data from the table
        rows = response.css('table.table tbody tr')
        for row in rows:
            party = row.css('td:nth-child(1)::text').get(default='').strip()
            won = row.css('td:nth-child(2) a::text').get(default='').strip()

            yield {
                'state': state_name,
                'party': party,
                'won': won,
            }
