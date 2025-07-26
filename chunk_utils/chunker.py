from langchain.text_splitter import RecursiveCharacterTextSplitter

# def chunk_text(text: str, chunk_size: int =800, chunk_overlap: int = 200) -> list[str]:
#     splitter = RecursiveCharacterTextSplitter(
#         chunk_size=chunk_size,
#         chunk_overlap=chunk_overlap,
#         separators=["\n\n", "\n", ".", "।", " "],
#     )
#     chunks = splitter.split_text(text)
#     return chunks




def chunk_text(text: str, chunk_size: int = 5000, chunk_overlap: int = 1100) -> list[str]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", "।", " "],
        keep_separator=False,
        strip_whitespace=True,
    )
    chunks = splitter.split_text(text)
    chunks = [chunk for chunk in chunks if chunk.strip()]
    return chunks
