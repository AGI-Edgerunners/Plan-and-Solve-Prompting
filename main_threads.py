import os
import threading
from collections import Counter

from config import args
from extracter import extract_answer, get_precision
from prompt import get_prompt, construct_input
from prediction_runner import basic_runner
from utils import *

now = print_now(1).split(' ')[0].replace('/', '-')
Result_Folder = 'result/{}'.format(now)
# Result_Folder = 'result'
if not os.path.exists(Result_Folder):
    os.mkdir(Result_Folder)
Decoder_Error_File = f'{Result_Folder}/{args.learning_type}-{args.dataset}-{args.task_id}-{args.engine}_deco.json'
Predict_File = f'{Result_Folder}/{args.dataset}/{args.learning_type}-{args.task_id}-{args.engine}.json'
if not os.path.exists(f'{Result_Folder}/{args.dataset}'):
    os.mkdir(f'{Result_Folder}/{args.dataset}')

Decoder_Error_File_Lock = threading.Lock()
Predict_File_Lock = threading.Lock()
API_File_Lock = threading.Lock()
Correct_Lock = threading.Lock()
Total_Lock = threading.Lock()

Global_Correct = 0
Global_Total = 0


def thread_task(datas: tuple, args, thread_id, apikey):
    correct = 0
    global Global_Correct
    global Global_Total
    question, answer, ids = datas
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
            Decoder_Error_File_Lock.acquire()
            write_json(decode_error_data, Decoder_Error_File)
            Decoder_Error_File_Lock.release()
            Total_Lock.acquire()
            Global_Total += 1
            Total_Lock.release()
            continue
        if not get_result:
            Total_Lock.acquire()
            Global_Total += 1
            Total_Lock.release()
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
                        Decoder_Error_File_Lock.acquire()
                        write_json(decode_error_data, Decoder_Error_File)
                        Decoder_Error_File_Lock.release()
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
                    Decoder_Error_File_Lock.acquire()
                    write_json(decode_error_data, Decoder_Error_File)
                    Decoder_Error_File_Lock.release()
                    Total_Lock.acquire()
                    Global_Total += 1
                    Total_Lock.release()
                    continue
                if not get_result:
                    Total_Lock.acquire()
                    Global_Total += 1
                    Total_Lock.release()
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
                    Predict_File_Lock.acquire()
                    write_json(json_data, Predict_File)
                    Predict_File_Lock.release()
                else:
                    json_data = {
                        "ID": ids[idx],
                        "question": question[idx],
                        "chain-of-thought": pred,
                        "pred": pred_answer,
                        "answer": answer[idx],
                        "ans": ans
                    }
                    Predict_File_Lock.acquire()
                    write_json(json_data, Predict_File)
                    Predict_File_Lock.release()
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
                        Predict_File_Lock.acquire()
                        write_json(json_data, Predict_File)
                        Predict_File_Lock.release()
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
                        Predict_File_Lock.acquire()
                        write_json(json_data, Predict_File)
                        Predict_File_Lock.release()
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
                        Predict_File_Lock.acquire()
                        write_json(json_data, Predict_File)
                        Predict_File_Lock.release()
                    else:
                        json_data = {
                            "ID": ids[idx],
                            "question": question[idx],
                            "chain-of-thought": pred,
                            "pred": pred_answer,
                            "answer": answer[idx],
                            "ans": ans
                        }
                        Predict_File_Lock.acquire()
                        write_json(json_data, Predict_File)
                        Predict_File_Lock.release()
        else:
            json_data = {
                "ID": ids[idx],
                "question": question[idx],
                "chain-of-thought": pred,
                "pred": pred_answer,
                "answer": answer[idx],
                "ans": ans
            }
            Predict_File_Lock.acquire()
            write_json(json_data, Predict_File)
            Predict_File_Lock.release()
        print(
            'thread:{} correct:{} tested:{} {} total:{} global correct/total:{}/{}'.format(thread_id, correct, idx + 1,
                                                                                           correct / (idx + 1),
                                                                                           len(question),
                                                                                           Global_Correct,
                                                                                           Global_Total))
    return correct


def zero_shot_cot():
    correct = 0
    question, answer, ids = load_data(args)
    avr_nums = int(len(question) / 8)
    thread_list = []
    apikey_list = json.load(open('apikeys.json', 'r', encoding='utf-8'))
    assert len(apikey_list) == 8
    for i in range(8):
        if i == 7:
            thread_list.append(
                TaskThread(
                    str(i),
                    datas=(question[i * avr_nums:], answer[i * avr_nums:],
                           ids[i * avr_nums:]),
                    args=args,
                    apikey=apikey_list[i]
                )
            )
        else:
            thread_list.append(
                TaskThread(
                    str(i),
                    datas=(question[i * avr_nums:(i + 1) * avr_nums], answer[i * avr_nums:(i + 1) * avr_nums],
                           ids[i * avr_nums:(i + 1) * avr_nums]),
                    args=args,
                    apikey=apikey_list[i]
                )
            )
    for i in range(8):
        thread_list[i].start()
    for i in range(8):
        thread_list[i].join()
    for i in range(8):
        correct += thread_list[i].result
    return correct


class TaskThread(threading.Thread):
    def __init__(self, thread_id, datas, args, apikey):
        super().__init__(None)
        self.thread_id = thread_id
        self.datas = datas
        self.args = args
        self.result = None
        self.apikey = apikey

    def run(self) -> None:
        self.result = thread_task(self.datas, self.args, self.thread_id, self.apikey)


if __name__ == '__main__':
    print_exp(args)
    alls = zero_shot_cot()
    print(alls)
