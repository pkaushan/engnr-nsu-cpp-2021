#include "Hashfunc.h"
#include <iostream>


uint64_t sum64( std::istream &file ) {
    uint64_t sum, end, block;
    sum = 0;
    block = 0;
    end = 0;
    unsigned char sign;
    while (file.read((char*) &sign, sizeof(unsigned char)))
    { //сканируем символы
        if (end == 8){ //проверка на законченность блока
            sum += block;
            block = 0;
            end = 0;
        }
        //считаем сумму
        block = block << 8;
        block += sign;
        end++;
    }
    sum = sum + block;
    return sum;
}

uint32_t adler32( std::istream &file ){
    int MOD_ADLER = 65521;
    uint32_t a, b;
    a = 1;
    b = 0;
    unsigned char index;
    while( file.read((char *)(&index), sizeof(unsigned char)) )
    {
        a = (a + (index)) % MOD_ADLER; //самое большое простое число меньше 2^16
        b = (b + a) % MOD_ADLER;
    }
    return (b << 16) | a;
}
