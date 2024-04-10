#!/bin/bash
mkdir -p build
cd build && {
  echo "Building venom"
  rm -rf *
  cmake .. -DCMAKE_BUILD_TYPE=Release -DCUDA_ARCHS="89" -DBASELINE=OFF -DIDEAL_KERNEL=OFF -DOUT_32B=OFF
  make -j
}