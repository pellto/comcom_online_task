import os
import csv
import argparse

import torch
from tqdm import tqdm
from torch.utils.data import Dataset, DataLoader
from transformers import GPT2LMHeadModel, PreTrainedTokenizerFast
from transformers import AdamW, get_linear_schedule_with_warmup


class ConversationDataset(Dataset):
    def __init__(self, data_path, tokenizer, max_length):
        self.conversation_data = []
        self.end_of_text_token = "</s>"
        unknown_token = tokenizer.unk_token_id

        header = 0
        with open(data_path, encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')

            for row in csv_reader:
                if header == 0:
                    header += 1
                    continue
                _type = ["일상", "부정", "긍정"][int(row[2])]

                temp_conversation = tokenizer.encode(f"{row[0]} {row[1]} {self.end_of_text_token}")
                for i in range(len(temp_conversation)):
                    if temp_conversation[i] > tokenizer.vocab_size:
                        temp_conversation[i] = unknown_token

                if len(temp_conversation) > max_length:
                    temp_conversation = temp_conversation[:max_length]
                else:
                    temp_conversation = temp_conversation + [tokenizer.pad_token_id] * (max_length -
                                                                                        len(temp_conversation))
                temp_conversation = torch.tensor(temp_conversation)
                self.conversation_data.append(temp_conversation)

    def __len__(self):
        return len(self.conversation_data)

    def __getitem__(self, idx):
        return self.conversation_data[idx]


DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'


def fine_tuning(MODEL_TYPE, DATA_PATH, MAX_SEQ_LEN, BATCH_SIZE,
                LEARNING_RATE, WARMUP_STEPS, OUTPUT_FOLDER, EPOCHS):
    print("=" * 15, "LOAD MODEL", "=" * 15)
    model = GPT2LMHeadModel.from_pretrained(MODEL_TYPE)
    tokenizer = PreTrainedTokenizerFast.from_pretrained(MODEL_TYPE)

    print("=" * 15, "GET DATASET", "=" * 15)
    dataset = ConversationDataset(data_path=DATA_PATH, tokenizer=tokenizer, max_length=MAX_SEQ_LEN)
    data_loader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)

    print("=" * 15, "MODEL ATTACH", "=" * 15)
    model = model.to(DEVICE)

    model.train()
    optimizier = AdamW(model.parameters(), lr=LEARNING_RATE)
    scheduler = get_linear_schedule_with_warmup(optimizier, WARMUP_STEPS, len(data_loader) - WARMUP_STEPS, -1)

    if not os.path.exists(OUTPUT_FOLDER):
        os.mkdir(OUTPUT_FOLDER)

    print("=" * 15, "TRAIN MODEL", "=" * 15)
    for epoch in range(EPOCHS):
        print(f'EPOCH : {epoch}, started' + "=" * 30)
        total_loss = 0.0
        total_count = 0
        with tqdm(data_loader, desc="Train Epoch #{}".format(epoch)) as t:
            for idx, train_ids in enumerate(t):
                train_ids = train_ids.to(DEVICE)
                outputs = model(train_ids, labels=train_ids)

                loss = outputs[0]
                total_loss += loss.detach().data
                total_count += 1
                t.set_postfix(loss='{:.6f}'.format(total_loss / total_count))
                optimizier.zero_grad()
                scheduler.optimizer.zero_grad()
                loss.backward()
                optimizier.step()
                scheduler.step()

                if idx % 2000 == 1:
                    torch.save(model.state_dict(), os.path.join(OUTPUT_FOLDER, f"KoGPT2_KoDialog_{epoch}_{idx}.pt"))

            torch.save(model.state_dict(), os.path.join(OUTPUT_FOLDER, f"KoGPT2_KoDialog_{epoch}.pt"))


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--model_save_path', required=True,
                        help="Save fine-tuned Model path")
    parser.add_argument('--data_path', required=True,
                        help="Setting your data_path for fine-tuning KoGPT-2")
    parser.add_argument('--batch_size', default=4,
                        help="The number of data belonging to per iter (default:4)")
    parser.add_argument('--epochs', default=3,
                        help="The number of train epochs (default:3")
    parser.add_argument('--lr', default=3e-5,
                        help="learning rate range lr < 1")
    parser.add_argument('--warm_up', default=100,
                        help="Setting Warm_up steps for scheduler in your data-set")
    parser.add_argument('--base_model', default='taeminlee/kogpt2',
                        help="pretrained KoGPT-2 model path in Huggingface")
    parser.add_argument('--max_length', default=100,
                        help="Setting max_sequence length in encoded tensor length")

    args = parser.parse_args()

    BATCH_SIZE = args.batch_size
    EPOCHS = args.epochs
    LEARNING_RATE = args.lr
    WARMUP_STEPS = args.warm_up
    MAX_SEQ_LEN = args.max_length
    DATA_PATH = args.data_path
    MODEL_TYPE = args.base_model
    OUTPUT_FOLDER = args.model_save_path
    fine_tuning(MODEL_TYPE=MODEL_TYPE, DATA_PATH=DATA_PATH, MAX_SEQ_LEN=MAX_SEQ_LEN, BATCH_SIZE=BATCH_SIZE,
                LEARNING_RATE=LEARNING_RATE, WARMUP_STEPS=WARMUP_STEPS, OUTPUT_FOLDER=OUTPUT_FOLDER, EPOCHS=EPOCHS)


if __name__=="__main__":
    main()
