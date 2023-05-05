# Plan-and-Solve-Prompting
Improving Zero-Shot Chain-of-Though Reasoning in Large Language Models

## run experiment
Set an api-key of OpenAI API in the file ```apikeys.json```
```shell
python main.py --prompt_id 310 \
--dataset SVAMP \
--engine text-davinci-003 \
--learning_type zero_shot
```

## run experiment with threads
Set 8 different api-keys of OpenAI API in the file ```apikeys.json```
```shell
python main.py --prompt_id 310 \
--dataset SVAMP \
--engine text-davinci-003 \
--learning_type zero_shot
```