import openai
import os
import json
from pathlib import Path
from langchain.document_loaders import UnstructuredFileLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.callbacks import StreamingStdOutCallbackHandler
from langchain.retrievers import WikipediaRetriever
from langchain.schema import BaseOutputParser, output_parser

BASE_DIR = Path(__file__).resolve().parent.parent

with open(BASE_DIR/'secrets.json') as f:
    secrets = json.loads(f.read())

os.environ['OPENAI_API_KEY']= secrets['OPENAI_API_KEY']

llm = ChatOpenAI(
    temperature=0.1,
    model="gpt-3.5-turbo-1106",
    streaming=True,
    callbacks=[StreamingStdOutCallbackHandler()],
)

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
    ]
)