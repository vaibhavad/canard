import json
from glob import glob
from datetime import datetime, timedelta

CONV_DIR = '/Users/vaibhav/Coqoa/final_conversations_2'
REWRITES_FILE = 'data/results/ocoqa-test-t5-qrecc.txt'
TARGET_DIR = 'rewrites/t5/qrecc_model/'
MIN_CONV_LENGTH = 10
MIN_ANNOTATION_LENGTH = 3
IST_TIME_OFFSET = 9.5
END_DATE = '2021-06-07'
end_date = datetime.strptime(END_DATE + " 23:59:59", '%Y-%m-%d %H:%M:%S')

def main():

    convs = []
    turns = 0.0
    files = sorted(glob(CONV_DIR + '/*'))
    
    for file in files:
        with open(file, 'r') as f:
            conv = json.load(f)
            ist_timestamp = datetime.strptime(conv["timestamp"], '%Y-%m-%d %H:%M:%S') +  timedelta(hours = IST_TIME_OFFSET)
            conv["id"] = file.split('/')[-1]
            if (len(conv["turns"]) >= MIN_CONV_LENGTH and 'additional_answers' in conv and len(conv["additional_answers"]) >= MIN_ANNOTATION_LENGTH) and ist_timestamp <= end_date:
                convs.append(conv)

    src_ques = []
    trg_ques = []

    with open(REWRITES_FILE, 'r') as f:
        for line in f:
            trg_ques.append(line.strip())


    for conv in convs:

        for i, turn in enumerate(conv["turns"]):
            if i % 2 == 0:
                src_ques.append({"id": conv["id"], "text": turn["text"]})

    assert len(src_ques) == len(trg_ques)

    conv_id = src_ques[0]["id"]
    ques = []

    for i, line in enumerate(src_ques):
        if not line["id"] == conv_id:
            with open(TARGET_DIR + conv_id, 'w') as f:
                for q in ques:
                    f.write(q)
                    f.write('\n')
            ques = []
            conv_id = line["id"]
        ques.append(trg_ques[i])

if __name__ == "__main__":
    main()

