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

## prompt
<table>
<tr>
<td>prompt id</td>
<td>type</td>
<td>prompt text</td>
</tr>
<tr>
<td>13</td>
<td>COT</td>
<td>Let's think step by step.</td>
</tr>
<tr>
<td>324</td>
<td>PS</td>
<td>Let's first understand the problem and devise a plan to solve the problem. Then, let's carry out the plan to solve the problem step by step.</td>
</tr>
</table>