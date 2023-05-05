import json

from config import args


def create_demo_text():
    if args.demo_path == 'demos/svamp.json' or args.demo_path == 'demos/svamp_6.json' or args.demo_path == 'demos/gsm8k_6.json' \
            or args.demo_path == 'demos/svamp_8_6.json' or args.demo_path == 'demos/svamp_4.json' or args.demo_path == 'demos/svamp_2.json' \
            or args.demo_path == 'demos/auto_svamp_prompt/svamp_2prompt.json' or args.demo_path == 'demos/auto_svamp_prompt/gsm8k_2prompt.json':
        x, z, y = [], [], []
        with open(args.demo_path, encoding="utf-8") as f:
            json_data = json.load(f)
            json_data = json_data["demo"]
            for line in json_data:
                x.append(line["question"])
                z.append(line["rationale"])
                y.append(line["pred_ans"])
        index_list = list(range(len(x)))
        demo_text = ""
        for i in index_list:
            demo_text += x[i] + " " + z[i] + " " + \
                         args.direct_answer_trigger_for_fewshot + " " + y[i] + ".\n\n"
    elif args.demo_path == 'demos/aqua.json':
        x, y, z, k = [], [], [], []
        with open(args.demo_path, encoding="utf-8") as f:
            json_data = json.load(f)
            json_data = json_data["demo"]
            for line in json_data:
                x.append(line['question'])
                y.append(line['answer_choice'])
                z.append(line['rationale'])
                k.append(line['pred_ans'])
            index_list = list(range(len(x)))
            demo_text = ""
            for i in index_list:
                demo_text += x[i] + ' ' + y[i] + '\n' + \
                             z[i] + args.direct_answer_trigger_for_fewshot + ' ' + k[i] + ".\n\n"
    elif args.demo_path == 'demos/commonsenseqa.json':
        x, y, z, k = [], [], [], []
        with open(args.demo_path, encoding="utf-8") as f:
            json_data = json.load(f)
            json_data = json_data["demo"]
            for line in json_data:
                x.append(line['question'])
                y.append(line['answer_choice'])
                z.append(line['rationale'])
                k.append(line['pred_ans'])
            index_list = list(range(len(x)))
            demo_text = ""
            for i in index_list:
                demo_text += x[i] + ' ' + y[i] + '\n' + \
                             z[i] + ' So the answer is' + ' ' + k[i] + ".\n\n"
    elif args.demo_path == 'demos/strategyqa.json':
        x, z, y = [], [], []
        with open(args.demo_path, encoding="utf-8") as f:
            json_data = json.load(f)
            json_data = json_data["demo"]
            for line in json_data:
                x.append(line["question"])
                z.append(line["rationale"])
                y.append(line["pred_ans"])
        index_list = list(range(len(x)))
        demo_text = ""
        for i in index_list:
            demo_text += x[i] + " " + z[i] + ' So the answer is' + " " + y[i] + ".\n\n"
    elif args.demo_path == 'demos/coin_flip.json':
        x, z, y = [], [], []
        with open(args.demo_path, encoding="utf-8") as f:
            json_data = json.load(f)
            json_data = json_data["demo"]
            for line in json_data:
                x.append(line["question"])
                z.append(line["rationale"])
                y.append(line["pred_ans"])
        index_list = list(range(len(x)))
        demo_text = ""
        for i in index_list:
            demo_text += x[i] + " " + z[i] + ' So the answer is' + " " + y[i] + ".\n\n"
    elif args.demo_path == 'demos/last_letters.json':
        x, z, y = [], [], []
        with open(args.demo_path, encoding="utf-8") as f:
            json_data = json.load(f)
            json_data = json_data["demo"]
            for line in json_data:
                x.append(line["question"])
                z.append(line["rationale"])
                y.append(line["pred_ans"])
        index_list = list(range(len(x)))
        demo_text = ""
        for i in index_list:
            demo_text += x[i] + " " + z[i] + ' The answer is' + " " + y[i] + ".\n\n"
    else:
        pass
    return demo_text


Few_Shot_Demo_Folder = 'few_shot_demos/'

prompt_13 = "Let's think step by step."

prompt_310 = 'Extract variables and their corresponding numerals first. Then solve the problem step by step.'
prompt_311 = 'Extract objects ans their corresponding numerals first. Then solve the problem step by step.'
prompt_312 = 'Extract variables and their corresponding numerals first and then solve the problem step by step.'
prompt_313 = 'Extract variables and assign their corresponding numerals to these variables first and then solve the ' \
             'problem step by step. '
prompt_314 = 'Step 1: Extract variables and assign their corresponding numerals to these variables;\nStep 2: Capture ' \
             'relations among variables and state transitions;\nStep 3: Solve the problem step by step. '
prompt_315 = 'Step 1: Extract variables and assign their corresponding numerals to these variables;\nStep 2: Capture the ' \
             'variables\' changes;\nStep 3: Solve the problem step by step. '
prompt_316 = 'Step 1: Extract variables and their corresponding numerals;\nStep 2: Capture the variables\' ' \
             'changes;\nStep 3: Solve the problem step by step. '

prompt_321 = 'Firstly, extract variables and their corresponding numerals. Then, calculate intermediate variables. ' \
             'Finally, solve the problem step by step. '
prompt_322 = 'Firstly, extract variables and their corresponding numerals. Then, calculate intermediate variables. ' \
             'Finally, solve the problem step by step. '
prompt_323 = 'Firstly, extract relevant variables, memorize the change of these variables, and update them. Then, ' \
             'solve the problem step by step. '
prompt_324 = "Let's first understand the problem and devise a plan to solve the problem. " \
             "Then, let's carry out the plan to solve the problem step by step."
prompt_325 = 'Let\'s first understand the problem, extract relevant variables and their corresponding numerals, and devise a plan. ' \
             'Then, let\'s carry out the plan, calculate intermediate variables (pay attention to correct numeral calculation and commonsense), solve the problem step by step, and show the answer. '
prompt_326 = 'Let\'s first understand the problem, extract relevant variables and their corresponding numerals, and devise a complete plan.' \
             'Then, let\'s carry out the plan, calculate intermediate variables (pay attention to correct numerical calculation and commonsense), solve the problem step by step, and show the answer.'
prompt_327 = 'Let\'s first understand the problem, extract relevant variables and their corresponding numerals, and devise a complete plan. ' \
             'Then, let\'s carry out the plan, calculate intermediate variables (pay attention to correct numerical calculation and commonsense), solve the problem step by step, and show the answer.'
prompt_328 = 'Let\'s first understand the problem, extract relevant variables and their corresponding numerals, and devise a complete plan.Then, let\'s carry out the plan, calculate intermediate variables (pay attention to the correctness of the calculation and common sense), solve the problem step by step, and show the answer.'
prompt_329 = 'Let\'s first understand the problem and devise a plan to solve the problem.Then, let\'s carry out the plan by solving the problem step by step.'
prompt_330 = 'Let\'s first understand the problem, extract relevant correct variables and their correct corresponding numerals, and devise a complete plan. Then, let\'s carry out the plan, calculate intermediate variables included extracted variables(pay attention to correct numerical calculation and commonsense), solve the problem by single equations, and show the answer.'
prompt_331 = 'Let\'s first understand the problem, extract relevant correct variables and their correct corresponding numerals, and devise complete plans. Then, let\'s carry out the plan, calculate intermediate variables including extracted variables(pay attention to correct numerical calculation and common sense), solve the problem by single equations, and show the answer.'
prompt_332 = 'Let\'s devise a complete plan. Then, let\'s carry out the plan, solve the problem step by step, and show the answer.'
prompt_333 = 'Let\'s devise a plan and solve the problem step by step.'
prompt_334 = 'Let\'s first understand the problem, extract relevant variables and their corresponding numerals, and devise a plan. Then, let\'s carry out the plan, calculate intermediate variables (pay attention to correct numerical calculation and common sense), solve the problem step by step(pay attention to calculation), and show the answe'
prompt_335 = 'Let\'s first understand the problem, extract relevant variables and their corresponding numerals, and devise a complete plan. Then, let\'s carry out the plan, calculate intermediate variables (pay attention to correct numerical calculation and common sense), solve the problem step by step carefully, and show the answer.'
prompt_336 = 'Let\'s first understand the problem, extract all relevant  variables and their corresponding numerals carefully, and devise a plan. Then, let\'s carry out the plan, calculate intermediate variables(pay attention to correct numerical calculation and common sense), solve the problem step by step carefully, and show the answer.'
prompt_337 = 'Let\'s first understand the problem carefully(pay attention to correct semantic), extract all relevant  variables and their corresponding numerals(pay attention to common sense), and devise a complete plan. \nThen, let\'s implement the plan carefully, calculate intermediate variables(pay attention to any correct numerical calculation, common sense and measurement unit), solve the problem step by step carefully(pay attention to correct numerical calculation and do not skip any step), and show the answer.'
prompt_338 = 'Let\'s first understand the problem semantic carefully, extract all relevant  variables and their corresponding numerals(pay attention to common sense), and devise a complete plan. \nThen, let\'s implement the plan carefully, calculate intermediate variables(pay attention to any correct numerical calculation, common sense and measurement unit), solve the problem step by step carefully(pay attention to correct numerical calculation and do not skip any step), and show the answer.'
prompt_339 = 'Let\'s extract relevant variables and their corresponding numerals, and devise a plan. ' \
             'Then, let\'s carry out the plan, calculate intermediate variables (pay attention to correct numeral calculation and commonsense), solve the problem step by step, and show the answer. '
prompt_340 = 'Let\'s devise a plan. Then implement the plan, and solve the problem step by step'
prompt_341 = 'Firstly, extract variables and their corresponding numerals. Then, calculate intermediate variables (pay attention to correct numerical calculation and commonsense). Finally, solve the problem step by step'
prompt_342 = ' Let\'s devise a plan to to solve the problem(please be sure to give yes or no).'
prompt_343 = 'Let\'s first devise a plan, then solve the problem step by step.(Distinguish between tail up and head up)'
prompt_344 = 'Let\'s first devise a plan, then solve the problem step by step.'
prompt_345 = 'Let\'s first understand the problem and devise a complete plan.Then, let\'s carry out the plan, reason problem step by step. Every step answer the subquestion "does the person flip and what is the coin current state?", and according to the coin last state give the final answer(pay attention to every flip, the coin turns state). \n\nPlan: \nStep 1:'
prompt_346 = 'Let\'s first understand the problem and devise a complete plan.Then, let\'s carry out the plan, reason problem step by step. Every step answer the subquestion "does the person flip and what is the coin current state?", and according to the last coin state, give the final answer(pay attention that the coin turns state at every flip). \n\nPlan: \nStep 1:'
prompt_347 = 'Let\'s first understand the problem and devise a complete plan. Then, let\'s carry out the plan and reason problem step by step. Every step answer the subquestion, "does the person flip and what is the coin\'s current state?". According to the coin\'s last state, give the final answer (pay attention to every flip and the coin’s turning state).'
prompt_348 = 'Let\'s first assume the answer is \'yes\', then devise a plan to reason the answer\'s correctness.'
prompt_349 = 'Let\'s devise a plan and think the problem step by step according to normal people\'s thought.'
prompt_350 = 'Let\'s first understand the problem, extract relevant variables and  their corresponding numerals, and make a complete plan.Then,  let\'s carry out the plan, calculate intermediate variables (pay attention to correct numerical calculation and commonsense), solve the problem step by step, and show the answer.'
prompt_351 = 'Let\'s start with answering yes or no. Then make a plan to reason the answer step by step.'
prompt_352 = 'Let\'s make a plan and reason the question step by step.'
prompt_353 = 'Let\'s first prepare relevant information and make a plan. Then, let\'s answer the question step by step (pay attention to commonsense and logical coherence).'
prompt_354 = 'Let\'s make a plan to reason the question according to the information of open world. Then carry out the plan and reason the question logically. Finally, give out yes or no to the question.(pay attention to commonsense and logical coherence).'
prompt_355 = 'Let\'s first extract relevant information from knowledge of the open world and make a plan to answer the question. Then, let\'s carry out the plan and answer the question step by step.'


def get_prompt():
    if args.learning_type == 'zero_shot':
        try:
            demos = None
            return demos, eval('prompt_{}'.format(args.prompt_id))
        except NameError as e:
            raise NameError('can\'t find prompt_id: {}'.format(args.prompt_id))
    elif args.learning_type == 'few_shot':
        demo_file = Few_Shot_Demo_Folder + f'{args.domain}_prompt_{args.prompt_id}.json'
        if args.dataset.lower() in ['aqua']:
            demo_file = Few_Shot_Demo_Folder + f'{args.domain}_prompt_{args.prompt_id}_choices.json'
        try:
            f = open(demo_file, 'r', encoding='utf-8')
            demos_list = json.load(f)
            demos_list = demos_list['demo']
            demos = '\n'.join(demos_list)
            return demos, eval('prompt_{}'.format(args.prompt_id))
        except NameError as e:
            raise NameError('can\'t find prompt_id: {}'.format(args.prompt_id))
        except FileNotFoundError as e:
            raise FileNotFoundError('can\'t find the demo file: {}'.format(demo_file))
    else:
        raise ValueError('not support learning_type: {}'.format(args.learning_type))


def construct_input(prompt, text):
    inputs = 'Q:' + text + "\nA: " + prompt
    return inputs
