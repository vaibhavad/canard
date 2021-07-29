import json
from glob import glob
from datetime import datetime, timedelta

CONV_DIR = '/Users/vaibhav/Coqoa/final_final_conversations'
REWRITES_FILES = ['data/results/ocoqa-train-t5-qrecc.txt',
                  'data/results/ocoqa-dev-t5-qrecc.txt',
                  'data/results/ocoqa-test-t5-qrecc.txt']
TARGET_DIRS = ['rewrites/train/ocoqa/t5/qrecc_model/',
               'rewrites/dev/ocoqa/t5/qrecc_model/',
               'rewrites/test/ocoqa/t5/qrecc_model/']
MIN_CONV_LENGTH = 10
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

    for idx, rewrites_file in enumerate(REWRITES_FILES):

        src_ques = []
        trg_ques = []

        with open(rewrites_file, 'r') as f:
            for line in f:
                trg_ques.append(line.strip())

        for conv in convs[idx]:

            for i, turn in enumerate(conv["turns"]):
                if i % 2 == 0:
                    src_ques.append({"id": conv["id"], "text": turn["text"]})

        assert len(src_ques) == len(trg_ques)

        conv_id = src_ques[0]["id"]
        rewrite_ques = []
        original_ques = []

        for i, ques in enumerate(src_ques):
            if not ques["id"] == conv_id:
                assert len(original_ques) == len(rewrite_ques)
                with open(TARGET_DIRS[idx] + conv_id, 'w') as f:
                    f.write(original_ques[0])
                    f.write('\n')
                    for q in rewrite_ques[1:]:
                        f.write(q)
                        f.write('\n')
                rewrite_ques = []
                original_ques = []
                conv_id = ques["id"]
            rewrite_ques.append(trg_ques[i])
            original_ques.append(ques["text"])

        assert len(original_ques) == len(rewrite_ques)
        with open(TARGET_DIRS[idx] + conv_id, 'w') as f:
            f.write(original_ques[0])
            f.write('\n')
            for q in rewrite_ques[1:]:
                f.write(q)
                f.write('\n')


if __name__ == "__main__":
    main()
