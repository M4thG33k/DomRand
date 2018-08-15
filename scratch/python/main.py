import json
import urllib2
from pyquery import PyQuery as pq
import re

# d = pq(url="https://dominionstrategy.com/all-cards/")
d = pq(filename="cards.html")

data = dict()
tables = d("table")
headers = d("h2")

typeSplit = re.compile(u"[\u2013\-]")
hlineReplace = re.compile(u"(\u2014)+-?")


def handleCategory(index):
    def handleRow(jndex):
        row = rows.eq(jndex).find("td")
        card = dict()
        card["name"] = row.eq(0).text()
        card["types"] = map(lambda x: x.strip(), re.split(typeSplit, row.eq(1).text()))
        # card["types"] = map(lambda x: x.strip(), row.eq(1).text().split(u'\u2013'))
        cost = row.eq(2).html()
        if cost:
            cost = cost.replace(u"\u25c9", " P").replace("/", " ").replace("*", " AST").replace("+", " OVER").split(" ")
            realCost = dict()
            for c in cost:
                c = c.strip()
                if c:
                    if c[0] == "$":
                        realCost["coin"] = int(c[1:])
                    elif c[-1] == "D":
                        realCost["debt"] = int(c[:-1])
                    elif c == "P":
                        realCost["potion"] = 1
                    elif c == "AST":
                        realCost["conditional"] = True
                    elif c == "OVER":
                        realCost["canOverpay"] = True
                    else:
                        print "ERROR", c
            card["cost"] = realCost
            card["desc"] = re.sub(re.compile(" +"), " ", re.sub(hlineReplace, " ",
                                                                row.eq(3).text().replace("\n", " ").replace(u"\u25c9",
                                                                                                            "{{POTION}}").replace(
                                                                    u"\u2013", " ")))
        cards.append(card)

    cards = []
    data[headers.eq(index).text()] = cards

    rows = tables.eq(index).find("tr")
    rows.each(handleRow)


headers.each(handleCategory)

with open("cards.json", 'w') as f:
    f.write(json.dumps(data))
