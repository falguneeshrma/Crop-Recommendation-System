import os
import json

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

HERE = os.path.dirname(os.path.abspath(__file__))
INDEX_DIR = os.path.join(HERE, "vectorstore", "faiss_index")
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL = "openai/gpt-oss-120b"
SYSTEM_PROMPT = """You are an agricultural assistant helping farmers understand crop \
recommendations. Answer ONLY using the context provided below, which comes from an \
agronomic knowledge base. If the answer isn't in the context, say you don't have \
that information rather than guessing.

Keep answers practical and easy to understand for a farmer — avoid unnecessary \
jargon, and use bullet points for multi-step advice (e.g. fertilizer schedules).

Context:
{context}
"""


class CropRAGAssistant:
    """Wraps the FAISS retriever + Groq LLM into one ask()/explain_recommendation() interface."""

    def __init__(self, groq_api_key: str | None = None, k: int = 4):
        api_key = groq_api_key or os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise ValueError(
                "No Groq API key found. Set GROQ_API_KEY in your .env "
                "(free key at https://console.groq.com/keys)."
            )

        embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
        if not os.path.exists(INDEX_DIR):
            raise FileNotFoundError(f"No FAISS index at {INDEX_DIR}, run ingest.py first.")

        vectorstore = FAISS.load_local(INDEX_DIR, embeddings, allow_dangerous_deserialization=True)
        self.retriever = vectorstore.as_retriever(search_kwargs={"k": k})

        llm = ChatGroq(model=LLM_MODEL, api_key=api_key, temperature=0.2)
        self.llm = llm
        prompt = ChatPromptTemplate.from_messages([("system", SYSTEM_PROMPT), ("human", "{question}")])

        def format_docs(docs):
            return "\n\n---\n\n".join(
                f"[{d.metadata.get('crop', 'unknown').capitalize()}] {d.page_content}" for d in docs
            )

        self.chain = (
            {"context": self.retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )

    def ask(self, question: str, crop: str | None = None) -> dict:
        # nudging the query with the crop name keeps retrieval on-topic for
        # follow-up questions right after a prediction ("how much water does it need?")
        query = f"Regarding {crop}: {question}" if crop else question
        docs = self.retriever.invoke(query)
        answer = self.chain.invoke(query)
        sources = sorted({d.metadata.get("crop", "unknown") for d in docs})
        return {"answer": answer, "sources": sources}

    def explain_recommendation(self, crop: str, inputs: dict) -> str:
        stats_path = os.path.join(HERE, "data", "crop_stats.json")
        try:
            with open(stats_path, "r") as f:
                stats = json.load(f)
        except Exception:
            stats = {}

        crop_stats = stats.get(crop.lower(), {})
        
        comparisons = []
        labels = {
            'N': 'Nitrogen', 'P': 'Phosphorus', 'K': 'Potassium',
            'temperature': 'Temperature', 'humidity': 'Humidity', 
            'ph': 'Soil pH', 'rainfall': 'Rainfall'
        }
        units = {
            'N': ' kg/ha', 'P': ' kg/ha', 'K': ' kg/ha',
            'temperature': ' °C', 'humidity': '%',
            'ph': '', 'rainfall': ' mm'
        }
        
        for key in ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']:
            val = inputs.get(key, 0)
            if key in crop_stats:
                min_val, max_val, _ = crop_stats[key]
                if val < min_val:
                    comp = f"below the suitable range ({min_val:.1f}-{max_val:.1f})"
                elif val > max_val:
                    comp = f"above the suitable range ({min_val:.1f}-{max_val:.1f})"
                else:
                    comp = f"within the suitable range ({min_val:.1f}-{max_val:.1f})"
            else:
                comp = "no reference data available"
                
            unit_str = units[key]
            comparisons.append(f"• {labels[key]}: {val}{unit_str} — {comp}")
            
        comparisons_str = "\n".join(comparisons)
        
        question = (
            f"A machine learning model recommended '{crop}' for a farmer's field. "
            f"Here are the exact conditions compared to the crop's reference ranges:\n"
            f"{comparisons_str}\n\n"
            f"Format your response EXACTLY like this (do NOT output anything else):\n"
            f"Why this crop?\n\n"
            f"Predicted crop: {crop.capitalize()}\n\n"
            f"Your conditions compared with {crop.capitalize()}'s requirements:\n"
            f"{comparisons_str}\n\n"
            f"Overall: <write a 2-3 sentence explanation of why the combination of conditions supports the predicted crop. If any conditions are outside the suitable range, explicitly mention them here.>"
        )
        
        system_msg = (
            "You are a helpful agricultural assistant. Your job is to strictly format the data provided by the user into the requested output structure. "
            "Write the 'Overall:' summary based ONLY on the comparisons provided in the prompt. Do not invent any ranges."
        )
        
        from langchain_core.messages import SystemMessage, HumanMessage
        messages = [SystemMessage(content=system_msg), HumanMessage(content=question)]
        
        return self.llm.invoke(messages).content


if __name__ == "__main__":
    # quick manual check: python rag_chain.py
    bot = CropRAGAssistant()
    print(bot.explain_recommendation(
        "rice", {"N": 90, "P": 42, "K": 43, "temperature": 24.5, "humidity": 82.0, "ph": 6.5, "rainfall": 220.0}
    ))
