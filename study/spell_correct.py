# 패키지 설치
# !pip install konlpy

# 자세한 사용방법은 노션 "AI통합 구현 및 통합>맞춤법 수정 모듈"
# 맞춤법 검사 및 정답 체크 소요 시간이 대략 20~30초 정도 소요됨

import torch
from transformers import PreTrainedTokenizerFast
from transformers import BartForConditionalGeneration
from konlpy.tag import Komoran

def korean_pos_tagging(sentence):
    komoran = Komoran()
    morphs_tags = komoran.morphs(sentence)
    return morphs_tags

def is_correct(sentence, words):
    # 모델 다운받기
    tokenizer = PreTrainedTokenizerFast.from_pretrained('Soyoung97/gec_kr')
    model = BartForConditionalGeneration.from_pretrained('Soyoung97/gec_kr')
    
    # 해당 단어가 문장에 들어가 있는지부터 확인하기
    sentence_k=korean_pos_tagging(sentence)

    cnt=0
    for word in words:
        word_k=korean_pos_tagging(word)
        if word_k[0] in sentence_k:
            cnt+=1

    # 선택한 단어 개수 이상의 단어가 들어가 있지 않은 경우
    if cnt < len(words):
        return {'answer':False, 'text': '현재 '+str(cnt)+'개의 단어가 포함되어 있습니다. 단어를 추가해주세요.'}

    # 들어가 있다면 문법적으로 맞는 문장인지 확인하기
    else:
        raw_input_ids = tokenizer.encode(sentence)
        input_ids = [tokenizer.bos_token_id] + raw_input_ids + [tokenizer.eos_token_id]
        corrected_ids = model.generate(torch.tensor([input_ids]),
                                max_length=128,
                                eos_token_id=1, num_beams=4,
                                early_stopping=True, repetition_penalty=2.0)
        cor_result=tokenizer.decode(corrected_ids.squeeze().tolist(), skip_special_tokens=True)

        if cor_result==sentence:
            return {'answer':True, 'text': '\"'+ sentence+'\"는 올바른 문장입니다.'}
        else:
            return {'answer':False, 'text': '\"'+ sentence+'\"는 교정이 필요한 문장입니다.\n\n\"'+ cor_result + '\"로 수정해 보세요.'}