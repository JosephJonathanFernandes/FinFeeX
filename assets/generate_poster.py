from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from PIL import Image, ImageDraw, ImageFont
import os

OUT_DIR = os.path.dirname(__file__)
PDF_PATH = os.path.join(OUT_DIR, 'FinFeeX_poster.pdf')
PNG_PATH = os.path.join(OUT_DIR, 'FinFeeX_poster.png')


def generate_pdf(path=PDF_PATH):
    c = canvas.Canvas(path, pagesize=A4)
    width, height = A4

    # Header
    c.setFillColor(colors.HexColor('#00796B'))
    c.rect(0, height - 60, width, 60, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont('Helvetica-Bold', 18)
    c.drawString(20 * mm, height - 44, 'FinFeeX — Hidden-Fees X-Ray')
    c.setFont('Helvetica', 10)
    c.drawString(20 * mm, height - 56, 'Unmasking the hidden costs behind every financial statement')

    # Problem / Solution
    c.setFillColor(colors.black)
    c.setFont('Helvetica-Bold', 12)
    c.drawString(20 * mm, height - 90, 'Problem')
    c.setFont('Helvetica', 10)
    text = c.beginText(20 * mm, height - 105)
    text.textLines('''Financial statements hide small recurring fees like convenience charges and FX markups. Users rarely notice them, but they add up.''')
    c.drawText(text)

    c.setFont('Helvetica-Bold', 12)
    c.drawString(20 * mm, height - 150, 'Solution')
    c.setFont('Helvetica', 10)
    text = c.beginText(20 * mm, height - 165)
    text.textLines('''FinFeeX extracts fee lines from PDFs, classifies charges, estimates annual cost, and drafts complaint emails.''')
    c.drawText(text)

    # Mock Fee Nutrition Label box
    c.setStrokeColor(colors.HexColor('#00796B'))
    c.rect(width - 100 * mm, height - 160, 80 * mm, 80 * mm, stroke=1, fill=0)
    c.setFont('Helvetica-Bold', 11)
    c.drawString(width - 96 * mm, height - 170, 'Fee Nutrition Label')
    c.setFont('Helvetica', 10)
    c.drawString(width - 96 * mm, height - 190, 'Transparency Score: 68%')
    c.drawString(width - 96 * mm, height - 205, 'Estimated Annual Hidden Cost: ₹1,088')
    c.drawString(width - 96 * mm, height - 220, 'Top fee: Convenience Fee (₹49/month)')

    # Footer
    c.setFont('Helvetica', 9)
    c.setFillColor(colors.grey)
    c.drawString(20 * mm, 20 * mm, 'FinFeeX — Hidden-Fees X-Ray | Demo prototype')

    c.showPage()
    c.save()


def generate_png(path=PNG_PATH):
    # Simple PNG version using PIL
    W, H = (1240, 1754)  # roughly A4 at 150dpi
    bg = (255, 255, 255)
    im = Image.new('RGB', (W, H), bg)
    draw = ImageDraw.Draw(im)

    # Header
    header_h = 120
    draw.rectangle([(0, 0), (W, header_h)], fill=(0, 121, 107))
    try:
        font_b = ImageFont.truetype('arialbd.ttf', 48)
        font = ImageFont.truetype('arial.ttf', 18)
    except Exception:
        font_b = ImageFont.load_default()
        font = ImageFont.load_default()

    draw.text((40, 28), 'FinFeeX — Hidden-Fees X-Ray', fill='white', font=font_b)
    draw.text((40, 78), 'Unmasking the hidden costs behind every financial statement', fill='white', font=font)

    # Problem & solution
    draw.text((40, 160), 'Problem', fill='black', font=font_b)
    draw.text((40, 200), 'Financial statements hide small recurring fees like convenience charges and FX markups. Users rarely notice them, but they add up.', fill='black', font=font)

    draw.text((40, 300), 'Solution', fill='black', font=font_b)
    draw.text((40, 340), 'FinFeeX extracts fee lines from PDFs, classifies charges, estimates annual cost, and drafts complaint emails.', fill='black', font=font)

    # Fee label box
    box_x = W - 520
    box_y = 220
    box_w = 460
    box_h = 260
    draw.rectangle([box_x, box_y, box_x + box_w, box_y + box_h], outline=(0, 121, 107), width=4)
    draw.text((box_x + 20, box_y + 20), 'Fee Nutrition Label', fill='black', font=font_b)
    draw.text((box_x + 20, box_y + 80), 'Transparency Score: 68%\nEstimated Annual Hidden Cost: ₹1,088\nTop fee: Convenience Fee (₹49/month)', fill='black', font=font)

    # Footer
    draw.text((40, H - 80), 'FinFeeX — Hidden-Fees X-Ray | Demo prototype', fill=(120, 120, 120), font=font)

    im.save(path, format='PNG')


if __name__ == '__main__':
    os.makedirs(OUT_DIR, exist_ok=True)
    generate_pdf()
    generate_png()
    print('Generated poster:', PDF_PATH, PNG_PATH)
