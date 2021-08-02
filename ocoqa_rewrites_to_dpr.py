# don't need this file anymore

import json
from glob import glob

CONV_DIR = '/Users/vaibhav/Coqoa/final_final_conversations'
REWRITES_DIR = 'rewrites/t5/qrecc_model'
ORIGINAL_DIR = 'rewrites/original'
ALL_HISTORY_DIR = 'rewrites/all_history'
DPR_OUTPUT_FILE_REWRITES = 'data/ocoqa_test_t5_qrecc.csv'
DPR_OUTPUT_FILE_ORIGINAL = 'data/ocoqa_test_original.csv'
DPR_OUTPUT_FILE_ALL_HISTORY = 'data/ocoqa_test_all_history.csv'
MIN_CONV_LENGTH = 10
DEV_IDS_FILE = '/Users/vaibhav/Coqoa/dev_list.txt'
TEST_IDS_FILE = '/Users/vaibhav/Coqoa/test_list.txt'

def main():

    ids = []
    files = glob(REWRITES_DIR + '/*')
    for file in files:
        ids.append(file.split('/')[-1])

    ids = sorted(ids)

    csv_rewrites = []
    csv_answers = []
    csv_original_questions = []
    csv_questions_all_history = []

    for id in ids:
        rewrites = []
        with open(REWRITES_DIR + '/' + id, 'r') as rewrite_f:
            for line in rewrite_f:
                rewrites.append(line.strip())
        questions = []
        questions_all_history = []
        answers = []
        with open(CONV_DIR + '/' + id, 'r') as conv_f:
            conv = json.load(conv_f)
            for i,turn in enumerate(conv["turns"]):
                if i%2 == 1:
                    answer = []
                    answer.append(turn["text"].strip('.'))
                    answers.append(answer)
                else:
                    questions.append(turn["text"])
                    questions_all_history.append(" ".join(questions))
        
        assert len(rewrites) >= len(answers)
        assert len(questions) == len(rewrites) == len(questions_all_history)
            # print(id)
            # print(rewrites)
            # print(len(rewrites))
            # print(answers)
            # print(len(answers))
            # assert False
        if len(rewrites) > len(answers):
            answers.append([''])
        assert len(rewrites) == len(questions) == len(questions_all_history) == len(answers)

        with open(ORIGINAL_DIR + '/' + id, 'w') as f:
            for ques in questions:
                f.write(ques)
                f.write('\n')
        with open(ALL_HISTORY_DIR + '/' + id, 'w') as f:
            for ques in questions_all_history:
                f.write(ques)
                f.write('\n')

        csv_rewrites.extend(rewrites)
        csv_original_questions.extend(questions)
        csv_questions_all_history.extend(questions_all_history)
        csv_answers.extend(answers)

    with open(DPR_OUTPUT_FILE_REWRITES, 'w') as f:
        for i,q in enumerate(csv_rewrites):
            f.write(q.lower().strip('?').strip())
            f.write('\t')
            f.write(str(csv_answers[i]))
            f.write('\n')
    
    with open(DPR_OUTPUT_FILE_ORIGINAL, 'w') as f:
        for i,q in enumerate(csv_original_questions):
            f.write(q.lower().strip('?').strip())
            f.write('\t')
            f.write(str(csv_answers[i]))
            f.write('\n')

    with open(DPR_OUTPUT_FILE_ALL_HISTORY, 'w') as f:
        for i,q in enumerate(csv_questions_all_history):
            f.write(q.lower().strip('?').strip())
            f.write('\t')
            f.write(str(csv_answers[i]))
            f.write('\n')

if __name__ == "__main__":
    main()

