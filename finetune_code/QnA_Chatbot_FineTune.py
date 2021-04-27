import os

import torch
from tqdm import tqdm
from torch.utils.data import Dataset, DataLoader
from transformers import GPT2LMHeadModel, PreTrainedTokenizerFast
from transformers import AdamW, get_linear_schedule_with_warmup


class ServiceConversationDataset(Dataset):
    def __init__(self, data_path):
        self.conversation_data = []
        with open(data_path, 'rt', encoding='utf-8') as f:
            data = f.read().split("\n")
            for line in data:
                self.conversation_data.append("<s> " + line.replace("`", " <s> ") + " </s>")

    def __len__(self):
        return len(self.conversation_data)

    def __getitem__(self, idx):
        return self.conversation_data[idx]


device = 'cpu'
if torch.cuda.is_available():
    device = 'cuda'


if __name__=="__main__":
    BATCH_SIZE = 4
    EPOCHS = 3
    LEARNING_RATE = 3e-5
    WARMUP_STEPS = 100
    MAX_SEQ_LEN = 100
    DATA_PATH = r"E:\dialog\all_data.txt"
    MODEL_TYPE = "taeminlee/kogpt2"
    OUTPUT_MODEL_PATH = r"E:\online_task\service_conversation"

    print("="*15, "LOAD MODEL", "="*15)
    model = GPT2LMHeadModel.from_pretrained(MODEL_TYPE)
    tokenizer = PreTrainedTokenizerFast.from_pretrained(MODEL_TYPE)

    print("=" * 15, "GET DATASET", "=" * 15)
    dataset = ServiceConversationDataset(DATA_PATH)
    data_loader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)

    print("=" * 15, "MODEL ATTACH", "=" * 15)
    model = model.to(device)

    model.train()
    optimizier = AdamW(model.parameters(), lr=LEARNING_RATE)
    scheduler = get_linear_schedule_with_warmup(optimizier, WARMUP_STEPS, len(data_loader) - WARMUP_STEPS, -1)

    if not os.path.exists(OUTPUT_MODEL_PATH):
        os.mkdir(OUTPUT_MODEL_PATH)

    print("=" * 15, "TRAIN MODEL", "=" * 15)
    start_token = torch.tensor(tokenizer.encode("<s>")).unsqueeze(0)
    unknown_token = tokenizer.unk_token_id

    for epoch in range(EPOCHS):
        print(f'EPOCH : {epoch}, started' + "=" * 30)
        proc_seq_count = 0
        total_loss = 0.0
        total_count =0
        with tqdm(data_loader, desc="Train Epoch #{}".format(epoch)) as t:
            for idx, data in enumerate(t):
                train_ids = tokenizer.encode(data[0])

                for i, token in enumerate(train_ids):
                    if token >= tokenizer.vocab_size:
                        train_ids[i] = unknown_token
                train_ids = torch.tensor(train_ids).to(device)
                outputs = model(train_ids, labels=train_ids)
                loss, logits = outputs[:2]
                loss.backward()
                total_loss += loss.detach().data
                total_count += 1
                t.set_postfix(loss='{:.6f}'.format(total_loss / total_count))
                optimizier.step()
                scheduler.step()
                optimizier.zero_grad()
                scheduler.optimizer.zero_grad()

                if idx % 5000 == 1:
                    torch.save(model.state_dict(), os.path.join(OUTPUT_MODEL_PATH, f"KoGPT2_KoDialog_{epoch}_{idx}.pt"))
            torch.save(model.state_dict(), os.path.join(OUTPUT_MODEL_PATH, f"KoGPT2_KoDialog_{epoch}.pt"))