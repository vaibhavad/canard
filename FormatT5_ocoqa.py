import json
from os.path import join
from spacy.lang.en import English
from glob import glob

CONV_DIR = '/Users/vaibhav/Coqoa/final_conversations'
OUTPUT_FILE = 'data/T5/trans_ocoqa_test.json'
MIN_CONV_LENGTH = 10
MIN_ANNOTATION_LENGTH = 3

def main():

    convs = []
    turns = 0.0
    files = sorted(glob(CONV_DIR + '/*'))
    
    for file in files:
        with open(file, 'r') as f:
            conv = json.load(f)
            if len(conv["turns"]) >= MIN_CONV_LENGTH and 'additional_answers' in conv and len(conv["additional_answers"]) >= MIN_ANNOTATION_LENGTH:
                convs.append(conv)

    nlp = English()

    with open(OUTPUT_FILE, 'w') as srch:
        for conv in convs:
            history = []

            for i, turn in enumerate(conv["turns"]):
                if i % 2 == 0:
                    src = ' SEP '.join(history + [turn["text"]])
                    obj = {"translation" : {"en1": src, "en2": "What is life?"}}
                    srch.write(json.dumps(obj)+'\n')
                if turn["text"] == 'UNANSWERABLE':
                    # pass
                    turn["text"] = "I don't know."
                # else:
                history.append(turn["text"])

if __name__ == "__main__":
    main()

