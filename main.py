import docx

def get_information_from_docx(text):
    """
    Extracts information from a docx file.
    
    Args:
        text (str): The text extracted from the docx file.
    
    Returns:
        dict: A dictionary containing the extracted information.
    """
    # Assuming you want to extract some basic information like title, author, etc.
    document = docx.Document()
    for para in document.paragraphs:
        if "Title" in para.text:
            title = para.text.split(":")[1].strip()
        elif "Author" in para.text:
            author = para.text.split(":")[1].strip()

    return {
        'title': title,
        'author': author
    }
