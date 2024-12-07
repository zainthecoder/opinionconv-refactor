#!/bin/bash
#SBATCH --partition=A40short
#SBATCH --time=6:40:00
#SBATCH --gpus=1
#SBATCH --ntasks=1
#SBATCH --output=/home/s28zabed/opinionconv-refactor/output_neg.out

# Activate the environment
source myenv/bin/activate

# Run your script
python generating_qa_op_pairs.py
