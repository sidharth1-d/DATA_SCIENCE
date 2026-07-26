import os
import chromadb
from llama_index.core import VectorStoreIndex , SimpleDirectoryReader,StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from llama_index.core import Settings

API_KEY = 'AIzaSyB8ZLy7eeC4-jkIgCKRwOJagG5E2xF38Bo'

Settings.llm = GoogleGenAI(model = 'gemini-2.5-flash',api_key = API_KEY)

Settings.embed_model = GoogleGenAIEmbedding(model = 'models/text-embedding-004',api_key = API_KEY)

os.makedirs("my_data",exist_ok=True)

sample_text = """
Core2web Technologies is a premier coding academy and IT training institute founded in January 2017 by Shashi Bagal Sir.

Headquartered in Pune, Maharashtra, the institute focuses on technical logic building, coding fundamentals, and industry-oriented software engineering.

Core Offerings & Curriculum

Programming Languages:
Comprehensive training in foundational languages including:
- C
- C++
- Java
- Python
- Data Structures & Algorithms (DSA)

Frameworks & Modern Tech:
Courses in:
- Flutter (cross-platform mobile apps)
- React (front-end development)
- Spring Boot (enterprise backend)
- Database Management Systems (DBMS)
- Operating Systems (OS)

Super-X Platform:
An intensive project implementation program and competition where students build real-world software products from scratch.
Placement Assistance:
Career support featuring:
- 200+ practical live questions
- 1,000+ mock quiz questions
- Mock interviews
- Dedicated aptitude preparation

Learning Ecosystem:
Core2web Mobile App available on the Google Play Store providing:
- Recorded video lectures
- Graphical progress tracking
- Community discussion forums
- Group assignments

Practical Labs:
A physical dedicated lab space designed to foster:
- Standard programming practices
- Team-based application testing

Student Success:
The institute has trained over 15,000 students resulting in placements across software firms like:
- PTC Software
- TCS
- Cognizant

Headquarter Address:
3rd Floor, Walhekar Properties,
Near Navale Bridge,
Narhe Gaon,
Pune, Maharashtra 411041,
India.
Operating Hours:
Open daily until 8:00 PM.
"""

with open("my_data/academy_info.txt", "w", encoding="utf-8") as f:
    f.write(sample_text.strip())

print("[System] Local .txt  knowledge file successfully created in './my_data' folder.")


db_client = chromadb.PersistentClient(path="./chroma_db_storage")

chroma_collection = db_client.get_or_create_collection("academy_knowledge_base")

vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

storage_context = StorageContext.from_defaults(vector_store=vector_store)

documents = SimpleDirectoryReader("./my_data").load_data()


index = VectorStoreIndex.from_documents(documents,storage_context=storage_context)

print("[System] Text embedded and permanently saved in disk in './chroma_db_storage'.")

query_engine = index.as_query_engine()

test_query = (
    "Who is the founder of the academy "
    "and where is the campus located?"
)

print(f"\n[User Question]: {test_query}")
response = query_engine.query(test_query)
print("\n[AI Generated Answer]:")
print(response)