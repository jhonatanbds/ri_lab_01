# -*- coding: utf-8 -*-
import scrapy
import json
from datetime import datetime
from ri_lab_01.items import RiLab01Item
from ri_lab_01.items import RiLab01CommentItem


class BrasilElpaisSpider(scrapy.Spider):
    name = 'brasil_elpais'
    allowed_domains = ['brasil.elpais.com']
    start_urls = []

    def __init__(self, *a, **kw):
        super(BrasilElpaisSpider, self).__init__(*a, **kw)
        with open('seeds/brasil_elpais.json') as json_file:
                data = json.load(json_file)
        self.start_urls = list(data.values())

    
    def parse(self, response):
        for next_article in response.css('a::attr(href)').getall():
            if (self.is_valid_url(next_article)):        
                yield scrapy.Request("https:" + next_article, callback=self.get_data)
                
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

    def is_valid_url(self, url):
        return "brasil.elpais.com/brasil/2019" in url


    def get_data(self, response):
        all_text = response.css('div.articulo__contenedor p::text').getall()
        article_text = ''
        for w in all_text:
            article_text += w
        return {
                # título
                'titulo': response.css('h1.articulo-titulo::text').get(default='Sem título').strip(),
                # subtítulo
                'subtitulo': response.css('h2.articulo-subtitulo::text').get(default='Sem subtítulo').strip(),
                # autor
                'autor': response.css('span.autor-nombre a::text').get(default='Sem autor').strip(),
                # data (dd/mm/yyyy hh:mi:ss)
                'data': response.css('time::attr(datetime)').get(default='Sem data').strip(),
                # seção (esportes, economia, etc.)
                'secao': response.url.split('/')[-2],
                # texto
                'texto': article_text,
                # url 
                'url': response.url
            }