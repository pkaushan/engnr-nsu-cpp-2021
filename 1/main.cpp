#include <fstream>
#include <iostream>
#include <cstring>
#include <string>
#include "Hashfunc.h"


int main(int argc, char *argv[]) {
    std::ifstream file;
    std::string helper, path, mode;
    helper = "Instruction: ./helper -m <mode> <filename> or ./helper <filename> -m <mode>. \n<mode>: adler32 or sum64";
    if (argc == 2) {
        if (strcmp(argv[1], "-h") == 0){
            std::cout << helper << std::endl;
            return 0;
        }
        else {
            std::cerr << " Error 1 " << std::endl << helper << std::endl;
            return 1;
        }
    }
    else if(argc == 4) {
        if((strcmp(argv[1], "-m") == 0)&&((strcmp(argv[2],"adler32") == 0)||(strcmp(argv[2],"sum64") == 0))){
            mode = argv[2];
            path = argv[3];
        }
        else if((strcmp(argv[2], "-m") == 0)&&((strcmp(argv[3],"adler32") == 0)||(strcmp(argv[3],"sum64") == 0))){
            mode = argv[3];
            path = argv[1];
        }
        else {
            std::cerr << " Error 2" << std::endl << helper << std::endl;
            return 1;
        }
    }
    else {
        std::cerr << " Error 3" << std::endl << helper << std::endl;
        return 1;
    }

    file.open(path, std::ios_base::binary);
    if(!(file.is_open())){
        std::cerr << " Error 4" << std::endl << helper << std::endl;
        return 1;
    }

    if(mode == "adler32"){
        std::cout << std::hex << adler32(file) << std::endl;
    }
    else{
        std::cout << std::hex << sum64(file) << std::endl;
    }
    return 0;
}