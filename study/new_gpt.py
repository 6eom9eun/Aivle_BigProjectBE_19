from pathlib import Path
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.callbacks import StreamingStdOutCallbackHandler
from langchain.schema import BaseOutputParser, output_parser
from langchain.output_parsers import CommaSeparatedListOutputParser
import numpy as np
import pandas as pd
import openai
import os
import json
from .models import Word, Quiz

BASE_DIR = Path(__file__).resolve().parent.parent

with open(BASE_DIR/'secrets.json') as f:
    secrets = json.loads(f.read())

os.environ['OPENAI_API_KEY']= secrets['OPENAI_API_KEY']

class JsonOutputParser(BaseOutputParser):
    def parse(self, text):
        text = text.replace("```", "").replace("json", "")
        return json.loads(text)

# GPT AI를 활용한 문장 생성하기
def make_sentence(word, meaning):
    # 파인튜닝 모델
    llm = ChatOpenAI(
        temperature=0.1,
        model="ft:gpt-3.5-turbo-0613:personal::8aG6fMiE",
        #model="gpt-3.5-turbo-1106",
        streaming=True,
        callbacks=[StreamingStdOutCallbackHandler()],
    )
    
    # JSON 파서 가져오기
    output_parser = JsonOutputParser()

    # 문장을 만들어 줄 프롬프트
    sentence_prompt = ChatPromptTemplate.from_messages([("system", """ Make 3 sentence using '{word}'""",)])
    
    # 체인 연결하기
    sentences_chain = sentence_prompt | llm
    
    # JSON 형식 변경 프롬프트
    formatting_prompt = ChatPromptTemplate.from_messages(
    [
        (
        "system",
        """
            You are a powerful formatting algorithm.

            You format questions into JSON format.

            You must follow this examples.

            Example Input:

            심심한 마음을 달래기 위해 책을 읽으며 시간을 보내고 있다. / 나는 심심한 마음을 달래기 위해 우리 가족과 함께 영화를 보았다. / 그는 심심한 마음을 달래기 위해 사무실에서 일하다가도 가끔씩 창밖을 내다보곤 한다.

            Example Output:

            ```json
            {{ "sentences": [
                    {{ text: [
                        "심심한 마음을 달래기 위해 책을 읽으며 시간을 보내고 있다.",
                        "나는 심심한 마음을 달래기 위해 우리 가족과 함께 영화를 보았다.",
                        "그는 심심한 마음을 달래기 위해 사무실에서 일하다가도 가끔씩 창밖을 내다보곤 한다."]
                    }},
                ]
            }}
            ```
            Your turn!

            Questions: {context}
        """,
        )
    ])
    
    # JSON 포멧으로 변환하는 모듈 생성
    formatting_chain = formatting_prompt | llm
    
    # 최종 체인 산출
    chain = {"context": sentences_chain} | formatting_chain | output_parser
    
    response=chain.invoke({"word":word, "meaning":meaning})
    
    return response

    

# 문제 만들기
def make_problem(word, meaning):
    # 파인튜닝 모델
    llm = ChatOpenAI(
        temperature=0.1,
        model="ft:gpt-3.5-turbo-0613:personal::8aG6fMiE",
        #model="gpt-3.5-turbo-1106",
        streaming=True,
        callbacks=[StreamingStdOutCallbackHandler()],
    )
    
    # 문장 생성 프롬프트(1개 생성)
    sent_prompt = ChatPromptTemplate.from_messages([("system", """ Make one sentence using '{word}'""",)])
    
    # 생성된 문장 List로 변환
    sentence_parser = CommaSeparatedListOutputParser()
    
    # 체인 생성
    sent_chain = sent_prompt | llm | sentence_parser
    
    # 임시 저장소
    result=dict()
    
    # 문장 만들기
    temp=sent_chain.invoke({"word":word})
    result['sentence']=temp[0]
    
    # 문제 만들기
    result['question']=f"위 문장에서 '{word}'가 의미하는 바는 무엇인가요?"
    
    # 보기 만들기
    content=[]
    content.append(meaning)   # 정답 보기 넣기
    
    # 데이터 프레임으로 해당 데이터 가져오기
    # # 랜덤으로 5개를 가져옴
    # random_rows=data.sample(n=5)
    # temp=random_rows['meaning'].tolist()
    # for i in range(len(temp)):
    #     # 보기 4개를 만들었다면
    #     if len(content)==4:
    #         break
    #     # 똑같은 뜻을 가지고 있다면
    #     elif meaning==temp[i]:
    #         continue
    #     # 보기에 추가 할 수 있다면
    #     else:
    #         content.append(temp[i])

    
    # 데이터베이스에서 활용하기
    for i in range(5):
        # 무작위로 뜻 불러오기
        random_word_entry = Word.objects.order_by('?').first()
        data_meaning = random_word_entry.meaning

        if len(content)==4:
            break
        elif meaning==data_meaning:
            continue
        else:
            content.append(data_meaning)
            
    # 보기를 무작위로 섞기
    np.random.shuffle(content)
    
    answers=[]
    for i in range(len(content)):
        # 정답일 경우
        if content[i]==meaning:
            answers.append({"answer":content[i], "correct": True})
        else:
            answers.append({"answer":content[i], "correct": False})

    new_format = {
        "questions": [
            {"Sentence":result['sentence'], "question":result['question'],"answers":answers}
        ]
    }

    return json.dumps(new_format, ensure_ascii=False)
    