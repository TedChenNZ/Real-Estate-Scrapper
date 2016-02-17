from lxml import html
import requests
import sys

def scrapeTrademe(url):
    page = requests.get(url)
    tree = html.fromstring(page.content)

    title = 'ListingTitle_title'
    location = 'ListingAttributes_AttributesRepeater_ctl01_ltHeaderRow'
    price = 'ListingTitle_classifiedTitlePrice'

    t = tree.get_element_by_id(title)
    l = tree.get_element_by_id(location)
    p = tree.get_element_by_id(price)

    t = t.text.strip()
    l = l.getnext().text.strip()
    p = p.text.strip()

    lst = [url, t, l, p]
    # lst = [s.replace(',', '') for s in lst]
    return "	".join(lst)

def scrapeRealestate(url):
    page = requests.get(url)
    tree = html.fromstring(page.content)

    title = '//*[@id="mainContent"]/div[1]/h1'
    location = '//*[@id="mainContent"]/div[1]/h3/span[1]'
    price = '//*[@id="mainContent"]/div[1]/h2'

    t = tree.xpath(title)
    l = tree.xpath(location)
    p = tree.xpath(price)

    t = t[0].text.strip()
    l = l[0].text.strip()
    p = p[0].text.strip()

    lst = [url, t, l, p]
    # lst = [s.replace(',', '') for s in lst]
    return "	".join(lst)

def parseUrl(url):
    if "trademe.co.nz" in url:
        try:
            return scrapeTrademe(url) + '\n'
        except:
            return url + "	" + "Error occurred - property may have expired\n"
    elif "realestate.co.nz" in url:
        try:
            return scrapeRealestate(url) + '\n'
        except:
            return url + "	" + "Error occurred - property may have expired\n"
    else:
        return url + "	" + "Unknown error occurred"
if (len(sys.argv) == 2):
    print(parseUrl(sys.argv[1]))
elif (len(sys.argv) > 2):
    f = open(sys.argv[1], 'r')
    o = open(sys.argv[2], 'w')
    urls = f.readlines()
    urls = [url.strip() for url in urls]
    # output = []
    for url in urls:
        if len(url.strip()) > 0:
            o.write(parseUrl(url))
else:
    print("Usage: input.txt output.txt")
