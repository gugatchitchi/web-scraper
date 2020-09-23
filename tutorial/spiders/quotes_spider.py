import scrapy

# TO RUN:
# to append json file ---->    scrapy crawl quotes --nolog -o quotes1.json 
# to overwrite jsaon file ----> scrapy crawl quotes -t json --nolog -o "quotes1.json"
# TODO overwrite does not work if you do not access different file first. dont know why.
class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'https://imedinews.ge/ge/archive',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for item in response.css('a.single-item'):

            post_title      = item.css('h3.title::text').get()
            post_descrip    = item.css('p.description::text').get()[4:-4].strip()
            post_date       = item.css('p.date::text').get()
            post_imgUrl     = item.css('div.youtube-bg').attrib['style'][22:-2]

            data = {
                'title': post_title,
                'descrip': post_descrip,
                'date': post_date, 
                'imgUrl': post_imgUrl
            }

            yield data