import subprocess
from setuptools import setup, find_packages, Extension
from torch.utils.cpp_extension import CppExtension, BuildExtension, CUDAExtension
from pybind11.setup_helpers import Pybind11Extension
import sys

def get_cuda_compute_capability():
    try:
        # 调用 nvidia-smi 获取 GPU 计算能力
        gpu_cc = subprocess.check_output(
            ["nvidia-smi", "--id=0", "--query-gpu=compute_cap", "--format=csv,noheader"],
            universal_newlines=True
        ).strip()

        # 根据计算能力设置 CUDA_COMPUTE_CAPABILITY
        if gpu_cc == "8.0":
            return "80"
        elif gpu_cc == "8.6":
            return "86"
        elif gpu_cc == "8.9":
            return "89"
        elif gpu_cc == "9.0":
            return "90"
        else:
            raise RuntimeError(f"Unsupported GPU compute capability: {gpu_cc}")
    except Exception as e:
        raise RuntimeError(f"Failed to detect GPU compute capability: {e}")

CUDA_COMPUTE_CAPABILITY = get_cuda_compute_capability()

setup(
    name='spatha',
    version='0.0.1',
    description='Custom library for Sparse Tensor Cores',
    author='Roberto L. Castro',
    author_email='roberto.lopez.castro@udc.es',
    ext_modules=[
            CUDAExtension('spatha',
                              ['spatha_mod/block_sparse/api/spatha.cu'],
                              extra_compile_args={'cxx':[], 'nvcc':[f"-arch=sm_{CUDA_COMPUTE_CAPABILITY}", '--ptxas-options=-v', '-lineinfo', '-DV_64']})
                  ],
    cmdclass={'build_ext': BuildExtension},
    install_requires=['torch']
)