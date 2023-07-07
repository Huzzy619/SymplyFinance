import json
import os

import openai
import requests
from dotenv import find_dotenv, load_dotenv
from langchain.utilities import GoogleSearchAPIWrapper 
from langchain.agents import AgentType, Tool, initialize_agent  
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI as LangchainOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.vectorstores import Chroma
from langchain.embeddings import AlephAlphaAsymmetricSemanticEmbedding, FakeEmbeddings
# import tiktoken

# Load environment variables
_ = load_dotenv(find_dotenv())
openai.api_key = "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"

os.environ["GOOGLE_CSE_ID"] = "55c1332fff9a840f0"
os.environ["GOOGLE_API_KEY"] = "AIzaSyCU6_DO5JWubdbBolU-ciATkPOclNCHTEI"

def finance(input):
    llm = LangchainOpenAI(temperature=0.1, openai_api_key="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")
    search = GoogleSearchAPIWrapper()
    # Creating a document loader
    loader = PyPDFLoader('Goldman-Sachs-annual-report-2022.pdf')
    pages = loader.load_and_split()
    # embeddings = AlephAlphaAsymmetricSemanticEmbedding()
    embeddings = FakeEmbeddings(size=4000)
    # embeddings = OpenAIEmbeddings()
    store = Chroma.from_documents(pages, embeddings, collection_name='annualreport')
    annual_report = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=store.as_retriever(), verbose=True)
    # Defining use of the Google SerperAPI Wrapper tool
    tools = [
        Tool(
            name= "Annual Report",
            func=annual_report.run,
            description="Search the annual report of a company",
        ),
        
        Tool(
            name="Intermediate Answer",
            func=search.run,
            description="Useful for when you need to ask with search."
        )
    ]
    agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
    # Set up ChatOpenAI model
    chat = ChatOpenAI(temperature=0, openai_api_key="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")
    # Defining investment-related system messages
    investment_system_messages = [
        SystemMessage(content="You are a friendly Stock/Financial analyst that  provides a detailed investment advice."),
        SystemMessage(content="Investing involves risks. It's important to do thorough research and consider professional advice."),
        SystemMessage(content="I can provide general and detailed information about investment strategies and concepts."),
        SystemMessage(content="You Provide highly profitable Financial/Investment Strategies")
    ]
    user_input = input
    conversation = [
        *investment_system_messages,
        HumanMessage(content=user_input)
    ]
    result = agent(conversation)
    response_text = result['output']
    return response_text


def bls(input):
    headers = {'Content-type': 'application/json'}
    data = json.dumps({"seriesid": ['CUUR0000SA0', 'SUUR0000SA0', 'LNS11000000', 'CES0500000007', 'CES0500000003', 'MPU4910012'
                                    'LNS13000000', 'LNS12000000', 'CES0000000001', 'CES0500000002', 'PRS85006092', 'PRS85006152'
                                    'LNS14000000', 'CES0500000008', 'PRS85006112', 'CUUR0000AA0', 'CWUR0000SA0', 'CUUR0000SA0L1E',
                                    'WPSFD4', 'WPUFD4', 'WPUFD49104', 'WPUFD49116', 'WPUFD49207', 'EIUIR', ' EIUIQ', 'CIU1010000000000A',
                                    ' CIU2010000000000A', 'CIU2020000000000A'
                                    ], "startyear": "1980", "endyear": "2023"})
    p = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)
    json_data = json.loads(p.text)
    # Prepare the data for the OpenAI GPT-3 model
    documents = []
    for series in json_data['Results']['series']:
        seriesId = series['seriesID']
        for item in series['data']:
            year = item['year']
            period = item['period']
            value = item['value']
            footnotes = ""
            for footnote in item['footnotes']:
                if footnote:
                    footnotes = footnotes + footnote['text'] + ','
            if 'M01' <= period <= 'M12':
                document = f"{seriesId} {year} {period} {value} {footnotes}"
                documents.append(document)
    # Join the documents with new lines
    documents_text = "\n".join(documents)
    # Use the OpenAI GPT-3 model to answer the query
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=input + "\n" + documents_text,
        max_tokens=50,
        temperature=0.7,
        n=1,
        stop=None
    )
    return response['choices'][0]['text']