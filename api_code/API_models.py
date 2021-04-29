import torch
from transformers import GPT2LMHeadModel, PreTrainedTokenizerFast


DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

Chatbot_Path = "./models/Kodialog_Chatbot.pt"
Simple_QnA_Path = "./models/Kodialog_SimpleQnA.pt"

MODEL = GPT2LMHeadModel.from_pretrained("taeminlee/kogpt2")
TOKENIZER = PreTrainedTokenizerFast.from_pretrained("taeminlee/kogpt2")

Simple_QnA_Model = GPT2LMHeadModel.from_pretrained("taeminlee/kogpt2")
Simple_QnA_Model.load_state_dict(torch.load(Simple_QnA_Path, map_location=torch.device(DEVICE)))

Chatbot_Model = GPT2LMHeadModel.from_pretrained("taeminlee/kogpt2")
Chatbot_Model.load_state_dict(torch.load(Chatbot_Path, map_location=torch.device(DEVICE)))


def __str2tensor__(input_text):
    return TOKENIZER.encode(input_text, add_special_tokens=True, return_tensors="pt")


def generate_sentence_getter(args):
    data = __str2tensor__(args['input_text'])
    params = {"max_length":args['max_length'],
    "early_stopping":True,
    "top_k":100,
    "top_p":0.92,
    "repetition_penalty":1.1}
    if args == "":
        return TOKENIZER.decode(MODEL.generate(data)[0], skip_special_tokens=True)
    return TOKENIZER.decode(MODEL.generate(data, **params)[0], skip_special_tokens=True)


def generate_simple_getter(args=""):
    data = __str2tensor__(args['input_text'])
    params = {"max_length": args['max_length'],
              "early_stopping": True,
              "top_k": 100,
              "top_p": 0.92,
              "repetition_penalty": 1.1}
    if args == "":
        return TOKENIZER.decode(Simple_QnA_Model.generate(data)[0], skip_special_tokens=True)
    return TOKENIZER.decode(Simple_QnA_Model.generate(data, **params)[0], skip_special_tokens=True)


def generate_bot_answer_getter(args=""):
    data = __str2tensor__(args['input_text'])
    params = {"max_length": args['max_length'],
              "early_stopping": True,
              "top_k": 100,
              "top_p": 0.92,
              "repetition_penalty": 1.1}
    if args == "":
        return TOKENIZER.decode(Chatbot_Model.generate(data)[0], skip_special_tokens=True)
    return TOKENIZER.decode(Chatbot_Model.generate(data, **params)[0], skip_special_tokens=True)

