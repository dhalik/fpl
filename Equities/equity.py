import urllib2
import yql
import json
import constants

class Equity:
    def __init__(self, ticker):
        """
            Equity Object.
            @param ticker - The ticker for the stock. i.e. AAPL
        """
        self.ticker = ticker
        self.getInfo()
        self.getCompetitorData()

    def industryBasedPrice(self, industryStats, stat):
        """
            Internal Generic to calcualte price by company stats
        """
        averagePE = sum(industryStats)/float(len(industryStats))
        maxPE = max(industryStats)
        minPE = min(industryStats)
        companyVal = float(self.keystats.rows[0].get(stat).get('content'))
        return [minPE*companyVal, averagePE*companyVal, maxPE*companyVal]

    def industryPricebyPE(self):
        """
            Return computed stock price based on diluted EPS for company.
            returns a list of [min, average, max]
        """
        return self.industryBasedPrice(self.industryPE, "DilutedEPS")

    def industryPricebyBook(self):
        """
            Return computed stock price based on diluted EPS for company.
            returns a list of [min, average, max]
        """
        return self.industryBasedPrice(self.industryPBook, "BookValuePerShare")

    def industryEVbyRevenues(self):
        """
            Return computed stock price based on diluted EPS for company.
            returns a list of [min, average, max]
        """
        EV = self.industryBasedPrice(self.industryEVRevenues, "Revenue")
        return EV

    def industryEVbyEBIT(self):
        """
            Return computed stock price based on diluted EPS for company.
            returns a list of [min, average, max]
        """
        return self.industryBasedPrice(self.industryEVEBIT, "EBITDA")

    def getCompetitorData(self):
        self.industryPE = []
        self.industryEVRevenues = []
        self.industryEVEBIT = []
        self.industryPBook = []
        for comp in self.otherCompanyData.rows:
            try:
                pe = comp.get('ForwardPE').get('content')
                evrev = comp.get('EnterpriseValueRevenue').get('content')
                evebit = comp.get('EnterpriseValueEBITDA').get('content')
                pbook = comp.get('PriceBook').get('content')
            except AttributeError:
                pass

            try:
                self.industryPE.append(float(pe))
            except ValueError:
                pass
            try:
                self.industryPBook.append(float(pbook))
            except ValueError:
                pass
            try:
                self.industryEVEBIT.append(float(evebit))
            except ValueError:
                pass
            try:
                self.industryEVRevenues.append(float(evrev))
            except ValueError:
                pass

    def getInfo(self):
        """
            Internal function to get financial information from yahoo finance website.
            This function will grab current stock price, and other generic information for the
            security given by the ticker in the constructor.

            Data Collected:
                self.quote is quote information for the stock
                self.keystats is the the key stats defined in yql
                self.balancesheet is the balance sheet
                self.incomestatement is the income statement
                self.cashflow is the cashflow statement
                self.otherComapnyData is a list of all of the data for competitor companies
        """

        y = yql.Public()
        yqlEnv = "store://datatables.org/alltableswithkeys"

        #define queries used for data gathering
        query = "SELECT * FROM yahoo.finance.quote WHERE symbol in(\"" + self.ticker + "\")"
        query2 = "SELECT * FROM yahoo.finance.balancesheet WHERE symbol =\"" + self.ticker + "\""
        query3 = "SELECT * FROM yahoo.finance.incomestatement WHERE symbol =\"" + self.ticker + "\""
        query4 = "SELECT * FROM yahoo.finance.keystats WHERE symbol =\""+self.ticker+"\""
        query5 = "SELECT Industry FROM yahoo.finance.stocks WHERE symbol =\"" + self.ticker + "\""

        #download data using yql. Possibly add cashflow
        self.quote = y.execute(query, env=yqlEnv)
        self.balancesheet = y.execute(query2, env=yqlEnv)
        self.incomestatement = y.execute(query3, env=yqlEnv)
        self.keystats = y.execute(query4, env = yqlEnv)
        industryString = y.execute(query5,  env = yqlEnv)

        #grab relevent data
        self.industry = industryString.rows[0].get('Industry')
        self.price = self.quote.rows[0].get('LastTradePriceOnly')
        self.industryId = constants.industry[self.industry]

        #grab relevant competitor data
        competitors = "SELECT * FROM yahoo.finance.industry WHERE id="+str(self.industryId)
        res = y.execute(competitors, env=yqlEnv)

        self.competitorList = [];
        for row in res.rows[0].get('company'):
            if type(row) is dict:
                self.competitorList.append(row.get('symbol'))
        competitorString = ",".join('"{0}"'.format(w) for w in self.competitorList)

        competitorsListQuery = "SELECT * FROM yahoo.finance.keystats WHERE symbol in("+competitorString+")"
        self.otherCompanyData = y.execute(competitorsListQuery, env=yqlEnv)

def main():
    a = Equity("DRI")
    priceByEPS = a.industryPricebyPE()
    priceByBook = a.industryPricebyBook()
    EVbyRev = a.industryEVbyRevenues()
    EVbyEBITDA = a.industryEVbyEBIT()

    print "min price by PE " + str(priceByEPS[0])
    print "max price by PE " + str(priceByEPS[1])
    print "average price by PE " + str(priceByEPS[2])

    print "min price by Book " + str(priceByBook[0])
    print "max price by Book " + str(priceByBook[1])
    print "average price by Book " + str(priceByBook[2])

    print "min EV by Rev " + str(EVbyRev[0])
    print "max EV by Rev " + str(EVbyRev[1])
    print "average EV by Rev " + str(EVbyRev[2])

    print "min EV by EBITDA" + str(EVbyEBITDA[0])
    print "max EV by EBITDA " + str(EVbyEBITDA[1])
    print "average EV by EBITDA" + str(EVbyEBITDA[2])

if __name__ == "__main__":
    main()
