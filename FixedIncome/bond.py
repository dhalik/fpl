from __future__ import division
from numpy import linspace

class Bond:
    """Basic bond object"""
    def __init__(self, faceValue, coupon, maturity):
        """
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
        annuity = self.coupon / rate * (1 - 1 / ((1 + rate) ** self.maturity))
        fv = self.faceValue / (1 + rate) ** self.maturity
        return annuity + fv


def main():
    bond = Bond(1000, 0.08, 10)
    template = "For rate {}, price is {}"
    for r in xrange(1, 13):
        print template.format(r/100, bond.price(r/100))

if __name__ == "__main__":
    main()
