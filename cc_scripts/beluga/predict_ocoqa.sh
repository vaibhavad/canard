#!/bin/bash
#SBATCH --account=rrg-bengioy-ad
#SBATCH --gres=gpu:1
#SBATCH --mem=32G
#SBATCH --time=2:00:00
#SBATCH --cpus-per-task=10
#SBATCH --job-name=evaluate_qrecc
#SBATCH --output=/scratch/vaibhav/canard/logs/%x-%j.out
#SBATCH --error=/scratch/vaibhav/canard/logs/%x-%j.err

module load python/3.6
module load StdEnv/2020
module load scipy-stack/2020b
virtualenv --no-download $SLURM_TMPDIR/env
source $SLURM_TMPDIR/env/bin/activate
pip install --no-index --upgrade pip

pip install --no-index --find-links $HOME/python_wheels 'torchtext==0.4.0'
pip install --no-index --find-links $HOME/python_wheels 'waitress==2.0.0'
pip install --no-index spacy
pip install --no-index configargparse

cd $HOME/OpenNMT-py
pip install . --no-index

DATA_DIR=$SCRATCH/canard/data/ocoqa
PREDICTION_DIR=$SCRATCH/canard/predictions/ocoqa_predictions
name=ocoqa

MODEL_PATH=$SCRATCH/canard/models/qrecc_models/model
python translate.py -gpu 0 \
                    -batch_size 20 \
                    -beam_size 10 \
                    -model "$MODEL_PATH"_step_400000.pt \
                    -src $DATA_DIR/"$name"-src.txt \
                    -output "$PREDICTION_DIR/"$name"-qrecc.txt" \
                    -min_length 3 \
                    -stepwise_penalty \
                    -coverage_penalty summary \
                    -beta 5 \
                    -length_penalty wu \
                    -alpha 0.9 \
                    -block_ngram_repeat 3 

MODEL_PATH=$SCRATCH/canard/models/canard_models/model
python translate.py -gpu 0 \
                    -batch_size 20 \
                    -beam_size 10 \
                    -model "$MODEL_PATH"_step_200000.pt \
                    -src $DATA_DIR/"$name"-src.txt \
                    -output "$PREDICTION_DIR/"$name"-canard.txt" \
                    -min_length 3 \
                    -stepwise_penalty \
                    -coverage_penalty summary \
                    -beta 5 \
                    -length_penalty wu \
                    -alpha 0.9 \
                    -block_ngram_repeat 3 
