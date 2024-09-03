#!/bin/bash
#SBATCH --partition=A100devel
#SBATCH --gpus=1
#SBATCH --ntasks=1
#SBATCH -o "/home/s28zabed/opinionconv-refactor/output.out"

python UPDATED_MAIN.py