import json
from glob import glob
from datetime import datetime, timedelta

CONV_DIR = '/Users/vaibhav/Coqoa/final_final_conversations'
MIN_CONV_LENGTH = 10
OUTPUT_FILES = ['data/T5/trans_ocoqa_train.json',
               'data/T5/trans_ocoqa_dev.json',
               'data/T5/trans_ocoqa_test.json']
DEV_IDS_FILE = '/Users/vaibhav/Coqoa/dev_list.txt'
TEST_IDS_FILE = '/Users/vaibhav/Coqoa/test_list.txt'


def main():

    convs = [[], [], []]
    files = sorted(glob(CONV_DIR + '/*'))
    
    dev_ids = []
    with open(DEV_IDS_FILE) as f:
        for line in f:
            dev_ids.append(line.strip())

    test_ids = []
    with open(TEST_IDS_FILE) as f:
        for line in f:
            test_ids.append(line.strip())
    turns = 0
    for file in files:
        with open(file, 'r') as f:
            conv = json.load(f)
            if len(conv["turns"]) >= MIN_CONV_LENGTH:
                turns += len(conv['turns'])
                if conv['id'] in dev_ids:
                    convs[1].append(conv)
                elif conv['id'] in test_ids:    
                    convs[2].append(conv)
                else:
                    convs[0].append(conv)
    print(turns/2)
    
    for i, output_file in enumerate(OUTPUT_FILES):
        with open(output_file, 'w') as srch:
            for conv in convs[i]:
                history = []

                for i, turn in enumerate(conv["turns"]):
                    if i % 2 == 0:
                        src = ' SEP '.join(history + [turn["text"]])
                        obj = {"translation": {"en1": src, "en2": "What is life?"}}
                        srch.write(json.dumps(obj)+'\n')
                    if turn["text"] == 'UNANSWERABLE':
                        # pass
                        turn["text"] = "I don't know."
                    # else:
                    history.append(turn["text"])


if __name__ == "__main__":
    main()
