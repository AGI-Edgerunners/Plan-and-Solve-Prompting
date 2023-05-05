import json
import datetime
import numpy as np
import random
import torch
import os

Dataset_Folder = 'dataset'

def mkpath(path):
    if not os.path.exists(path):
        os.mkdir(path)

def print_now(return_flag=0):
    t_delta = datetime.timedelta(hours=9)
    JST = datetime.timezone(t_delta, 'JST')
    now = datetime.datetime.now(JST)
    now = now.strftime('%Y/%m/%d %H:%M:%S')
    if return_flag == 0:
        print(now)
    elif return_flag == 1:
        return now
    else:
        pass


def print_exp(args, return_flag=0):
    info = ''
    for k, v in vars(args).items():
        info += '{}:{}\n'.format(k, v)
    print('---------------experiment args---------------')
    print(info)
    print('---------------------------------------------')
    if return_flag == 0:
        return
    elif return_flag == 1:
        return info
    else:
        pass


def load_data(args):
    decoder = json.JSONDecoder()
    questions = []
    answers = []
    ids = []
    datapath = args.datapath if args.datapath else '{}/{}/{}.json'.format(Dataset_Folder, args.dataset,args.dataset)
    if args.dataset == 'gsm8k_zct_8':
        questions, rational, answers = [], [], []
        datapath = 'result/ours/text003/gsm8k_zct_1_10_8.json'
        with open(datapath) as f:
            json_data = json.load(f)
            for idx, line in enumerate(json_data):
                q = line['question']
                r = line['chain-of-thought']
                a = line['answer']
                questions.append(q)
                rational.append(r)
                answers.append(a)
                ids.append('temp_{}'.format(idx))
        if args.test_num == 'full':
            return questions, rational, answers
        else:
            return questions[:int(args.test_num)], rational[:int(args.test_num)], answers[:int(args.test_num)]
    if args.dataset == 'CommonsenseQA':
        datapath = 'dataset/CommonsenseQA/CommonsenseQA.jsonl'
    # read dataset file
    if args.dataset.lower() in ['svamp', 'svamp_sorted', 'gsm8k', 'gsm8k_sorted', 'multiarith', 'addsub', 'singleeq',
                                'strategyqa', 'coin_flip', 'last_letters']:
        with open(datapath) as f:
            if args.dataset.lower() in ['coin_flip', 'last_letters', 'strategyqa']:
                json_data = json.load(f)["examples"]
            else:
                json_data = json.load(f)

            for idx, line in enumerate(json_data):
                if args.dataset.lower() == 'svamp':
                    if line['Body'][-1] != '.':
                        q = line['Body'].strip() + ". " + line["Question"].strip()
                    else:
                        q = line['Body'].strip() + " " + line["Question"].strip()
                    a = float(line["Answer"])
                    id = line["ID"]
                elif args.dataset == 'svamp_sorted':
                    q = line['Question']
                    a = float(line['Answer'])
                    id = line['ID']
                elif args.dataset.lower() == 'strategyqa':
                    q = line["input"].strip()
                    a = int(line["target_scores"]["Yes"])
                    if a == 1:
                        a = "yes"
                    else:
                        a = "no"
                    id = 'temp_{}'.format(idx)
                elif args.dataset.lower() in ['coin_flip','last_letters']:
                    q = line["question"]
                    a = line["answer"]
                    id = 'temp_{}'.format(idx)
                elif args.dataset.lower() in ["multiarith", 'addsub', 'singleeq']:
                    q = line['sQuestion']
                    a = float(line['lSolutions'][0])
                    id = 'temp_{}'.format(idx)
                elif args.dataset.lower() in ['gsm8k', 'gsm8k_sorted', 'examples', 'examples']:
                    q = line['question']
                    a = float(line['answer'])
                    id = 'temp_{}'.format(idx)
                else:
                    raise ValueError('not support dataset: {}'.format(args.dataset))
                questions.append(q)
                answers.append(a)
                ids.append(id)

    elif args.dataset.lower() in ['aqua', 'commonsenseqa']:
        with open(datapath) as f:
            lines = f.readlines()
            for idx, line in enumerate(lines):
                if args.dataset.lower() == 'aqua':
                    json_res = decoder.raw_decode(line)[0]
                    choice = "(" + "(".join(json_res["options"])
                    choice = choice.replace("(", " (").replace(")", ") ")
                    choice = "Answer Choices:" + choice
                    q = json_res["question"].strip() + ' ' + choice
                    a = json_res["correct"]
                    id = 'temp_{}'.format(idx)
                elif args.dataset.lower() == 'commonsenseqa':
                    json_res = decoder.raw_decode(line)[0]
                    choice = "Answer Choices:"
                    for c in json_res["question"]["choices"]:
                        choice += " ("
                        choice += c["label"]
                        choice += ") "
                        choice += c["text"]
                    q = json_res["question"]["stem"].strip() + " " + choice
                    a = json_res["answerKey"]
                    id = 'temp_{}'.format(idx)
                else:
                    raise ValueError('not support dataset: {}'.format(args.dataset))
                questions.append(q)
                answers.append(a)
                ids.append(id)
    elif args.dataset.lower() in ['finqa','convfinqa']:
        with open(datapath) as f:
            json_data = json.load(f)
            for idx, line in enumerate(json_data):
                if args.dataset.lower() == 'convfinqa':
                    text = line['text'] + '\n'
                    table = line['table'].strip() + '\n'
                    q = 'Question: {}\n'.format(line['questions'])
                    a = line['answer']
                    id = 'temp_{}'.format(idx)
                elif args.dataset.lower() == 'finqa':
                    text = line['text'] + '\n'
                    table = line['table'].strip() + '\n'
                    q = 'Question: {}\n'.format(line['question'])
                    a = line['answer']
                    id = 'temp_{}'.format(idx)
                questions.append(text+table+q)
                answers.append(a)
                ids.append(id)
    else:
        raise ValueError('not support dataset: {}'.format(args.dataset))

    if args.test_end == 'full':
        return questions[int(args.test_start):], answers[int(args.test_start):], ids[int(args.test_start):]
    else:
        return questions[int(args.test_start):int(args.test_end)], answers[int(args.test_start):int(args.test_end)], ids[int(args.test_start):int(args.test_end)]

# def load_data(args):
#     decoder = json.JSONDecoder()
#     questions = []
#     answers = []
#     ids = []
#     datapath = args.datapath if args.datapath else '{}/{}/{}.json'.format(Dataset_Folder, args.dataset, args.dataset)
#     if args.dataset == 'CommonsenseQA':
#         datapath = 'dataset/CommonsenseQA/CommonsenseQA.jsonl'
#     # read dataset file
#     if args.dataset.lower() in ['svamp', 'svamp_sorted', 'gsm8k', 'gsm8k_sorted', 'multiarith', 'addsub', 'singleeq',
#                                 'strategyqa', 'coin_flip', 'last_letters']:
#         with open(datapath) as f:
#             if args.dataset.lower() in ['coin_flip', 'last_letters', 'strategyqa']:
#                 json_data = json.load(f)["examples"]
#             else:
#                 json_data = json.load(f)
#
#             for idx, line in enumerate(json_data):
#                 if args.dataset.lower() == 'svamp':
#                     if line['Body'][-1] != '.':
#                         q = line['Body'].strip() + ". " + line["Question"].strip()
#                     else:
#                         q = line['Body'].strip() + " " + line["Question"].strip()
#                     a = float(line["Answer"])
#                     id = line["ID"]
#                 elif args.dataset == 'svamp_sorted':
#                     q = line['Question']
#                     a = float(line['Answer'])
#                     id = line['ID']
#                 elif args.dataset.lower() == 'strategyqa':
#                     q = line["input"].strip()
#                     a = int(line["target_scores"]["Yes"])
#                     if a == 1:
#                         a = "yes"
#                     else:
#                         a = "no"
#                     id = 'temp_{}'.format(idx)
#                 elif args.dataset.lower() in ['coin_flip', 'last_letters']:
#                     q = line["question"]
#                     a = line["answer"]
#                     id = 'temp_{}'.format(idx)
#                 elif args.dataset.lower() in ["multiarith", 'addsub', 'singleeq']:
#                     q = line['sQuestion']
#                     a = float(line['lSolutions'][0])
#                     id = 'temp_{}'.format(idx)
#                 elif args.dataset.lower() in ['gsm8k', 'gsm8k_sorted', 'examples', 'examples']:
#                     q = line['question']
#                     a = float(line['answer'])
#                     id = 'temp_{}'.format(idx)
#                 else:
#                     raise ValueError('not support dataset: {}'.format(args.dataset))
#                 questions.append(q)
#                 answers.append(a)
#                 ids.append(id)
#
#     elif args.dataset.lower() in ['aqua', 'commonsenseqa']:
#         with open(datapath) as f:
#             lines = f.readlines()
#             for idx, line in enumerate(lines):
#                 if args.dataset.lower() == 'aqua':
#                     json_res = decoder.raw_decode(line)[0]
#                     choice = "(" + "(".join(json_res["options"])
#                     choice = choice.replace("(", " (").replace(")", ") ")
#                     choice = "Answer Choices:" + choice
#                     q = json_res["question"].strip() + ' ' + choice
#                     a = json_res["correct"]
#                     id = 'temp_{}'.format(idx)
#                 elif args.dataset.lower() == 'commonsenseqa':
#                     json_res = decoder.raw_decode(line)[0]
#                     choice = "Answer Choices:"
#                     for c in json_res["question"]["choices"]:
#                         choice += " ("
#                         choice += c["label"]
#                         choice += ") "
#                         choice += c["text"]
#                     q = json_res["question"]["stem"].strip() + " " + choice
#                     a = json_res["answerKey"]
#                     id = 'temp_{}'.format(idx)
#                 else:
#                     raise ValueError('not support dataset: {}'.format(args.dataset))
#                 questions.append(q)
#                 answers.append(a)
#                 ids.append(id)
#     elif args.dataset.lower() in ['finqa', 'convfinqa']:
#         with open(datapath) as f:
#             json_data = json.load(f)
#             for idx, line in enumerate(json_data):
#                 if args.dataset.lower() == 'convfinqa':
#                     text = line['text'] + '\n'
#                     table = line['table'].strip() + '\n'
#                     q = 'Question: {}\n'.format(line['questions'])
#                     a = line['answer']
#                     id = 'temp_{}'.format(idx)
#                 elif args.dataset.lower() == 'finqa':
#                     text = line['text'] + '\n'
#                     table = line['table'].strip() + '\n'
#                     q = 'Question: {}\n'.format(line['question'])
#                     a = line['answer']
#                     id = 'temp_{}'.format(idx)
#                 questions.append(text + table + q)
#                 answers.append(a)
#                 ids.append(id)
#     else:
#         raise ValueError('not support dataset: {}'.format(args.dataset))
#
#     if args.test_end == 'full':
#         return questions[int(args.test_start):], answers[int(args.test_start):], ids[int(args.test_start):]
#     else:
#         return questions[int(args.test_start):int(args.test_end)], answers[
#                                                                    int(args.test_start):int(args.test_end)], ids[
#                                                                                                              int(args.test_start):int(
#                                                                                                                  args.test_end)]


def write_json(data, path):
    f = open(path, mode='a', encoding='utf-8')
    json.dump(data, f, indent=4, ensure_ascii=False)
    f.close()


def fix_seed(seed):
    # random
    random.seed(seed)
    # Numpy
    np.random.seed(seed)
    # Pytorch
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
