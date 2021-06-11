# python FormatT5.py data/release/train.json train data/T5
# python FormatT5.py data/release/dev.json dev data/T5
# python FormatT5.py data/release/test.json test data/T5

import json
import argparse
from os.path import join
from spacy.lang.en import English

def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument("dataset_file")
    parser.add_argument("split")
    parser.add_argument("output_dir")

    args = parser.parse_args()

    with open(args.dataset_file) as inh:
        samples = json.load(inh)

    with open(join(args.output_dir,'trans_canard_{}.json').format(\
                                        args.split), 'w') as srch:
        first_question = None
        for sample in samples:
            assert len(sample['History']) >= 2
            if len(sample['History']) == 2:
                first_question = sample["Rewrite"]
                src = ' SEP '.join([first_question])
                tgt = sample['Rewrite']
                obj = {"translation" : {"en1": src, "en2": tgt}}
                srch.write(json.dumps(obj)+'\n')
            else:
                src = ' SEP '.join([first_question] + sample['History'][3:] + [sample['Question']])
                tgt = sample['Rewrite']
                obj = {"translation" : {"en1": src, "en2": tgt}}
                srch.write(json.dumps(obj)+'\n')

if __name__ == "__main__":
    main()

