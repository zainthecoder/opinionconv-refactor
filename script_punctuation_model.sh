#!/bin/bash
#SBATCH --partition=A40short
#SBATCH --time=0:10:00
#SBATCH --gpus=1
#SBATCH --ntasks=1
#SBATCH --output=/home/s28zabed/opinionconv-refactor/output.out

# Activate the environment
source myenv/bin/activate

# Run your script
python punctuation_model.py
