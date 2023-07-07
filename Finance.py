from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.llms import OpenAI
import os
import streamlit as st
import openai
from dotenv import load_dotenv, find_dotenv
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.tools import BaseTool
from langchain.llms import OpenAI
from langchain import LLMMathChain, SerpAPIWrapper, GoogleSearchAPIWrapper
from langchain.agents import load_tools, initialize_agent, AgentType
from langchain.llms import OpenAI as LangchainOpenAI
from langchain import SerpAPIWrapper
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from langchain.utilities.wolfram_alpha import WolframAlphaAPIWrapper
from langchain.utilities import GoogleSerperAPIWrapper
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import RetrievalQA
import openai
from dotenv import load_dotenv, find_dotenv
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import Chroma
# Load environment variables
_ = load_dotenv(find_dotenv())
openai.api_key = os.environ['OPENAI_API_KEY']

# Displaying the initial UI/UX
st.title("Symply Finance")
st.write("We are your AI-powered Financial Wizard")
st.subheader("Here's some additional information:")
st.write("This app provides general information about investing in financial markets.")
st.write("It's important to do your own research and consider professional advice before making any investment decisions.")

# Collecting prompt from our users
prompt = st.text_input('What would you like to know or explained')

# Initialize the Langchain LLM and the Temperature (How creative the AI will be)
llm = LangchainOpenAI(temperature=0.1)

# Initializing the Google Serper API Wrapper tool
# search = GoogleSerperAPIWrapper(api_key=os.getenv('SERPER_API_KEY'))

os.environ["GOOGLE_CSE_ID"] = "55c1332fff9a840f0"
os.environ["GOOGLE_API_KEY"] = "AIzaSyCU6_DO5JWubdbBolU-ciATkPOclNCHTEI"

search = GoogleSearchAPIWrapper()

# Creating a document loader
loader = PyPDFLoader('Goldman-Sachs-annual-report-2022.pdf')
pages = loader.load_and_split()
embeddings = OpenAIEmbeddings()
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

# Initialize the tools and agent
# tools = load_tools(["google-serper"], llm=llm)
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

# Set up ChatOpenAI model
chat = ChatOpenAI(temperature=0)

# Defining investment-related system messages
investment_system_messages = [
    SystemMessage(content="You are a friendly Financial analyst that  provides a detailed investment advice."),
    SystemMessage(content="Investing involves risks. It's important to do thorough research and consider professional advice."),
    SystemMessage(content="I can provide general and detailed information about investment strategies and concepts."),
    SystemMessage(content="You Provide highly profitable Investment Strategies")
]

# Processing user input and display results
if st.button("Submit"):
    if prompt:
        user_input = prompt
        conversation = [
            *investment_system_messages,
            HumanMessage(content=user_input)
        ]
        result = agent(conversation)
        response_text = result['output']
        st.write(response_text)
    else:
        st.write("Please enter a question.")


