import langchain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ChatMessageHistory, ConversationBufferMemory
from langchain.document_loaders import DirectoryLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.agents import initialize_agent, AgentType
from langchain.agents.agent_toolkits import VectorStoreInfo, VectorStoreToolkit

class ChatBot:

    def __init__(self):

        langchain.verbose = True

        self.llm = ChatOpenAI(
                        model='gpt-3.5-turbo', 
                        temperature=0
                    )

        self.tools = []

    def add_vectorstore_tools(self, dir, glob):

        loader = DirectoryLoader(dir, glob=glob)
        index = VectorstoreIndexCreator().from_loaders([loader])

        info = VectorStoreInfo(
            name="langchain-apps",
            description="langchain-apps のソースコード",
            vectorstore=index.vectorstore,
        )
        toolkit = VectorStoreToolkit(
            vectorstore_info=info
        )
        self.tools.extend(toolkit.get_tools())

    def chat(self, message, history):

        chat_memory = ConversationBufferMemory(
            chat_memory=history,
            memory_key="chat_history",
            return_messages=True
        )

        agent = initialize_agent(
            self.tools,
            self.llm,
            agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
            memory=chat_memory,
            handle_parsing_errors=True,
        )

        return agent.run(input=message)