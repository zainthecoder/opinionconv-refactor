#!/bin/bash
#SBATCH --partition=A40short
#SBATCH --time=0:10:00
#SBATCH --gpus=1
#SBATCH --ntasks=1
#SBATCH --output=/home/s28zabed/opinionconv-refactor/output.out

# Initialize Conda for the shell (necessary if not already done)
source ~/.bashrc


# Activate the environment
conda activate myenv

# Run your script
python MAIN.py
