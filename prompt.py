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

prompt_101 = "Let's think step by step."

prompt_201 = "Let's first understand the problem and devise a plan to solve the problem. " \
             "Then, let's carry out the plan to solve the problem step by step."
prompt_301 = "Let's first understand the problem, extract relevant variables and their corresponding numerals, " \
             "and devise a plan. Then, let's carry out the plan, calculate intermediate variables (pay attention to " \
             "correct numeral calculation and commonsense), solve the problem step by step, and show the answer."
prompt_302 = "Let's first understand the problem, extract relevant variables and their corresponding numerals, " \
             "and devise a complete plan. Then, let's carry out the plan, calculate intermediate variables " \
             "(pay attention to correct numerical calculation and commonsense), " \
             "solve the problem step by step, and show the answer."
prompt_303 = "Let's devise a plan and solve the problem step by step."
prompt_304 = "Let's first understand the problem and devise a complete plan. " \
             "Then, let's carry out the plan and reason problem step by step. Every step answer the subquestion, " \
             "\"does the person flip and what is the coin's current state?\". According to the coin's last state, " \
             "give the final answer (pay attention to every flip and the coin’s turning state)."
prompt_305 = "Let's first understand the problem, extract relevant variables and  their corresponding numerals, " \
             "and make a complete plan. Then, let's carry out the plan, calculate intermediate variables (pay " \
             "attention to correct numerical calculation and commonsense), " \
             "solve the problem step by step, and show the answer."
prompt_306 = "Let's first prepare relevant information and make a plan. Then, let's answer the question step by step " \
             "(pay attention to commonsense and logical coherence)."
prompt_307 = "Let's first understand the problem, extract relevant variables and their corresponding numerals, " \
             "and make and devise a complete plan. Then, let's carry out the plan, calculate intermediate variables " \
             "(pay attention to correct numerical calculation and commonsense), " \
             "solve the problem step by step, and show the answer."

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
