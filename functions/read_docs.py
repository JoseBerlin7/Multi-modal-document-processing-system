'''Purpose: To read and preprocess the PDF documents'''

import pymupdf

class document_handling:
    def __init__(self, book_path=rf"data\1 - The Power of Positive Thinking ( PDFDrive ).pdf"):
        self.book_path = book_path
    
    def get_books_info(self):
        try:
            pg_start = int(input("Enter the chapter 1 page number\t:\t"))+1 # To process data from here
            pg_end = int(input("Enter the end page of the last chapter\t:\t"))+1 
            # We added one cuz our count starts from 0

        except Exception as e:
            print(f"input Error : {e}")
            return 0,-1

        return pg_start, pg_end
    
    def get_pdf_contents(self):
        start, end = self.get_books_info()
        with pymupdf.open(self.book_path) as book:
            content = " ".join([page.get_text() for page in book[start:min(end, len(book))]])
        return content