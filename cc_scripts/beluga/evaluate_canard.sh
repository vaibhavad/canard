#!/bin/bash
#SBATCH --account=rrg-bengioy-ad
#SBATCH --gres=gpu:1
#SBATCH --mem=32G
#SBATCH --time=01:00:00
#SBATCH --cpus-per-task=10
#SBATCH --job-name=evaluate_canard
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

DATA_DIR=$SCRATCH/canard/data/seq2seq
MODEL_PATH=$SCRATCH/canard/models/canard_models/model
GLOVE_DIR=$SCRATCH/canard/glove
PREDICTION_DIR=$SCRATCH/canard/predictions/canard_predictions

for name in dev test
do
    python translate.py -gpu 0 \
                        -batch_size 20 \
                        -beam_size 10 \
                        -model "$MODEL_PATH"_step_200000.pt \
                        -src $DATA_DIR/"$name"-src.txt \
                        -output "$PREDICTION_DIR/"$name".txt" \
                        -min_length 3 \
                        -stepwise_penalty \
                        -coverage_penalty summary \
                        -beta 5 \
                        -length_penalty wu \
                        -alpha 0.9 \
                        -block_ngram_repeat 3 
done

echo "Dev - BLEU"
perl $HOME/canard/multi-bleu-detok.perl "$DATA_DIR/dev-tgt.txt" < "$PREDICTION_DIR/dev.txt"

echo "Test - BLEU"
perl $HOME/canard/multi-bleu-detok.perl "$DATA_DIR/test-tgt.txt" < "$PREDICTION_DIR/test.txt"
