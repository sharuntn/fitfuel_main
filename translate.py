from transformer import Transformer
import torch
import numpy as np

tokens = ['h', 'o', 'w', ' ', 'd', 'i', 's', 't', 'p', 'm', 'k', 'n', 'g', 'a', 'u', 'b', 'l', '4', 'y', 'e', 'r', 'v', 'c', 'f', '2', '7', '3', '?', 'x', '-', '5', '"', '&', '1', '9', '(', ')', "'", '0', '!', 'j', '\\', ':', '6', '<', '_', '>', 'q', 'z', '8', '/', ';', '%', '’', '–', '…', '“', '”', '‘', '+', 'é', 'â', '\x80', '\x99', '\x98', '\x94', '\x93', '\x9c', '\x9d', '¦', 'î', '±', '\u200b', '̇', '🙂', '،', '=', '—', '℅', '<START>', '<END>', '<PAD>']
lang_to_index = {'h': 0, 'o': 1, 'w': 2, ' ': 3, 'd': 4, 'i': 5, 's': 6, 't': 7, 'p': 8, 'm': 9, 'k': 10, 'n': 11, 'g': 12, 'a': 13, 'u': 14, 'b': 15, 'l': 16, '4': 17, 'y': 18, 'e': 19, 'r': 20, 'v': 21, 'c': 22, 'f': 23, '2': 24, '7': 25, '3': 26, '?': 27, 'x': 28, '-': 29, '5': 30, '"': 31, '&': 32, '1': 33, '9': 34, '(': 35, ')': 36, "'": 37, '0': 38, '!': 39, 'j': 40, '\\': 41, ':': 42, '6': 43, '<': 44, '_': 45, '>': 46, 'q': 47, 'z': 48, '8': 49, '/': 50, ';': 51, '%': 52, '’': 53, '–': 54, '…': 55, '“': 56, '”': 57, '‘': 58, '+': 59, 'é': 60, 'â': 61, '\x80': 62, '\x99': 63, '\x98': 64, '\x94': 65, '\x93': 66, '\x9c': 67, '\x9d': 68, '¦': 69, 'î': 70, '±': 71, '\u200b': 72, '̇': 73, '🙂': 74, '،': 75, '=': 76, '—': 77, '℅': 78, '<START>': 79, '<END>': 80, '<PAD>': 81}
index_to_lang = {0: 'h', 1: 'o', 2: 'w', 3: ' ', 4: 'd', 5: 'i', 6: 's', 7: 't', 8: 'p', 9: 'm', 10: 'k', 11: 'n', 12: 'g', 13: 'a', 14: 'u', 15: 'b', 16: 'l', 17: '4', 18: 'y', 19: 'e', 20: 'r', 21: 'v', 22: 'c', 23: 'f', 24: '2', 25: '7', 26: '3', 27: '?', 28: 'x', 29: '-', 30: '5', 31: '"', 32: '&', 33: '1', 34: '9', 35: '(', 36: ')', 37: "'", 38: '0', 39: '!', 40: 'j', 41: '\\', 42: ':', 43: '6', 44: '<', 45: '_', 46: '>', 47: 'q', 48: 'z', 49: '8', 50: '/', 51: ';', 52: '%', 53: '’', 54: '–', 55: '…', 56: '“', 57: '”', 58: '‘', 59: '+', 60: 'é', 61: 'â', 62: '\x80', 63: '\x99', 64: '\x98', 65: '\x94', 66: '\x93', 67: '\x9c', 68: '\x9d', 69: '¦', 70: 'î', 71: '±', 72: '\u200b', 73: '̇', 74: '🙂', 75: '،', 76: '=', 77: '—', 78: '℅', 79: '<START>', 80: '<END>', 81: '<PAD>'}

START_TOKEN = '<START>'
END_TOKEN = '<END>'
PADDING_TOKEN = '<PAD>'

d_model = 512
max_sequence_length = 460
ffn_hidden = 2048
num_heads = 8
drop_prob = 0.1
num_layers = 1
vocab_size = len(tokens)
device = 'cuda' if torch.cuda.is_available() else 'cpu'

transformer = Transformer(d_model,ffn_hidden,num_heads,drop_prob,num_layers,max_sequence_length,vocab_size,lang_to_index,lang_to_index,START_TOKEN,END_TOKEN,PADDING_TOKEN)

transformer.load_state_dict(torch.load('prototype_600.pth',map_location=torch.device('cpu')))

NEG_INFTY = -1e9

def create_masks(eng_batch, kn_batch):
    num_sentences = len(eng_batch)
    look_ahead_mask = torch.full([max_sequence_length, max_sequence_length] , True)
    look_ahead_mask = torch.triu(look_ahead_mask, diagonal=1)
    encoder_padding_mask = torch.full([num_sentences, max_sequence_length, max_sequence_length] , False)
    decoder_padding_mask_self_attention = torch.full([num_sentences, max_sequence_length, max_sequence_length] , False)
    decoder_padding_mask_cross_attention = torch.full([num_sentences, max_sequence_length, max_sequence_length] , False)

    for idx in range(num_sentences):
      eng_sentence_length, kn_sentence_length = len(eng_batch[idx]), len(kn_batch[idx])
      eng_chars_to_padding_mask = np.arange(eng_sentence_length + 1, max_sequence_length)
      kn_chars_to_padding_mask = np.arange(kn_sentence_length + 1, max_sequence_length)
      encoder_padding_mask[idx, :, eng_chars_to_padding_mask] = True
      encoder_padding_mask[idx, eng_chars_to_padding_mask, :] = True
      decoder_padding_mask_self_attention[idx, :, kn_chars_to_padding_mask] = True
      decoder_padding_mask_self_attention[idx, kn_chars_to_padding_mask, :] = True
      decoder_padding_mask_cross_attention[idx, :, eng_chars_to_padding_mask] = True
      decoder_padding_mask_cross_attention[idx, kn_chars_to_padding_mask, :] = True

    encoder_self_attention_mask = torch.where(encoder_padding_mask, NEG_INFTY, 0)
    decoder_self_attention_mask =  torch.where(look_ahead_mask + decoder_padding_mask_self_attention, NEG_INFTY, 0)
    decoder_cross_attention_mask = torch.where(decoder_padding_mask_cross_attention, NEG_INFTY, 0)
    return encoder_self_attention_mask, decoder_self_attention_mask, decoder_cross_attention_mask



def translate(text):
  transformer.eval()
  q = (text,)
  a = ("",)
  for word_counter in range(max_sequence_length):
    encoder_self_attention_mask, decoder_self_attention_mask, decoder_cross_attention_mask= create_masks(q, a)
    predictions = transformer(q,
                              a,
                              encoder_self_attention_mask.to(device),
                              decoder_self_attention_mask.to(device),
                              decoder_cross_attention_mask.to(device),
                              enc_start_token=False,
                              enc_end_token=False,
                              dec_start_token=True,
                              dec_end_token=False)
    next_token_prob_distribution = predictions[0][word_counter]
    next_token_index = torch.argmax(next_token_prob_distribution).item()
    next_token = index_to_lang[next_token_index]
    a = (a[0] + next_token, )
    if next_token == END_TOKEN:
      break
  return a[0][:-5]

if __name__ == "__main__":

        text =input("enter the query")
        answer = translate(text=text.lower())
        print(f'prediction: {answer}')