#include "bond.h"
#include <cmath>

Bond::Bond(float couponRate, float faceValue, Period compounding, int numPeriods){
    this->numPeriods = numPeriods;
    this->couponRate = couponRate / (int)compounding;
    this->compounding = compounding;
    this->faceValue = faceValue;
    payment = couponRate * faceValue;
}

float Bond::price(float r){
    float discountFactor = pow((1+r), numPeriods);
    float presentValueCoupon = (payment * (1 - 1/discountFactor))/r ;
    float presentValueFace = faceValue/discountFactor;
    return presentValueCoupon + presentValueFace;
}

float Bond::getPayment(){ return payment; }
float Bond::getFaceValue(){ return faceValue; }
float Bond::getCouponRate(){ return couponRate; }
