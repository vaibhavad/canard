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
    parser.add_argument("--spacy", default=True)
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


    if args.spacy:
        nlp = English()
    
    for instances, split in info:
        with open(join(args.output_dir,'{}-src.txt').format(\
                                            split), 'w') as srch:
            with open(join(args.output_dir,'{}-tgt.txt').format(\
                                            split), 'w') as tgth:
                for sample in instances:
                    if len(sample['Context']) == 0:
                        history = []
                        src = ' ||| '.join(history+[sample['Rewrite']])
                        tgt = sample['Rewrite']
                        if args.spacy:
                            src = ' '.join([tok.text for tok in nlp(src)])
                            tgt = ' '.join([tok.text for tok in nlp(tgt)])

                        srch.write(src+'\n')
                        tgth.write(tgt+'\n')
                        history.append(sample["Rewrite"])
                        history.append(sample["Answer"])
                    else:
                        src = ' ||| '.join(history+[sample['Question']])
                        tgt = sample['Rewrite']
                        if args.spacy:
                            src = ' '.join([tok.text for tok in nlp(src)])
                            tgt = ' '.join([tok.text for tok in nlp(tgt)])

                        srch.write(src+'\n')
                        tgth.write(tgt+'\n')
                        history.append(sample['Question'])
                        history.append(sample["Answer"])

if __name__ == "__main__":
    main()

