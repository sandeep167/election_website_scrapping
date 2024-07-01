import scrapy

class PartyWiseResultsSpider(scrapy.Spider):
    name = 'parli_result_partywise_results'
    allowed_domains = ['results.eci.gov.in']
    start_urls = ['https://results.eci.gov.in/PcResultGenJune2024/index.htm']

    def parse(self, response):
        # Extracting data from the table rows
        table_rows = response.css('table tr.tr')  # Using 'tr.tr' to select only rows with class 'tr'

        for row in table_rows:
            # Extracting data from each row
            party = row.css('td:nth-child(1)::text').get().strip() if row.css('td:nth-child(1)::text').get() else None
            won = row.css('td:nth-child(2) a::text').get().strip() if row.css('td:nth-child(2) a::text').get() else None

            yield {
                'Party': party,
                'Won': won,
            }
