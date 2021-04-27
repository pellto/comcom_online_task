import torch
from transformers import GPT2LMHeadModel, PreTrainedTokenizerFast


FINETUNE_MODEL_PATH = r"E:\online_task\KoGPT2_KoDialog_2.pt"
SERVICE_MODEL_PATH = r"E:\online_task\service_conversation\KoGPT2_KoDialog_2.pt"


MODEL = GPT2LMHeadModel.from_pretrained("taeminlee/kogpt2")
TOKENIZER = PreTrainedTokenizerFast.from_pretrained("taeminlee/kogpt2")

KoGPT_2_MODEL = GPT2LMHeadModel.from_pretrained("taeminlee/kogpt2")
KoGPT_2_MODEL.load_state_dict(torch.load(FINETUNE_MODEL_PATH))

SERVICE_MODEL = GPT2LMHeadModel.from_pretrained("taeminlee/kogpt2")
SERVICE_MODEL.load_state_dict(torch.load(FINETUNE_MODEL_PATH))

def __str2tensor__(input_text):
    return TOKENIZER.encode(input_text, add_special_tokens=True, return_tensors="pt")


def generate_sentence_getter(args):
    data = __str2tensor__(args['input_text'])
    if args == "":
        return TOKENIZER.decode(MODEL.generate(data)[0], skip_special_tokens=True)
    return TOKENIZER.decode(MODEL.generate(data, **args)[0], skip_special_tokens=True)


def generate_answer_getter(args=""):
    data = __str2tensor__(args['input_text'])
    if args == "":
        return TOKENIZER.decode(KoGPT_2_MODEL.generate(data)[0], skip_special_tokens=True)
    return TOKENIZER.decode(KoGPT_2_MODEL.generate(data, **args)[0])


def generate_service_getter(args=""):
    data = __str2tensor__(args['input_text'])
    if args == "":
        return TOKENIZER.decode(SERVICE_MODEL.generate(data)[0], skip_special_tokens=True)
    return TOKENIZER.decode(SERVICE_MODEL.generate(data, **args)[0])

