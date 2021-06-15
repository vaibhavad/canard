import json
from glob import glob
from datetime import datetime, timedelta

CONV_DIR = '/Users/vaibhav/Coqoa/final_conversations_2'
OUTPUT_FILE = 'data/T5/trans_ocoqa_test.json'
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
            if (len(conv["turns"]) >= MIN_CONV_LENGTH and 'additional_answers' in conv and len(conv["additional_answers"]) >= MIN_ANNOTATION_LENGTH) and ist_timestamp <= end_date:
                convs.append(conv)

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

