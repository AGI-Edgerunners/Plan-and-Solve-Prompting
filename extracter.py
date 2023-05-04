import re
from typing import Union


def extract_finance(args, text):
    pattern = '-?\d+\.?\d*%?'
    pred = re.findall(pattern, text)
    if pred:
        if '%' == pred[-1][-1]:
            pred_answer = eval(pred[-1][:-1] + '/100')
        else:
            pred_answer = float(pred[-1])
        return pred_answer
    pattern = 'yes|no'
    pred = re.findall(pattern, text)
    if pred:
        return pred[-1]
    return None


def extract_answer(args, text):
    dataset = args.dataset.lower()
    if dataset in ["svamp", "gsm8k", "multiarith", "addsub", "singleeq"]:
        pred_answer = extract_number(args, text)
    elif dataset == "commonsenseqa":
        pred = text.strip()
        pred = re.sub("\(|\)|\:|\.|\,", "", pred)
        pred = pred.split()
        pred_answer = [i for i in pred if i in ('A|B|C|D|E')][-1]
        # pred_answer = re.findall(r'A|B|C|D|E', pred)[0]
        return pred_answer
    elif dataset == "aqua":
        pred = text.strip()
        pred_answer = re.findall(r'A|B|C|D|E', pred)[0]
        return pred_answer
    elif dataset == "strategyqa" or dataset == 'coin_flip':
        pred = text.lower()
        pred = re.sub("\"|\'|\n|\.|\s|\:|\,", " ", pred)
        pred = pred.split()
        pred_answer = [i for i in pred if i in ("yes", "no")][-1]
        return pred_answer
    elif dataset == "last_letters":
        pred = re.sub("\"|\'|\n|\.|\s", "", text)
        pred_answer = pred
        return pred_answer
    else:
        raise NotImplementedError(' not support dataset: {}'.format(dataset))
    if isinstance(pred_answer, str):
        try:
            pred_answer = float(pred_answer)
        except ValueError as e:
            pred_answer = float('inf')
    return pred_answer


def get_precision(gt_ans: float) -> int:
    precision = 5
    if '.' in str(gt_ans):
        precision = len(str(gt_ans).split('.')[-1])
    return precision


def extract_bool(args, text: str) -> str:
    pass


def extract_number(args, text: str) -> Union[float, None]:
    text = text.replace(',', '')
    pred = [s for s in re.findall(r'-?\d+\.?\d*', text)]
    if pred:
        pred_answer = float(pred[-1])
    else:
        pred_answer = None
    return pred_answer


def extract_choice(args, text: str) -> str:
    pass
