from langchain_openai import  ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import WebBaseLoader
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda, RunnableParallel, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()


web_urls = ["https://www.flipkart.com/apple-iphone-16-ultramarine-128-gb/p/itmcc210cae43fba?pid=MOBH4DQFYZT6EH2F&lid=LSTMOBH4DQFYZT6EH2FP6PUJU&marketplace=FLIPKART&cmpid=content_mobile_22428124232_x_8965229628_gmc_pla&tgi=sem,1,G,11214002,x,,,,,,,c,,,,,,,&entryMethod=22428124232&cmpid=content_22428124232_gmc_pla&gad_source=1&gad_campaignid=22428139664&gbraid=0AAAAADxRY5_JFWlJobrL0E2cRisVZSZZm&gclid=CjwKCAjwgb_CBhBMEiwA0p3oOJcN3d9nHU0pc4vrYU2145Pn5dP1jok-V6CVJkxzpG7lzFnRfKoqSRoCYQ8QAvD_BwE", "https://www.reliancedigital.in/product/apple-iphone-16-256-gb-ultramarine-m0xrrm-8590266?gad_source=1&gad_campaignid=22588256564&gbraid=0AAAAADthdYkctIarnomuRcCK3jhP5Lj6W&gclid=CjwKCAjwgb_CBhBMEiwA0p3oOCHxV6xPLzfWDVLOAEND8JP1G21p5VZALi1Iw_lyUj0ZADFETopgJBoCV0cQAvD_BwE"]


loader = WebBaseLoader(web_path=web_urls)
docs = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=50)
chunks = splitter.split_documents(docs)
# print (len(chunks))
# print (chunks[45])

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vector_store = FAISS.from_documents(chunks,embeddings)

# print (vector_store.index_to_docstore_id)

retriever = vector_store.as_retriever(search_type = "similarity",search_kwargs={"k": 4})

# print (retriever)

# result = retriever.invoke('What are the phones we are talking about?')
# # print (result)
llm = ChatOpenAI(model="gpt-4o", temperature=0.3)

prompt = PromptTemplate(template= '''You are a smart assistant, answer the questions given to you buy the user
                        if you do not have the information say no I cannot answer. Answer ONLY from the provided  context
                        Question :{question}
                        {context}
                        ''', input_variables=["context", "question"])

question = "what is the price of iphone 16?"
retrieved_docs = retriever.invoke(question)

context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)
final_prompt = prompt.invoke({"context": context_text, "question": question})

# answer = llm.invoke(final_prompt)
# print(answer.content)

def format_docs(retrieved_docs):
  context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)
  return context_text

parallel_chain = RunnableParallel({"context" : retriever | RunnableLambda(format_docs), "question": RunnablePassthrough()})

# print (parallel_chain.invoke('what is the model number?'))

parser = StrOutputParser()

main_chain = parallel_chain | prompt | llm | parser

print (main_chain.invoke('can you tell me about iphone 16 in bullet points?'))