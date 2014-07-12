import urllib2
from BeautifulSoup import BeautifulSoup

class Equity:
    def __init__(self, ticker):
        """
            Equity Object.
            @param ticker - The ticker for the stock. i.e. AAPL
        """
        self.ticker = ticker
        self.getInfo()

    def getInfo(self):
        """
            Internal function to get financial information from yahoo finance website.
            This function will grab current stock price, and other generic information.
        """
        url = "https://ca.finance.yahoo.com/q?s="+self.ticker
        response = urllib2.urlopen(url)
        soup = BeautifulSoup(response.read())
        ticker_tag = "yfs_l84_" + self.ticker
        self.price = soup.find("span",id=ticker_tag).text


    def __str__(self):
        return str(self.price)

def main():
    securities = ["aapl", "goog", "tsla", "spy"]
    for s in securities:
        a = Equity(s)
        print "Price for " + s + " is " + str(a)

if __name__ == "__main__":
    main()
