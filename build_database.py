# AUTONOMOUS RESEARCH AGENT
#
# PROJECT PIPELINE
#
# Day 1:
# PDF -> Text
#
# Day 2:
# PDF -> Text -> Chunks
#
# Future:
# PDF -> Text -> Chunks -> Embeddings
# -> Vector Database -> Semantic Search
# -> LLM -> Final Answer

import os

from pdf_reader import extract_text
from chunker import create_chunks

PAPERS_FOLDER = "papers"
CHUNKS_FOLDER = "data/chunks"

os.makedirs(CHUNKS_FOLDER, exist_ok=True)

for file in os.listdir(PAPERS_FOLDER):

    if file.endswith(".pdf"):

        pdf_path = os.path.join(
            PAPERS_FOLDER,
            file
        )

        print(f"\nProcessing: {file}")

        text = extract_text(pdf_path)

        chunks = create_chunks(text)

        print(
            f"Created {len(chunks)} chunks"
        )

        output_file = os.path.join(
            CHUNKS_FOLDER,
            file.replace(".pdf", ".txt")
        )

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as f:

            for i, chunk in enumerate(chunks):

                f.write(
                    f"\n\n===== CHUNK {i+1} =====\n\n"
                )

                f.write(chunk)

        print(
            f"Saved: {output_file}"
        )