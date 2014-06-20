from __future__ import division
from numpy import linspace

class Bond:
    def __init__(self, faceValue, coupon, maturity):
        """
            Basic bond object,
            @param faceValue - The face value of the bond
            @param coupon    - The coupon rate on the bond
            @param maturity  - The number of years until maturity of the bond
        """
        self.couponRate = coupon
        self.faceValue = faceValue
        self.coupon = self.couponRate*faceValue
        self.maturity = maturity

    def price(self, rate):
        """
        Calculate the price of a bond using a given rate
        @param rate - The market rate to price the bond.
        @return - The price of a bond

        """
        annuity = self.coupon/rate*(1-1/((1+rate)**self.maturity))
        fv = self.faceValue / (1+rate)**self.maturity
        return annuity + fv


def main():
    a = Bond(1000,0.08,10)
    for r in linspace(0,0.1,0.01):
        print a.price(i)

if __name__ == "__main__":
    main()