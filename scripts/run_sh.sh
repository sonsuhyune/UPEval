# 실행 쉘파일 (run_main.sh) 200_ESConv_for_evalframe_wrole  200_AugESC_for_evalframe_wrole
FILE_NAME=200_ESConv_for_evalframe_wrole
MODEL_TYPE=gpt-3.5
DATA_TYPE=esc-eval
PROMPT=upeval
CUDA_VISIBLE_DEVICES=5 python3 main.py \
  --input_path data_for_UPEval/${FILE_NAME}.json \
  --model_type ${MODEL_TYPE} \
  --eval_turn 10 \
  --check_turn 1 \
  --data_type ${DATA_TYPE} \
  --prompt ${PROMPT}  \
  --output_path ./main_results/${MODEL_TYPE}_${FILE_NAME}_t.json



