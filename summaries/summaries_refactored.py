import whisper
import textwrap

from langchain.chat_models import ChatOpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.schema import Document
from langchain.llms import OpenAI
from langchain import PromptTemplate
from langchain.chains import LLMChain
from langchain.document_loaders import WebBaseLoader

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime


# Transcribe audio
def transcribe_audio(path):
    model = whisper.load_model("base")
    transcription = model.transcribe(audio=path, fp16=False)
    return textwrap.fill(transcription["text"], width=50)


# Summarize text
def summarize_text(text):
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k")
    chain = load_summarize_chain(llm, chain_type="stuff")
    docs = [Document(page_content=text)]
    return chain.run(docs)


def summarize_web_content(url):
    loader = WebBaseLoader(url)
    docs = loader.load()

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k")
    chain = load_summarize_chain(llm, chain_type="stuff")

    return chain.run(docs)


# Export to PDF
def export_to_pdf(summary, title, participants, filename="summary.pdf"):
    wrapped_summary = textwrap.fill(summary, width=75)
    date_of_meeting = datetime.now().strftime("%Y-%m-%d")

    # Clean and wrap the title
    title = title.replace("\n", " ")
    wrapped_title = textwrap.fill(title, width=50)

    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # Title
    c.setFont("Helvetica-Bold", 18)
    y_title = height - 100
    for line in wrapped_title.split("\n"):
        c.drawString(100, y_title, line)
        y_title -= 20  # Adjust the line spacing as needed for the title
    c.setFont("Helvetica", 12)

    # Date
    c.drawString(100, y_title - 30, f"Date: {date_of_meeting}")

    # Participants
    c.drawString(100, y_title - 50, "Participants:")
    for i, participant in enumerate(participants):
        c.drawString(120, y_title - 70 - (i * 14), participant)

    # Summary
    y_summary = y_title - 150  # Adjust this value based on the title and participants
    for line in wrapped_summary.split("\n"):
        c.drawString(100, y_summary, line)
        y_summary -= 14

    c.save()


def create_title(summary):
    llm = OpenAI(temperature=0)
    prompt = PromptTemplate(
        input_variables=["summary"],
        template="Create a title for this summary:{summary}?",
    )

    chain = LLMChain(llm=llm, prompt=prompt)
    title = chain.run(summary)
    title = title.replace("\n", " ").strip()

    return title


# Example usage with MP3 file
path = "./17 VS Code Tips That Will Change Your Data Science Workflow.mp3"
participants = ["Alice", "Bob", "Charlie"]

transcription = transcribe_audio(path)
summary = summarize_text(transcription)
title = create_title(summary)
export_to_pdf(summary, title, participants, filename="summary-audio.pdf")

# Example usage with Web URL
web_url = "https://termene.ro/"
summary = summarize_web_content(web_url)
title = create_title(summary)
export_to_pdf(summary, title, participants=[], filename="summary-web.pdf")
