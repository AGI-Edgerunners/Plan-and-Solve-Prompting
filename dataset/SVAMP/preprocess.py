import json
from os import path
import random
random.seed(2021)
data_path='dataset/SVAMP/SVAMP.json'

trainset_path='dataset/SVAMP/trainset.json'
testset_path='dataset/SVAMP/testset.json'
validset_path='dataset/SVAMP/validset.json'

def write_json_data(data, filename):
    """
    write data to a json file
    """
    with open(filename, 'w+', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    f.close()


def read_json_data(filename):
    '''
    load data from a json file
    '''
    f = open(filename, 'r', encoding="utf-8")
    return json.load(f)

datas=read_json_data(data_path)
print(len(datas))
random.shuffle(datas)
divide=int(len(datas)/10)

trainset=datas[:divide*8]
validset=datas[divide*8:divide*9]
testset=datas[divide*9:]
print(len(trainset),len(validset),len(testset))

write_json_data(trainset,trainset_path)
write_json_data(validset,validset_path)
write_json_data(testset,testset_path)