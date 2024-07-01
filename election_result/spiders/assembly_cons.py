import scrapy

class PartyWiseResultsSpider(scrapy.Spider):
    name = 'assembly_cons'
    start_urls = [
        'https://results.eci.gov.in/AcResultGenJune2024/partywiseresult-S01.htm',
        'https://results.eci.gov.in/AcResultGenJune2024/partywiseresult-S18.htm',
    ]

    def parse(self, response):
        # Extract the heading for Andhra Pradesh
        heading = response.xpath('//h2/span/strong/text()').get()
        
        # Select all rows within the table body
        rows = response.xpath('//table[@class="table"]/tbody/tr')
        
        for row in rows:
            party = row.xpath('.//td[1]/text()').get().strip()
            won = row.xpath('.//td[2]/a/text()').get().strip()

            yield {
                'state': heading,
                'party': party,
                'won': won,
            }
