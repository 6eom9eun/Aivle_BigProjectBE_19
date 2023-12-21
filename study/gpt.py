from pathlib import Path
from langchain.document_loaders import UnstructuredFileLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.callbacks import StreamingStdOutCallbackHandler
from langchain.retrievers import WikipediaRetriever
from langchain.schema import BaseOutputParser, output_parser
import openai
import os
import json

BASE_DIR = Path(__file__).resolve().parent.parent

with open(BASE_DIR/'secrets.json') as f:
    secrets = json.loads(f.read())

os.environ['OPENAI_API_KEY']= secrets['OPENAI_API_KEY']

class JsonOutputParser(BaseOutputParser):
    def parse(self, text):
        text = text.replace("```", "").replace("json", "")
        return json.loads(text)

def make_sentence(word, meaning):
    # Chatgpt 모델 불러오기
    llm = ChatOpenAI(
        temperature=0.1,
        model="gpt-3.5-turbo-1106",
        streaming=True,
        callbacks=[StreamingStdOutCallbackHandler()],
    )    
    
    # JSON 파서 가져오기
    output_parser = JsonOutputParser()
    
    # 문장을 만들어줄 프롬프트
    sentence_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
                너는 문해력 수업을 진행하는 선생님이야.

                주어진 단어와 주어진 단어의 뜻에 기반하여 지문을 만들거야.
		        만든 지문에는 반드시 주어진 단어가 주어진 뜻으로 쓰여야 해.
                그리고 해당 단어가 반드시 지문에 들어가 있어야 해

                주어진 단어는 "{word}" 이고, 단어의 뜻은 "{meaning}" 이야.

                지문은 단어 당 3개씩 만들어주면 돼.

                그리고 반드시 예시문 형식에 맞춰 작성해줘

                예시문 :

                Sentence1: 우리는 항상 자기계발을 통해 지속적인 성장과 개선을 추구해야 합니다.
                Sentence2: 회사 내 모든 직원들은 제품 품질의 개선과 고객 만족도 향상에 최선을 다해야 합니다.
		        Sentence3: 협력사와의 원활한 의사소통을 통해 생산 공정에 대한 개선 방안을 공유할 수 있을 것이다.

                Sentence1: 심심한 마음을 달래기 위해 책을 읽으며 시간을 보내고 있다.
                Sentence2: 나는 심심한 마음을 달래기 위해 우리 가족과 함께 영화를 보았다.
		        Sentence3: 그는 심심한 마음을 달래기 위해 사무실에서 일하다가도 가끔씩 창밖을 내다보곤 한다.

                너의 차례야!
            """,
        )
    ])
    
    # 만든 프롬프트를 LLM에 적용하기
    sentences_chain = sentence_prompt | llm

    # JSON 파일로 변환할 프롬프트
    formatting_prompt = ChatPromptTemplate.from_messages(
    [
        (
        "system",
        """
            You are a powerful formatting algorithm.

            You format questions into JSON format.

            You must follow this examples.

            Example Input:

	        우리는 항상 자기계발을 통해 지속적인 성장과 개선을 추구해야 합니다.
	        회사 내 모든 직원들은 제품 품질의 개선과 고객 만족도 향상에 최선을 다해야 합니다.
	        협력사와의 원활한 의사소통을 통해 생산 공정에 대한 개선 방안을 공유할 수 있을 것이다.

            심심한 마음을 달래기 위해 책을 읽으며 시간을 보내고 있다.
            나는 심심한 마음을 달래기 위해 우리 가족과 함께 영화를 보았다.
	        그는 심심한 마음을 달래기 위해 사무실에서 일하다가도 가끔씩 창밖을 내다보곤 한다.


            Example Output:

            ```json
            {{ "sentences": [
                    {{ text: [
                        "우리는 항상 자기계발을 통해 지속적인 성장과 개선을 추구해야 합니다.",
                        "회사 내 모든 직원들은 제품 품질의 개선과 고객 만족도 향상에 최선을 다해야 합니다.",
                        "협력사와의 원활한 의사소통을 통해 생산 공정에 대한 개선 방안을 공유할 수 있을 것이다."]
                    }},
                    {{
                        text: [
                            "심심한 마음을 달래기 위해 책을 읽으며 시간을 보내고 있다.",
                            "나는 심심한 마음을 달래기 위해 우리 가족과 함께 영화를 보았다.",
                            "그는 심심한 마음을 달래기 위해 사무실에서 일하다가도 가끔씩 창밖을 내다보곤 한다."
                        ]
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

    # 최종 체인 생성
    chain = {"context": sentences_chain} | formatting_chain | output_parser
    
    response=chain.invoke({"word":word, "meaning":meaning})
    
    return response
    

# 문제 만들기
def make_problem(word, meaning):
    # Chatgpt 모델 불러오기
    llm = ChatOpenAI(
        temperature=0.1,
        model="gpt-3.5-turbo-1106",
        streaming=True,
        callbacks=[StreamingStdOutCallbackHandler()],
    )    
    
    # JSON 파서 가져오기
    output_parser = JsonOutputParser()
    
    # 문장을 만들어줄 프롬프트
    questions_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
                너는 문해력 문제를 출제하는 선생님이야.

                주어진 단어와 주어진 단어의 뜻에 기반하여 지문을 만들고,
                지문에서 주어진 단어가 어떤 의미로 사용되었는지 물어볼거야.

                주어진 단어는 {word} 이고, 단어의 뜻은 {meaning}이야.

                Sentence: {word}가 {meaning}을 의미를 가지도록 문장을 생성한다.
                Question: 위 문장에서 '{word}'가 의미하는 바는 무엇인가요?
                Answers: 4개의 선택지, 1개만 정답이고, 다른 3개는 정답이 아니고 절대 유사한 뜻을 가지지 않는다.

                (O)를 사용해서 정답을 표시해줘

                예시문 :

                Sentence: 부상을 방지하기 위해 달리기 전에 항상 준비운동을 해야한다.
                Question: 위 문장에서 '방지하다'이 의미하는 바는 무엇인가요?
                Answers: 다침|죽음|예방(O)|승인

                Sentence: 특정 지역에서 통용되는 지역 화폐의 명칭을 알아보자
                Question: 위 문장에서 '통용하다'이 의미하는 바는 무엇인가요?
                Answers: 지나감|사용(O)|개선|윤리

                너의 차례야!
            """,
        )
    ])
    
    # 만든 프롬프트를 LLM에 적용하기
    questions_chain = questions_prompt | llm
    
    # JSON 파일로 변환할 프롬프트
    formatting_prompt = ChatPromptTemplate.from_messages(
    [
        (
        "system",
        """
            You are a powerful formatting algorithm.

            You format exam questions  into JSON format.
            Answers with (o) are the correct ones.

            Example Input:

            Sentence: 어릴 적부터 그의 꿈은 작곡가가 되는 것이었다.
            Question: 위 문장에서 '작곡가'가 의미하는 바는 무엇인가요?
            Answers: 음악을 연주하는 사람|음악을 쓰는 사람(O)|음악을 감상하는 사람|음악을 가르치는 사람

            Sentence: 그 영화는 감동적인 이야기와 아름다운 비주얼로 관객들의 마음을 사로잡았다.
            Question: 위 문장에서 '비주얼'이 의미하는 바는 무엇인가요?
            Answers: 사운드|캐스팅|영상 효과|시각적인 요소를 포함한 영상(O)


            Example Output:

            ```json
            {{ "questions": [
                    {{
                        "Sentence": "어릴 적부터 그의 꿈은 작곡가가 되는 것이었다.",
                        "question": "위 문장에서 '작곡가'가 의미하는 바는 무엇인가요?",
                        "answers": [
                                {{
                                    "answer": "음악을 연주하는 사람",
                                    "correct": false
                                }},
                                {{
                                    "answer": "음악을 쓰는 사람",
                                    "correct": true
                                }},
                                {{
                                    "answer": "음악을 감상하는 사람",
                                    "correct": false
                                }},
                                {{
                                    "answer": "음악을 가르치는 사람",
                                    "correct": false
                                }}
                        ]
                    }},
                                {{
                        "Sentence": "그 영화는 감동적인 이야기와 아름다운 비주얼로 관객들의 마음을 사로잡았다.",
                        "question": "위 문장에서 '비주얼'이 의미하는 바는 무엇인가요?",
                        "answers": [
                                {{
                                    "answer": "사운드",
                                    "correct": false
                                }},
                                {{
                                    "answer": "캐스팅",
                                    "correct": false
                                }},
                                {{
                                    "answer": "영상 효과",
                                    "correct": false
                                }},
                                {{
                                    "answer": "시각적인 요소를 포함한 영상",
                                    "correct": true
                                }}
                        ]
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

    # 최종 체인 생성
    chain = {"context": questions_chain} | formatting_chain | output_parser
    
    response=chain.invoke({"word":word, "meaning":meaning})
    
    return response
    