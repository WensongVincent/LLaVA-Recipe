#!/bin/bash
# sh finetune.sh [7b/13b] [version] 

if [$1 -eq 7b]
then
    projector=llava7b-mm_projector.bin
fi

if [$1 -eq 13b]
then
    projector=llava13b-mm_projector.bin
fi

deepspeed llava/train/train_mem.py \
    --deepspeed ./scripts/zero3.json \
    --lora_enable True --lora_r 128 --lora_alpha 256 --mm_projector_lr 2e-5 \
    --model_name_or_path lmsys/vicuna-$1-v1.5 \
    --version v1 \
    --data_path ./Dataset/dataset-200m/val.json \
    --image_folder ./dataset/dataset-200m/images \
    --vision_tower openai/clip-vit-large-patch14-336 \
    --mm_projector_type mlp2x_gelu \
    --pretrain_mm_mlp_adapter ./mm_projectors/$projector \
    --mm_vision_select_layer -2 \
    --mm_use_im_start_end False \
    --mm_use_im_patch_token False \
    --bf16 True \
    --output_dir ./checkpoints/finetune/version-$1-$2 \
    --num_train_epochs 1 \
    --per_device_train_batch_size 8 \
    --per_device_eval_batch_size 4 \
    --gradient_accumulation_steps 2 \
    --evaluation_strategy "no" \
    --save_strategy "steps" \
    --save_steps 50000 \
    --save_total_limit 1 \
    --learning_rate 2e-5 \
    --weight_decay 0. \
    --warmup_ratio 0.03 \
    --lr_scheduler_type "cosine" \
    --logging_steps 1 \
    --tf32 True \
    --model_max_length 2048 \
    --gradient_checkpointing True \
    --lazy_preprocess True \
    --dataloader_num_workers 4 \
    --report_to wandb
