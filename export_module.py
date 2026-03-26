from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

def export_to_csv(df, path):
    df.to_csv(path, index=False, encoding='utf-8')

def export_to_excel(df, path):
    df.to_excel(path, index=False)

def export_report(report_text, path):
    with open(path, "w", encoding="utf-8") as f:
        f.write(report_text)
        
def export_report_to_pdf(report_text: str, pdf_path: str = "report.pdf"):
    font_path = "DejaVuSerif.ttf"
    if not os.path.exists(font_path):
        print("Предупреждение: DejaVuSerif.ttf не найден. PDF может отображаться некорректно.")

    try:
        pdfmetrics.registerFont(TTFont('DejaVuSerif', font_path))
    except:
        pass  # если шрифт не найден — используем стандартный

    doc = SimpleDocTemplate(pdf_path, pagesize=A4, rightMargin=2 * cm, leftMargin=2 * cm,
                            topMargin=2 * cm, bottomMargin=2 * cm)

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Russian', fontName='DejaVuSerif', fontSize=11, leading=14))
    styles.add(ParagraphStyle(name='Title', fontName='DejaVuSerif', fontSize=16, alignment=1, spaceAfter=20))
    styles.add(ParagraphStyle(name='Heading', fontName='DejaVuSerif', fontSize=13, spaceAfter=12))

    story = []

    # Разбиваем текст отчёта на строки и добавляем как Paragraph
    lines = report_text.split('\n')
    for line in lines:
        if line.strip() == "" or line.startswith("=" * 5):
            story.append(Spacer(1, 0.3 * cm))
            continue
        if line.startswith("АНАЛИТИЧЕСКИЙ ОТЧЁТ") or "ОТЧЁТ" in line:
            story.append(Paragraph(line, styles['Title']))
        elif line.startswith(("1.", "2.", "3.", "4.")) or line.startswith("3."):
            story.append(Paragraph(line, styles['Heading']))
        else:
            story.append(Paragraph(line, styles['Russian']))
        story.append(Spacer(1, 0.2 * cm))

    doc.build(story)
    print(f"PDF отчёт сохранён: {pdf_path}")