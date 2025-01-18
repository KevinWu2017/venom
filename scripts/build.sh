#!/bin/bash

GPU_CC=$(nvidia-smi --id=0 --query-gpu=compute_cap --format=csv,noheader)

if [ "$GPU_CC" = "8.0" ]; then
    CUDA_COMPUTE_CAPABILITY=80
elif [ "$GPU_CC" = "8.6" ]; then
    CUDA_COMPUTE_CAPABILITY=86
elif [ "$GPU_CC" = "8.9" ]; then
    CUDA_COMPUTE_CAPABILITY=89
elif [ "$GPU_CC" = "9.0" ]; then
    CUDA_COMPUTE_CAPABILITY=90
else
    echo "Unsupported GPU compute capability: $GPU_CC"
    exit 1
fi

mkdir -p build
cd build && {
  echo "Building venom"
  rm -rf *
  cmake .. -DCMAKE_BUILD_TYPE=Release -DCUDA_ARCHS="$CUDA_COMPUTE_CAPABILITY" -DBASELINE=OFF -DIDEAL_KERNEL=OFF -DOUT_32B=OFF
  make -j
}