import requests
from bs4 import BeautifulSoup
import html5lib
from requests_html import HTMLSession
import pandas as pd

import asyncio
if asyncio.get_event_loop().is_running(): # Only patch if needed (i.e. running in Notebook, Spyder, etc)
    import nest_asyncio
    nest_asyncio.apply()
        
class scraping:
    def get_links(self, links):
        links2 = []
        session = HTMLSession()
        for url in links:
            r = session.get(url)
            r.html.render(timeout=15, sleep=15)
            soup = BeautifulSoup(r.html.html,'html5lib')
            products = soup.find_all('a',class_='product-info product-name')
            for i in products:
                if(i.get('href') is not None):
                    x = 'https://www.vitaminshoppe.com' + i.get('href')
                    links2.append(x)
        session.close()
        return links2
    
    def scrape_data(self,links2):
        brands = []
        names = []
        reg_prices = []
        sale_prices = []
        for url in links2:
            session = HTMLSession()
            r = session.get(url)
            r.html.render(sleep=16,timeout=16)
            soup = BeautifulSoup(r.html.html,'html5lib')
            session.close()
            brand = soup.find('div', class_='productBrandName')
            if(brand is not None):
                brand = brand.get_text()
            name = soup.find('h1',class_='pdp-redesign--product-heading reduce__size-product-name')
            if(name is not None):
                name = name.get_text()
            reg_price = soup.find(class_='price-reduced-opacity-40')
            if(reg_price is not None):
                reg_price = reg_price.get_text()
            sale_price=soup.find(class_='priceCurrencyLabel price-reduced-opacity-40 sale-price-displayed')
            if(sale_price is not None):
                sale_price = sale_price.get_text()
                
            brands.append(brand)
            names.append(name)
            reg_prices.append(reg_price)
            sale_prices.append(sale_price)
            # print('brand:',brand,'name:',name,'reg_price:',reg_price,'sale_price:',sale_price)
            
            img = []
            images = soup.find_all('img',{'class':'cloudzoom'})
            for i in images:
                x = i.get('src')
                if x is not None:
                    img.append(x)

            count = 0
            for i in img:
                r = requests.get(i)
                count += 1
                f = str(name) + '_' + str(count)
                # path = os.path.images(f)
                file = open("images/"+f,'wb')
                file.write(r.content)
                file.close
                
            info = soup.find('div',{'class':'container-fluid remove-padd'})
        
        d = {}
        d['brand']=brands
        d['name']=names
        d['reg_price']=reg_prices
        d['sale_price']=sale_prices
        
        return d
    
    def write_to_csv(self, d):
        (pd.DataFrame.from_dict(data=d, orient='columns').to_csv('dict_file.csv', header=False))
  
        
links = []
links.append('https://www.vitaminshoppe.com/c/vitamins-supplements/multivitamins/women-s-multivitamins?page=1')
links.append('https://www.vitaminshoppe.com/c/vitamins-supplements/multivitamins/women-s-multivitamins?page=2')
links.append('https://www.vitaminshoppe.com/c/vitamins-supplements/multivitamins/women-s-multivitamins?page=3')
links.append('https://www.vitaminshoppe.com/c/vitamins-supplements/multivitamins/men-s-multivitamins?page=1')
links.append('https://www.vitaminshoppe.com/c/vitamins-supplements/multivitamins/men-s-multivitamins?page=2')
links.append('https://www.vitaminshoppe.com/c/vitamins-supplements/multivitamins/men-s-multivitamins?page=3')
        
        
x = scraping()
links2 = x.get_links(links)
d = x.scrape_data(links2)
x.write_to_csv(d)