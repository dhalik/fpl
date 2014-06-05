#include "bond.h"
#include "period.h"
#include <iostream>

int main(){
    Bond b(0.05, 1000, YEARLY, 10);
    std::cout << b.price(0.07);
}
