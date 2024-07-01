import scrapy

class AreaStateSpider(scrapy.Spider):
    name = 'by_election'
    start_urls = ['https://results.eci.gov.in/AcResultByeJune2024/index.htm']

    def parse(self, response):
        # Extracting all box-content sections
        box_contents = response.css('div.box-content')

        for box in box_contents:
            # Extracting area and state information from each box-content
            area = box.css('h3::text').get()
            state = box.css('h4::text').get()

            # Extracting additional details
            won_status = box.css('h2.won::text').get()
            candidate_name = box.css('h5::text').get()
            party_name = box.css('h6::text').get()

            yield {
                'Area': area.strip() if area else None,
                'State': state.strip() if state else None,
                'Won_Status': won_status.strip() if won_status else None,
                'Candidate_Name': candidate_name.strip() if candidate_name else None,
                'Party_Name': party_name.strip() if party_name else None,
            }
