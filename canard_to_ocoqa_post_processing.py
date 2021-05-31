import json
from glob import glob

CONV_DIR = '/Users/vaibhav/Coqoa/final_conversations'
TARGET_FILE = 'ocoqa-trg.txt'
MIN_CONV_LENGTH = 10

def main():

    convs = []
    turns = 0.0
    files = sorted(glob(CONV_DIR + '/*'))
    
    for file in files:
        with open(file, 'r') as f:
            conv = json.load(f)
            conv["id"] = file.split('/')[-1]
            if len(conv["turns"]) >= MIN_CONV_LENGTH:
                convs.append(conv)

    src_ques = []
    trg_ques = []

    with open(TARGET_FILE, 'r') as f:
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
            with open("canard_rewrites/" + conv_id, 'w') as f:
                for q in ques:
                    f.write(q)
                    f.write('\n')
            ques = []
            conv_id = line["id"]
        ques.append(trg_ques[i])

if __name__ == "__main__":
    main()

