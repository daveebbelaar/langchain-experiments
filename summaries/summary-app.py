import whisper
import textwrap

from langchain.chat_models import ChatOpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.schema import Document

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime

# --------------------------------------------------------------
# Transcribe audio
# --------------------------------------------------------------

model = whisper.load_model("base")

path = "./17 VS Code Tips That Will Change Your Data Science Workflow.mp3"

transcription = model.transcribe(audio=path, fp16=False)
result = transcription["text"]

wrapped_text = textwrap.fill(result, width=50)
print(wrapped_text)

# --------------------------------------------------------------
# Summarize text
# --------------------------------------------------------------

llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k")
chain = load_summarize_chain(llm, chain_type="stuff")

docs = [Document(page_content=result)]

summary = chain.run([docs])

wrapped_text = textwrap.fill(summary, width=50)
print(wrapped_text)

# Export to PDF
wrapped_summary = textwrap.fill(summary, width=75)

# Metadata
title = "Meeting Summary"
date_of_meeting = datetime.now().strftime("%Y-%m-%d")
participants = ["Alice", "Bob", "Charlie"]

c = canvas.Canvas("summary.pdf", pagesize=letter)
width, height = letter

# Title
c.setFont("Helvetica-Bold", 18)
c.drawString(100, height - 100, title)
c.setFont("Helvetica", 12)

# Date
c.drawString(100, height - 130, f"Date: {date_of_meeting}")

# Participants
c.drawString(100, height - 150, "Participants:")
for i, participant in enumerate(participants):
    c.drawString(120, height - 170 - (i * 14), participant)

# Summary
y = height - 240  # Adjust this value based on the number of participants
for line in wrapped_summary.split("\n"):
    c.drawString(100, y, line)
    y -= 14  # Adjust the line spacing as needed

c.save()
