#ifndef __BOND__H__
#define __BOND__H__

#include "period.h"

class Bond{
    private:
        float couponRate;
        float payment;
        float faceValue;
        int numPeriods;
        Period compounding;

    public:
        //Constructed with couponRate,facevalue
        Bond(float, float, Period, int);
        //price the bond given a market rate
        float price(float);

        //getters and Setters
        float getPayment();
        float getFaceValue();
        float getCouponRate();
};

#endif
