set PYTHONPATH=src
::python ./train.py --model_name 117M --model_name 117M --dataset naruto-subtitles-merged.txt.npz --batch_size 1 --save_every 10000 --sample_every 1000 --run_name naruto
::python ./train.py --model_name 117M --model_name 117M --dataset monogatari-subtitles-merged.txt.npz --batch_size 1 --save_every 10000 --sample_every 1000 --run_name monogatari
python ./train.py --model_name 117M --model_name 117M --dataset overlord-vn-merged.txt.npz --batch_size 1 --save_every 10000 --sample_every 1000 --run_name overlord
::python ./train.py --model_name 117M --model_name 117M --dataset gutenberg-poetry-v001.txt.npz --batch_size 1 --save_every 10000 --sample_every 1000 --run_name gutenberg

::text generation works with this code:
::python src/generate_unconditional_samples.py --top_k 40 --temperature 0.9 --nsamples 2 --seed 0 --model_name monogatari

::interactive text generation
::python src/interactive_conditional_samples.py --top_k 40 --temperature 0.9  --seed 2000 --model_name monogatari

