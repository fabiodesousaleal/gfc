from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def registra_fontes() -> None:
    pdfmetrics.registerFont(TTFont('Arial-Bold', '/usr/share/fonts/truetype/msttcorefonts/Arial_Bold.ttf'))  
    pdfmetrics.registerFont(TTFont('Arial', '/usr/share/fonts/truetype/msttcorefonts/Arial.ttf'))   
    pdfmetrics.registerFont(TTFont('Times New Roman', '/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman.ttf'))
    pdfmetrics.registerFont(TTFont('Times New Roman-Bold', '/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman_Bold.ttf'))