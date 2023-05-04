import os
from collections import Counter
import openai

from config import args
from extracter import get_precision, extract_answer
from prompt import get_prompt, construct_input
from prediction_runner import basic_runner
from utils import write_json, print_now, load_data, print_exp

now = print_now(1).split(' ')[0].replace('/', '-')
Result_Folder = 'result/{}'.format(now)
if not os.path.exists('result'):
    os.mkdir('result')
if not os.path.exists(Result_Folder):
    os.mkdir(Result_Folder)

Decoder_Error_File = f'{Result_Folder}/{args.learning_type}-{args.dataset}-{args.prompt_id}-{args.engine}_deco.json'
Predict_File = f'{Result_Folder}/{args.dataset}/{args.learning_type}-{args.prompt_id}-{args.engine}.json'
if not os.path.exists(f'{Result_Folder}/{args.dataset}'):
    os.mkdir(f'{Result_Folder}/{args.dataset}')


def zero_shot_cot():
    correct = 0
    apikey = args.openai_apikey
    question, answer, ids = load_data(args)
    _, prompt = get_prompt()
    for idx, element in enumerate(question):
        # --test_star 100 从100开始测试
        # --test_end 100 只测前100个
        # --test_star 100 --test_end 200 从100开始测试，到200结束
        inputs = construct_input(prompt, element)
        try:
            get_result, pred, error_msg = basic_runner(args, inputs, args.max_length_cot, apikey)
        except:
            decode_error_data = {
                'question': question[idx]
            }
            write_json(decode_error_data, Decoder_Error_File)
            continue
        if not get_result:
            continue
        if args.SC:
            answer_list = []
            for i in range(len(pred)):
                input_ = inputs + pred[i]
                if 'Therefore, the answer is' in input_ or 'The answer is' in input_:
                    if 'The answer is' in input_:
                        input_2 = input_.split('The answer is')[-1]
                    else:
                        input_2 = input_.split('the answer is')[-1]
                    try:
                        pred_answer1 = extract_answer(args, input_2)
                    except:
                        pred_answer1 = None
                else:
                    inputs2 = input_ + ' ' + args.direct_answer_trigger_for_direct
                    try:
                        get_result, pred3, error_msg = basic_runner(args, inputs2, args.max_length_cot, apikey)
                    except:
                        decode_error_data = {
                            'question': question[idx]
                        }
                        write_json(decode_error_data, Decoder_Error_File)
                        continue
                    if not get_result:
                        continue
                    try:
                        pred_answer1 = extract_answer(args, pred3)
                    except:
                        pred_answer1 = None
                answer_list.append(pred_answer1)
            collection_words = Counter(answer_list)
            pred_answer = collection_words.most_common(1)[0][0]
        else:
            if 'Therefore, the answer is' in pred or 'The answer is' in pred:
                if 'The answer is' in pred:
                    pred2 = pred.split('The answer is')[-1]
                else:
                    pred2 = pred.split('the answer is')[-1]
                try:
                    pred_answer = extract_answer(args, pred2)
                except:
                    pred_answer = None
            else:
                inputs2 = inputs + pred + ' ' + args.direct_answer_trigger_for_direct
                try:
                    get_result, pred3, error_msg = basic_runner(args, inputs2, args.max_length_cot, apikey)
                except:
                    decode_error_data = {
                        'question': question[idx]
                    }
                    write_json(decode_error_data, Decoder_Error_File)
                    continue
                if not get_result:
                    continue
                try:
                    pred_answer = extract_answer(args, pred3)
                except:
                    pred_answer = None
        ans = False
        if pred_answer is not None:
            if args.dataset.lower() in ["svamp", "gsm8k", "multiarith", "addsub", "singleeq"]:
                if abs(pred_answer - answer[idx]) < 1e-3:
                    correct += 1
                    ans = True
                    json_data = {
                        "ID": ids[idx],
                        "question": question[idx],
                        "chain-of-thought": pred,
                        "pred": pred_answer,
                        "answer": answer[idx],
                        "ans": ans
                    }
                    write_json(json_data, Predict_File)
                else:
                    json_data = {
                        "ID": ids[idx],
                        "question": question[idx],
                        "chain-of-thought": pred,
                        "pred": pred_answer,
                        "answer": answer[idx],
                        "ans": ans
                    }
                    write_json(json_data, Predict_File)
            else:
                if isinstance(pred_answer, float) and isinstance(answer[idx], float):
                    precision = min(get_precision(pred_answer), get_precision(answer[idx]))
                    if round(pred_answer, precision) == round(answer[idx], precision):
                        correct += 1
                        ans = True
                        json_data = {
                            "ID": ids[idx],
                            "question": question[idx],
                            "chain-of-thought": pred,
                            "pred": pred_answer,
                            "answer": answer[idx],
                            "ans": ans
                        }
                        write_json(json_data, Predict_File)
                    else:
                        ans = False
                        json_data = {
                            "ID": ids[idx],
                            "question": question[idx],
                            "chain-of-thought": pred,
                            "pred": pred_answer,
                            "answer": answer[idx],
                            "ans": ans
                        }
                        write_json(json_data, Predict_File)
                else:
                    if pred_answer == answer[idx]:
                        correct += 1
                        ans = True
                        json_data = {
                            "ID": ids[idx],
                            "question": question[idx],
                            "chain-of-thought": pred,
                            "pred": pred_answer,
                            "answer": answer[idx],
                            "ans": ans
                        }
                        write_json(json_data, Predict_File)
                    else:
                        json_data = {
                            "ID": ids[idx],
                            "question": question[idx],
                            "chain-of-thought": pred,
                            "pred": pred_answer,
                            "answer": answer[idx],
                            "ans": ans
                        }
                        write_json(json_data, Predict_File)
        else:
            json_data = {
                "ID": ids[idx],
                "question": question[idx],
                "chain-of-thought": pred,
                "pred": pred_answer,
                "answer": answer[idx],
                "ans": ans
            }
            write_json(json_data, Predict_File)
        print('correct:{} tested:{} {} total:{}'.format(correct, idx + 1, correct / (idx + 1), len(question)))
    return correct


def few_shot_cot():
    correct = 0
    apikey = args.openai_apikey
    openai.api_key = apikey
    question, answer, ids = load_data(args)
    demos, prompt = get_prompt()
    for idx, element in enumerate(question):
        # --test_star 100 从100开始测试
        # --test_end 100 只测前100个
        # --test_star 100 --test_end 200 从100开始测试，到200结束
        inputs = construct_input(prompt, element)
        inputs = demos + '\n' + inputs
        try:
            get_result, pred, error_msg = basic_runner(args, inputs, args.max_length_cot, apikey)
        except:
            decode_error_data = {
                'question': question[idx]
            }
            write_json(decode_error_data, Decoder_Error_File)
            continue
        if not get_result:
            continue

        if 'The answer is' in pred or 'the answer is' in pred:
            if 'The answer is' in pred:
                pred2 = pred.split('The answer is')[-1]
            else:
                pred2 = pred.split('the answer is')[-1]
            try:
                pred_answer = extract_answer(args, pred2)
            except:
                pred_answer = None
        else:
            inputs2 = inputs + pred + ' ' + args.direct_answer_trigger_for_direct
            try:
                get_result, pred3, error_msg = basic_runner(args, inputs2, args.max_length_cot, apikey)
            except:
                decode_error_data = {
                    'question': question[idx]
                }
                write_json(decode_error_data, Decoder_Error_File)
                continue
            if not get_result:
                continue
            try:
                pred_answer = extract_answer(args, pred3)
            except:
                pred_answer = None
        ans = False
        if pred_answer is not None:
            if args.dataset.lower() in ["svamp", "gsm8k", "multiarith", "addsub", "singleeq"]:
                if abs(pred_answer - answer[idx]) < 1e-3:
                    correct += 1
                    ans = True
                    json_data = {
                        "ID": ids[idx],
                        "question": question[idx],
                        "chain-of-thought": pred,
                        "pred": pred_answer,
                        "answer": answer[idx],
                        "ans": ans
                    }
                    write_json(json_data, Predict_File)
                else:
                    json_data = {
                        "ID": ids[idx],
                        "question": question[idx],
                        "chain-of-thought": pred,
                        "pred": pred_answer,
                        "answer": answer[idx],
                        "ans": ans
                    }
                    write_json(json_data, Predict_File)
            else:
                if isinstance(pred_answer, float) and isinstance(answer[idx], float):
                    precision = min(get_precision(pred_answer), get_precision(answer[idx]))
                    if round(pred_answer, precision) == round(answer[idx], precision):
                        correct += 1
                        ans = True
                        json_data = {
                            "ID": ids[idx],
                            "question": question[idx],
                            "chain-of-thought": pred,
                            "pred": pred_answer,
                            "answer": answer[idx],
                            "ans": ans
                        }
                        write_json(json_data, Predict_File)
                    else:
                        ans = False
                        json_data = {
                            "ID": ids[idx],
                            "question": question[idx],
                            "chain-of-thought": pred,
                            "pred": pred_answer,
                            "answer": answer[idx],
                            "ans": ans
                        }
                        write_json(json_data, Predict_File)
                else:
                    if pred_answer == answer[idx]:
                        correct += 1
                        ans = True
                        json_data = {
                            "ID": ids[idx],
                            "question": question[idx],
                            "chain-of-thought": pred,
                            "pred": pred_answer,
                            "answer": answer[idx],
                            "ans": ans
                        }
                        write_json(json_data, Predict_File)
                    else:
                        json_data = {
                            "ID": ids[idx],
                            "question": question[idx],
                            "chain-of-thought": pred,
                            "pred": pred_answer,
                            "answer": answer[idx],
                            "ans": ans
                        }
                        write_json(json_data, Predict_File)
        else:
            json_data = {
                "ID": ids[idx],
                "question": question[idx],
                "chain-of-thought": pred,
                "pred": pred_answer,
                "answer": answer[idx],
                "ans": ans
            }
            write_json(json_data, Predict_File)
        print('correct:{} tested:{} total:{}'.format(correct, idx + 1, len(question)))
    return correct


if __name__ == '__main__':
    print_exp(args)
    if args.learning_type == 'zero_shot':
        alls = zero_shot_cot()
    else:
        alls = few_shot_cot()
    print(alls)
