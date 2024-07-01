import scrapy
from scrapy.exporters import CsvItemExporter

class ResultsSpider(scrapy.Spider):
    name = "test"
    allowed_domains = ["results.eci.gov.in"]
    start_urls = ["https://results.eci.gov.in/PcResultGenJune2024/index.htm"]
    
    # Initialize all_results as an empty list
    all_results = []

    def parse(self, response):
        # Extract state options
        state_options = response.css('#ctl00_ContentPlaceHolder1_Result1_ddlState option')

        # Iterate over each state option and construct the URL
        for option in state_options:
            state_value = option.css('::attr(value)').get()
            state_name = option.css('::text').get().strip()
            if state_value and state_name:
                # Construct URL for party-wise results using state_value
                partywise_url = f"https://results.eci.gov.in/PcResultGenJune2024/partywiseresult-{state_value}.htm"
                self.logger.info(f"State Value: {state_value}, URL: {partywise_url}, State Name: {state_name}")
                # Yield a new request for each partywise_url
                yield scrapy.Request(url=partywise_url, callback=self.parse_partywise_results, meta={'state_name': state_name})

    def parse_partywise_results(self, response):
        # Extract the state name from the meta data passed in the request
        state_name = response.meta.get('state_name', 'Unknown State')
        self.logger.info(f"Scraping URL: {response.url} for State: {state_name}")

        # Extract data from the table
        rows = response.css('div.card-body table.table tbody tr')
        for row in rows:
            party = row.css('td:nth-child(1)::text').get(default='').strip()
            won = row.css('td:nth-child(2) a::text').get(default='').strip()
            leading = row.css('td:nth-child(3)::text').get(default='').strip()
            total = row.css('td:nth-child(4)::text').get(default='').strip()

            # Append the extracted data to all_results
            self.all_results.append({
                'state': state_name,
                'party': party,
                'won': won,
                'leading': leading,
                'total': total,
            })

    def closed(self, reason):
        # Export all_results to a single CSV file
        if self.all_results:
            output_file = "state_partywise_results.csv"
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                exporter = CsvItemExporter(f)
                exporter.start_exporting()
                exporter.fields_to_export = ['state', 'party', 'won', 'leading', 'total']

                for result in self.all_results:
                    exporter.export_item({k: str(v) for k, v in result.items() if v is not None})

                exporter.finish_exporting()

            self.log(f"All state and party-wise results exported to {output_file}")
