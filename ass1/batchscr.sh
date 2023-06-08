#!/bin/bash

#SBATCH --job-name=wiki_search
#SBATCH -c 30
#SBATCH -t 20:00:00
#SBATCH --gres=gpu:2
#SBATCH --mem-per-cpu=2G
#SBATCH --output trainer.log



module add cuda/8.0
module add cudnn/7-cuda-8.0
export CUDA_VISIBLE_DEVICES=0,1
source activate nlp
python3 neural_model.py
#echo "Activating virtualenv"
#source ~/fenv/bin/activate
#cd /scratch/devesh.marwah/xl-sum-master/seq2seq/
# bash index.sh data.xml indexfolder/ invertedindex_stats.xml
#ls
# python3 pipeline.py  --model_name_or_path "google/mt5-base" --data_dir "../../XLSum_complete_v2.0" --output_dir "../../XLSum_output"  --lr_scheduler_type="transformer"  --learning_rate=1  --warmup_steps 5000  --weight_decay 0.01   --per_device_train_batch_size=2  --gradient_accumulation_steps=16   --max_steps 50000 --save_steps 5000  --evaluation_strategy "no"  --logging_first_step  --adafactor  --label_smoothing_factor 0.1  --upsampling_factor 0.5  --do_train

#pyton3 inf.py



