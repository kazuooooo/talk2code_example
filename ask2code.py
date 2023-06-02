from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import DeepLake
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from getpass import getpass
from dotenv import load_dotenv

load_dotenv()

embeddings = OpenAIEmbeddings()
# DeepLakeからデータを読み込み
vector_store = DeepLake(
    dataset_path=f"hub://kazuwombat/langchain-code",
    read_only=True,
    embedding_function=embeddings,
)
# Retrieverを定義
retriever = vector_store.as_retriever()
retriever.search_kwargs["distance_metric"] = "cos"
retriever.search_kwargs["fetch_k"] = 20
retriever.search_kwargs["maximal_marginal_relevance"] = True
retriever.search_kwargs["k"] = 20

# Chainを定義
model = ChatOpenAI(model_name="gpt-3.5-turbo")  # 'ada' 'gpt-3.5-turbo' 'gpt-4',
qa = ConversationalRetrievalChain.from_llm(model, retriever=retriever)


chat_history = []
chat_history.append(("What's StuffDocumentsChain?", "`StuffDocumentsChain` is a chain that combines multiple documents by stuffing them into context. It is a part of the BaseCombineDocumentsChain and is used to process and join documents in a specific format. The chain takes an LLMChain, document prompt, and other configurations as input, and is used to combine documents in a particular sequence or format, depending on the given prompts and configurations."))

def ask_question(question: str, chat_history: list) -> str:
    "Ask a question and return an answer."
    result = qa({"question": question, "chat_history": chat_history})
    return result["answer"]


question = getpass("What's your question?:")
print("Q:", question)
answer = ask_question(question, chat_history=chat_history)
print("A:", answer)
