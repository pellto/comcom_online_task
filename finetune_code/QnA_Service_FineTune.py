import os
import argparse

import torch
from tqdm import tqdm
from torch.utils.data import Dataset, DataLoader
from transformers import GPT2LMHeadModel, PreTrainedTokenizerFast
from transformers import AdamW, get_linear_schedule_with_warmup


DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'


class ChatBotDataset(Dataset):
    def __init__(self, data_path, tokenizer):
        self.conversation = {}
        with open(data_path, 'rt', encoding='utf-8') as f:
            data = f.read().split("\n")[:-1]
            for i in range(0, len(data), 2):
                temp_conversation = tokenizer(data[i]+data[i+1])
                for key in temp_conversation:
                    if key not in self.conversation:
                        self.conversation[key] = []
                    self.conversation[key].append(temp_conversation[key])

    def __len__(self):
        return len(self.conversation['input_ids'])

    def __getitem__(self, idx):
        return {key: torch.tensor(val[idx]) for key, val in self.conversation.items()}


def batch_padder(batch):
    max_length = -1
    pad_token_id = 3
    train_ids, attention_mask = [], []
    for data in batch:
        max_length = max(max_length, len(data['input_ids']))

    for i in range(len(batch)):
        train_ids.append(torch.cat([batch[i]["input_ids"],
                                           torch.LongTensor([pad_token_id] * (max_length - len(batch[i]["input_ids"])))]))
        attention_mask.append(torch.cat([batch[i]["attention_mask"],
                                           torch.LongTensor([0] * (max_length - len(batch[i]["attention_mask"])))]))
    return torch.stack(train_ids, 0), torch.stack(attention_mask, 0)


def get_data_loader(data_path, tokenizer, batch_size=4, shuffle=True):
    dataset = ChatBotDataset(data_path, tokenizer)
    dataloader = DataLoader(dataset, batch_size=batch_size,
                            collate_fn=batch_padder, shuffle=shuffle)
    return dataloader


def fine_tuning_runner(model, optim, data_loader, scheduler, epochs, save_path):
    model = model.to(DEVICE)
    model.train()
    print("=" * 15, "TRAIN MODEL", "=" * 15)
    for epoch in range(epochs):
        print(f'EPOCH : {epoch}, started' + "=" * 30)
        total_loss = 0.0
        total_count = 0
        with tqdm(data_loader, desc="Train Epoch #{}".format(epoch)) as t:
            for train_ids, attention_masks in t:
                train_ids, attention_masks = train_ids.to(DEVICE), attention_masks.to(DEVICE)
                outputs = model(train_ids, attention_mask=attention_masks, labels=train_ids)
                loss = outputs[0]

                total_loss += loss.detach().data
                total_count += 1
                t.set_postfix(loss='{:.6f}'.format(total_loss / total_count))
                optim.zero_grad()
                scheduler.optimizer.zero_grad()
                loss.backward()
                optim.step()
                scheduler.step()

        model.save_pretrained(os.path.join(save_path, f"epoch_{epoch}"))


def fine_tuning(MODEL_TYPE, DATA_PATH, BATCH_SIZE,
                LEARNING_RATE, WARMUP_STEPS, OUTPUT_MODEL_PATH, EPOCHS):
    print("=" * 15, "LOAD MODEL", "=" * 15)
    model = GPT2LMHeadModel.from_pretrained(MODEL_TYPE)
    tokenizer = PreTrainedTokenizerFast.from_pretrained(MODEL_TYPE)

    print("=" * 15, "GET DATASET", "=" * 15)
    data_loader = get_data_loader(DATA_PATH, tokenizer, BATCH_SIZE, True)

    optimizier = AdamW(model.parameters(), lr=LEARNING_RATE)
    scheduler = get_linear_schedule_with_warmup(optimizier, WARMUP_STEPS, len(data_loader) - WARMUP_STEPS, -1)

    if not os.path.exists(OUTPUT_MODEL_PATH):
        os.mkdir(OUTPUT_MODEL_PATH)

    fine_tuning_runner(model, optimizier, data_loader, scheduler, EPOCHS, OUTPUT_MODEL_PATH)
    model.save_pretrained(OUTPUT_MODEL_PATH)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--model_save_path', required=True,
                        help="Save fine-tuned Model path")
    parser.add_argument('--data_path', required=True,
                        help="Setting your data_path for fine-tuning KoGPT-2")
    parser.add_argument('--batch_size', default=8, type=int,
                        help="The number of data belonging to per iter (default:4)")
    parser.add_argument('--epochs', default=3, type=int,
                        help="The number of train epochs (default:3")
    parser.add_argument('--lr', default=3e-5, type=float,
                        help="learning rate range lr < 1")
    parser.add_argument('--warm_up', default=100, type=int,
                        help="Setting Warm_up steps for scheduler in your data-set")
    parser.add_argument('--base_model', default='taeminlee/kogpt2',
                        help="pretrained KoGPT-2 model path in Huggingface")

    args = parser.parse_args()

    BATCH_SIZE = args.batch_size
    EPOCHS = args.epochs
    LEARNING_RATE = args.lr
    WARMUP_STEPS = args.warm_up
    DATA_PATH = args.data_path
    MODEL_TYPE = args.base_model
    OUTPUT_FOLDER = args.model_save_path

    fine_tuning(MODEL_TYPE=MODEL_TYPE, DATA_PATH=DATA_PATH, BATCH_SIZE=BATCH_SIZE,
                LEARNING_RATE=LEARNING_RATE, WARMUP_STEPS=WARMUP_STEPS, OUTPUT_MODEL_PATH=OUTPUT_FOLDER, EPOCHS=EPOCHS)


if __name__=="__main__":
    main()