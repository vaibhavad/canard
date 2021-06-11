# python FormatT5_qrecc.py data/release/qrecc_train.json train data/T5 --make_dev_from_train --dev_percent 10
# python FormatT5_qrecc.py data/release/qrecc_test.json test data/T5

import json
import argparse
import random
from os.path import join
from spacy.lang.en import English

def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument("dataset_file")
    parser.add_argument("split")
    parser.add_argument("output_dir")
    parser.add_argument("--make_dev_from_train", action='store_true')
    parser.add_argument("--dev_percent", type=int, default=10)

    args = parser.parse_args()

    with open(args.dataset_file) as inh:
        samples = json.load(inh)
        num_convs = samples[-1]["Conversation_no"]
        if args.make_dev_from_train:
            num_dev_convs = round(float(args.dev_percent)/100.0 * num_convs)
            dev_convs_idxs = random.sample(range(1, num_convs+1), num_dev_convs)
            train_samples = []
            dev_samples = []
            for sample in samples:
                if sample["Conversation_no"] in dev_convs_idxs:
                    dev_samples.append(sample)
                else:
                    train_samples.append(sample)

    if args.make_dev_from_train:
        info = [(train_samples, args.split), (dev_samples, 'dev')]
    else:
        info = [(samples, args.split)]
    
    for instances, split in info:
        with open(join(args.output_dir,'trans_qrecc_{}.json').format(\
                                            split), 'w') as srch:
            for sample in instances:
                if len(sample['Context']) == 0:
                    history = []
                    src = ' SEP '.join(history+[sample['Rewrite']])
                    tgt = sample['Rewrite']
                    obj = {"translation" : {"en1": src, "en2": tgt}}
                    srch.write(json.dumps(obj)+'\n')
                    history.append(sample["Rewrite"])
                    history.append(sample["Answer"])
                else:
                    src = ' SEP '.join(history+[sample['Question']])
                    tgt = sample['Rewrite']
                    obj = {"translation" : {"en1": src, "en2": tgt}}
                    srch.write(json.dumps(obj)+'\n')

                    history.append(sample['Question'])
                    history.append(sample["Answer"])

if __name__ == "__main__":
    main()

