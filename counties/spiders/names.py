#!/usr/bin/python3
import scrapy
import os
#creating a directory name data
if os.path.exists('data'):
    pass
else:
    os.mkdir('data')

class NamesSpider(scrapy.Spider):
    name = 'names'
    start_urls = [
    'https://en.wikipedia.org/wiki/List_of_counties_by_U.S._state_and_territory',
    
    ]

    def parse(self,response):

        all_counties = response.css('.column-width:nth-child(74) li:nth-child(10) , .column-width li > a::text').extract()
        for county in all_counties:
            county_state = county.split(", ")
            #if statement removes the unnecessary data in the reponse
            if (len(county_state)==2):
                if os.path.exists(f'data/{county_state[1]}'):
                    #checking the existing path
                    if os.path.exists(f'data/{county_state[1]}/{county_state[0]}'):
                        pass
                    else:
                        os.mkdir(f'data/{county_state[1]}/{county_state[0]}')
                        #reating the .gitkeep file
                        with open(f'data/{county_state[1]}/{county_state[0]}/.gitkeep', 'w') as fp: 
                            pass
                else:
                    os.mkdir(f'data/{county_state[1]}')
                    if os.path.exists(f'data/{county_state[1]}/{county_state[0]}'):
                        pass
                    else:
                        os.mkdir(f'data/{county_state[1]}/{county_state[0]}')
                        with open(f'data/{county_state[1]}/{county_state[0]}/.gitkeep', 'w') as fp: 
                            pass