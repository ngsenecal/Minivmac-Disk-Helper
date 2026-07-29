#!/bin/sh

# Minivmac build for Minivmac Disk Helper

if [ ! -x ./setup_t ]; then
	gcc -o setup_t setup/tool.c
fi

# run setup tool to generate makefile generator
./setup_t -maintainer "neilsenecalwork@gmail.com" \
        -homepage "https://github.com/ngsenecal" \
        -n "minivmac-disk-helper-ver" \
        -e bgc \
        -t lx64 \
        -m II \
        -hres 512 -vres 342 -depth 1 \
        -magnify 1 \
        -mf 2 \
        -sound 1 \
        -sony-sum 1 -sony-tag 1 \
        -speed z -ta 2 -em-cpu 2 -mem 8M \
        -chr 0 -drc 1 -sss 4 \
        -fullscreen 1 \
        -var-fullscreen 1 \
        -iid 1 \
        -drives 2 \
        -km Option Command -km Control Option -km F5 CM\
        -api sd2 \
        > setup.sh

# generate makefile and build
bash -x ./setup.sh
make clean
make -j $(nproc)
