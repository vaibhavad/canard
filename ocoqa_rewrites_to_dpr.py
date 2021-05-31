import json
from os.path import join
from spacy.lang.en import English
from glob import glob

CONV_DIR = '/Users/vaibhav/Coqoa/final_conversations'
REWRITES_DIR = 'rewrites/canard_model'
DPR_OUTPUT_FILE = 'data/ocoqa_canard_dpr_format.csv'
MIN_CONV_LENGTH = 10

def main():

    ids = []
    files = glob(REWRITES_DIR + '/*')
    for file in files:
        ids.append(file.split('/')[-1])

    ids = sorted(ids)

    csv_rewrites = []
    csv_answers = []

    for id in ids:
        rewrites = []
        with open(REWRITES_DIR + '/' + id, 'r') as rewrite_f:
            for line in rewrite_f:
                rewrites.append(line.strip())

        answers = []
        with open(CONV_DIR + '/' + id, 'r') as conv_f:
            conv = json.load(conv_f)
            for i,turn in enumerate(conv["turns"]):
                if i%2 == 1:
                    answer = []
                    answer.append(turn["text"].strip('.'))
                    answers.append(answer)
        
        assert len(rewrites) >= len(answers)
            # print(id)
            # print(rewrites)
            # print(len(rewrites))
            # print(answers)
            # print(len(answers))
            # assert False
        if len(rewrites) > len(answers):
            answers.append([''])
        assert len(rewrites) == len(answers)

        csv_rewrites.extend(rewrites)
        csv_answers.extend(answers)

    with open(DPR_OUTPUT_FILE, 'w') as f:
        for i,rewrite in enumerate(csv_rewrites):
            f.write(rewrite.lower().strip('?').strip())
            f.write('\t')
            f.write(str(csv_answers[i]))
            f.write('\n')

if __name__ == "__main__":
    main()

