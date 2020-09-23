import scrapy

# TO RUN:
# to append json file ---->    scrapy crawl quotes --nolog -o imediNews.json 
# to overwrite jsaon file ----> scrapy crawl quotes -t json --nolog -o "quotes1.json"
# TODO overwrite does not work if you do not access different file first. dont know why.
class QuotesSpider(scrapy.Spider):
    name = "quotes"

    # Starts the request to the urls
    def start_requests(self):
        urls = [
            'https://imedinews.ge/ge/archive',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    # Gets the data forthe given urls
    def parse(self, response):
        # Itterates trhough 'a.single-item' on the url
        # for every item returns it title, description, image url and date
        for item in response.css('a.single-item'):
            # Get General data for the post
            post_title = item.css('h3.title::text').get()
            post_descrip = item.css('p.description::text').get()[4:-4].strip()
            post_imgUrl = item.css('div.youtube-bg').attrib['style'][22:-2]

            # Get date for the post
            date  = item.css('p.date::text').get()[0:-2]
            # extract day, year and month name
            day = date[:2]
            year = date[-4:]
            month_name = date[3:-5]
            # Default month if something is wrong with month_name
            month = 'month'
            # We check month_name to generate month number
            if(month_name == 'იანვარი'):
                month = '01'
            if(month_name == 'თებერვალი'):
                month = '02'
            if(month_name == 'მარტი'):
                month = '03'
            if(month_name == 'აპრილი'):
                month = '04'
            if(month_name == 'მაისი'):
                month = '05'
            if(month_name == 'ივნისი'):
                month = '06'
            if(month_name == 'ივლისი'):
                month = '07'
            if(month_name == 'აგვისტო'):
                month = '08'
            if(month_name == 'სექტემბერი'):
                month = '09'
            if(month_name == 'ოქტომბერი'):
                month = '10'
            if(month_name == 'ნოემბერი'):
                month = '11'
            if(month_name == 'დეკემბერი'):
                month = '12'
            # Create date with day, moneht and year
            post_date = day + "-" + month + "-" + year

            # Generate unique id for each post
            post_id = "imediNews_"+post_title[0:3]+post_title[-3:-1]+post_descrip[0:3]+post_descrip[-3:-1]+"_"+post_date

            # Asign all data to the object
            data = {
                'id': post_id,
                'title': post_title,
                'descrip': post_descrip,
                'date': post_date, 
                'imgUrl': post_imgUrl
            }

            # yield the data object
            yield data

        # If there is next page go there and repeat actions
        next_page = response.css('a.pgng-navigation__next::attr(href)').get()
        if next_page is not 'javascript:void(0)':
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
