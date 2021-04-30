import os
import argparse

import pandas as pd
from tqdm import tqdm


def preprocessing(BASE_PATH, SAVE_PATH):
    question_lists, answer_lists = [], []
    all_data = []
    for fn in os.listdir(BASE_PATH):
        if os.path.splitext(fn)[-1] != '.xlsx':
            continue
        print(fn)
        data = pd.read_excel(os.path.join(BASE_PATH, fn))
        all_sentence, id_list = [], []
        for sentence, speaker_id in tqdm(zip(data["SENTENCE"], data["SPEAKERID"]), total=len(data)):
            all_sentence.append(str(sentence))
            id_list.append(speaker_id)

        questions, answers = [], []
        i = 0
        while i < len(all_sentence):
            end = i + 1
            _id = id_list[i]
            if end >= len(all_sentence):
                break
            while end < len(all_sentence) and id_list[end] == _id:
                end += 1
            if _id == 1:
                try:
                    questions.append(" ".join(all_sentence[i:end]) + "</s>")
                except:
                    print(i, end)
                    break
            else:
                answers.append(" ".join(all_sentence[i:end]) + "</s>")
            i = end
        min_length = min(len(questions), len(answers))
        question_lists.extend(questions[:min_length])
        answer_lists.extend(answers[:min_length])
        for i in range(min_length):
            all_data.append(questions[i])
            all_data.append(answers[i])

    with open(SAVE_PATH, 'wt', encoding='utf-8') as f:
        for line in all_data:
            f.write(line + "\n")


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--data_dir', required=True,
                        help="Your Data Directory Path")
    parser.add_argument('--save_file', required=True,
                        help="Save path extension : '.txt'")

    args = parser.parse_args()

    DATA_PATH = args.data_dir
    SAVE_PATH = args.save_file

    preprocessing(DATA_PATH, SAVE_PATH)


if __name__=="__main__":
    main()