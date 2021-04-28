import torch
from transformers import GPT2LMHeadModel, PreTrainedTokenizerFast


QnA_Chatbot_Path = "./models/KoGPT2_QnAChatbot.pt"
Simple_QnA_Path = "./models/KoGPT2_SimpleQnA.pt"

MODEL = GPT2LMHeadModel.from_pretrained("taeminlee/kogpt2")
TOKENIZER = PreTrainedTokenizerFast.from_pretrained("taeminlee/kogpt2")

Simple_QnA_Model = GPT2LMHeadModel.from_pretrained("taeminlee/kogpt2")
Simple_QnA_Model.load_state_dict(torch.load(Simple_QnA_Path))

QnA_Chatbot_Model = GPT2LMHeadModel.from_pretrained("taeminlee/kogpt2")
QnA_Chatbot_Model.load_state_dict(torch.load(QnA_Chatbot_Path))


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
        return TOKENIZER.decode(Simple_QnA_Model.generate(data)[0], skip_special_tokens=True)
    return TOKENIZER.decode(Simple_QnA_Model.generate(data, **args)[0])


def generate_service_getter(args=""):
    data = __str2tensor__(args['input_text'])
    if args == "":
        return TOKENIZER.decode(QnA_Chatbot_Model.generate(data)[0], skip_special_tokens=True)
    return TOKENIZER.decode(QnA_Chatbot_Model.generate(data, **args)[0])

