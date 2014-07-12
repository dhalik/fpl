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

    def getInfo(self):
        """
            Internal function to get financial information from yahoo finance website.
            This function will grab current stock price, and other generic information.
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
        self.industryString = y.execute(query5,  env = yqlEnv)

        #grab relevent data
        self.industry = self.industryString.rows[0].get('Industry')
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
    s = "gme"
    a = Equity(s)

if __name__ == "__main__":
    main()
