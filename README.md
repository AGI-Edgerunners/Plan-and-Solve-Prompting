# Plan-and-Solve-Prompting
Improving Zero-Shot Chain-of-Though Reasoning in Large Language Models

## run experiment
Set an api-key of OpenAI API in the file ```apikeys.json```
```shell
python main.py --prompt_id 324 \
--dataset SVAMP \
--engine text-davinci-003 \
--learning_type zero_shot
```

## run experiment with threads
Set 8 different api-keys of OpenAI API in the file ```apikeys.json```
```shell
python main_threads.py --prompt_id 324 \
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
<tr>
<td>325</td>
<td>PS+</td>
<td>Let's first understand the problem, extract relevant variables and their corresponding numerals, and devise a plan. Then, let's carry out the plan, calculate intermediate variables (pay attention to correct numeral calculation and commonsense), solve the problem step by step, and show the answer.</td>
</tr>
<tr>
<td>326</td>
<td>PS+</td>
<td>Let's first understand the problem, extract relevant variables and their corresponding numerals, and devise a complete plan. Then, let's carry out the plan, calculate intermediate variables (pay attention to correct numerical calculation and commonsense), solve the problem step by step, and show the answer.</td>
</tr>
<tr>
<td>333</td>
<td>PS+</td>
<td>Let's devise a plan and solve the problem step by step.</td>
</tr>
<tr>
<td>347</td>
<td>PS+</td>
<td>Let's first understand the problem and devise a complete plan. Then, let\'s carry out the plan and reason problem step by step. Every step answer the subquestion, \"does the person flip and what is the coin's current state?\". According to the coin's last state, give the final answer (pay attention to every flip and the coin’s turning state).</td>
</tr>
<tr>
<td>350</td>
<td>PS+</td>
<td>Let's first understand the problem, extract relevant variables and  their corresponding numerals, and make a complete plan.Then,  let's carry out the plan, calculate intermediate variables (pay attention to correct numerical calculation and commonsense), solve the problem step by step, and show the answer.</td>
</tr>
<tr>
<td>356</td>
<td>PS+</td>
<td>Let's first understand the problem, extract relevant variables and  their corresponding numerals, and make a complete plan.Then,  let's carry out the plan, calculate intermediate variables (pay attention to correct numerical calculation and commonsense), solve the problem step by step, and show the answer.</td>
</tr>
</table>