#!/bin/bash

setup(){

#Workdir:
    export WORKDIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
    echo "setting WORKDIR=${WORKDIR}"

#General UPS setup
    . "/nusoft/app/externals/setup"

#Root5    
    setup -q debug:e2 -f Linux64bit+2.6-2.5 root v5_34_05

#DK2NU    
    setup -q debug:e5 -f Linux64bit+2.6-2.5 dk2nu v01_01_03
    export DK2NU_INC=${DK2NU}/include/dk2nu/tree
    export DK2NU_LIB=${DK2NU}/lib

}
setup
