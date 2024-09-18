#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --gpus=1
#SBATCH --time=00:10:00
#SBATCH --job-name=jupyter-notebook
#SBATCH -o "/home/s28zabed/opinionconv-refactor/output.out"

python3 Sfsdfsdfsfcript.py


