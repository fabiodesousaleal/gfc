from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from werkzeug.security import generate_password_hash
from data.conexao import get_conexao

def registra_fontes() -> None:
    pdfmetrics.registerFont(TTFont('Arial-Bold', '/usr/share/fonts/truetype/msttcorefonts/Arial_Bold.ttf'))  
    pdfmetrics.registerFont(TTFont('Arial', '/usr/share/fonts/truetype/msttcorefonts/Arial.ttf'))   
    pdfmetrics.registerFont(TTFont('Times New Roman', '/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman.ttf'))
    pdfmetrics.registerFont(TTFont('Times New Roman-Bold', '/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman_Bold.ttf'))

def criar_login(username, password):            
    con = get_conexao()
    cursor = con.cursor()
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    cursor.execute('INSERT OR REPLACE INTO user (username, password, ativo) VALUES (?, ?, ?)', (username, hashed_password, 1))
    con.commit()
    con.close()