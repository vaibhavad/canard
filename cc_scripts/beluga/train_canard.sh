#!/bin/bash
#SBATCH --account=rrg-bengioy-ad
#SBATCH --gres=gpu:1
#SBATCH --mem=32G
#SBATCH --time=05:00:00
#SBATCH --cpus-per-task=10
#SBATCH --job-name=train_canard
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

cd $HOME/canard

python FormatSeq2Seq.py $SCRATCH/canard/data/seq2seq/release/train.json train $SCRATCH/canard/data/seq2seq --spacy True
python FormatSeq2Seq.py $SCRATCH/canard/data/seq2seq/release/dev.json dev $SCRATCH/canard/data/seq2seq --spacy True
python FormatSeq2Seq.py $SCRATCH/canard/data/seq2seq/release/test.json test $SCRATCH/canard/data/seq2seq --spacy True

DATA_DIR=$SCRATCH/canard/data/seq2seq
MODEL_PATH=$SCRATCH/canard/models/canard_models/model
GLOVE_DIR=$SCRATCH/canard/glove

cd $HOME/OpenNMT-py

python preprocess.py -train_src $DATA_DIR/train-src.txt \
                     -train_tgt $DATA_DIR/train-tgt.txt \
                     -valid_src $DATA_DIR/dev-src.txt \
                     -valid_tgt $DATA_DIR/dev-tgt.txt \
                     -save_data $MODEL_PATH \
                     -src_seq_length 10000 \
                     -tgt_seq_length 10000 \
                     -dynamic_dict \
                     -share_vocab \
                     -shard_size 100000

./tools/embeddings_to_torch.py -emb_file_both "$GLOVE_DIR/glove.840B.300d.txt" \
                               -dict_file "$MODEL_PATH.vocab.pt" \
                               -output_file "$MODEL_PATH/embeddings"

python train.py -save_model $MODEL_PATH \
                -data $MODEL_PATH \
                -copy_attn \
                -global_attention mlp \
                -word_vec_size 300 \
                -pre_word_vecs_enc "$MODEL_PATH/embeddings.enc.pt" \
                -pre_word_vecs_dec "$MODEL_PATH/embeddings.dec.pt" \
                -rnn_size 512 \
                -layers 1 \
                -encoder_type brnn \
                -train_steps 200000 \
                -max_grad_norm 2 \
                -dropout 0. \
                -batch_size 16 \
                -valid_batch_size 16 \
                -optim adagrad \
                -learning_rate 0.15 \
                -adagrad_accumulator_init 0.1 \
                -reuse_copy_attn \
                -copy_loss_by_seqlength \
                -bridge \
                -seed 777 \
                -world_size 1 \
                -gpu_ranks 0

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
                        -verbose \
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
