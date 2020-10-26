from reportlab.lib.pagesizes import A4, inch
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reportlab.platypus import Frame, Paragraph
from reportlab.lib.styles import ParagraphStyle

from config import Config

from app.db.database import GetWypozyczenieByID

import os
import json

strings = {}

def get_pdf_data(id):
    return GetWypozyczenieByID(id)

def generate_settings():
    settings = {"header1": "",
                "header2": "",
                "header3": "",
                "owner1": "",
                "owner2": "",
                "owner3": ""
                }
    with open('app/static/pdfSettings.json', 'w') as file:
        json.dump(settings, file)

def load_settings():
    global strings
    try:
        with open('app/static/pdfSettings.json') as file:
            strings = json.load(file)
    except FileNotFoundError:
        print('doing')
        generate_settings()
        with open('app/static/pdfSettings.json') as file:
            strings = json.load(file)

def create_logo_section(pdf):
    logo = ImageReader(Config.logo)
    pdf.drawImage(logo, 50, 790 - 73.2, mask='auto', width=126.4, height=73.2)

    pdf.setFont('AbhayaLibre', 10)

    pdf.drawString(53,790-73.2-15, strings['header1'])
    pdf.drawString(44,790-73.2-25, strings['header2'])
    pdf.drawString(52,790-73.2-35, strings['header3'])

def create_header_section(pdf, data_od, client_name, client_id):

    header_string = "UMOWA WYPOŻYCZENIA SPRZĘTU"
    data_string = "Zawarta w dniu"

    data = data_od
    client_name = client_name
    client_addres = "............................................"
    client_id_card = client_id

    pdf.setLineWidth(.3)

    set1 = 595 / 2 - (stringWidth(header_string, 'AbhayaLibreB', 13) / 2)
    set2 = 595 - 50 - stringWidth(data_string, 'AbhayaLibre', 10)
    data_set1 = 595 - 50 - stringWidth(data, 'AbhayaLibre', 10)

    pdf.setFont('AbhayaLibreB', 13)
    pdf.drawString(set1, 790, header_string)
    pdf.setFont('AbhayaLibre', 10)
    pdf.drawString(set2, 790, data_string)
    pdf.drawString(data_set1, 775, data)

    pdf.drawString(200, 750, "Zawarta w dniu %s pomiędzy: %s, zamieszkałym " % (data, client_name))
    pdf.drawString(200, 735, "%s , legitymująca/y się dowodem osobistym" % client_addres)
    pdf.drawString(200, 720, "(seria, numer) %s" % client_id_card)
    pdf.drawString(200, 705, "a")
    pdf.drawString(200, 690, strings['owner1'])
    pdf.drawString(200, 675, strings['owner2'])
    pdf.drawString(200, 660, strings['owner3'])
    pdf.drawString(200, 645, "Zwanym dalej 'Wypożyczającym'")

def create_items_talbe(pdf, items):

    pdf.setFont('AbhayaLibreB', 10)
    string = "&1"
    string_width = 595 / 2 - (stringWidth(string, 'AbhayaLibreB', 10) / 2)
    pdf.drawString(string_width, 610, string)

    pdf.setFont('AbhayaLibre', 10)
    pdf.drawString(50, 595, "Przedmiotem niniejszej umowy jest wypożyczenie sprzętu:")

    table_data = [["Przedmiot", "Wartość", "Cena"]]

    for x in items:
        table_data.append(x)

    inch_s = 0.0104166666666665
    multiple = 0.23
    offset = (multiple * len(table_data))/inch_s

    if 0 < len(table_data) < 5:
        offset -= len(table_data) * 4
    if 5 < len(table_data) < 10:
        offset -= len(table_data) * 4.3
    if 10 < len(table_data):
        offset -= len(table_data) * 4.8

    t = Table(table_data, colWidths=[4.25 * inch, 1.25 * inch ,1.25 * inch], rowHeights=0.23 * inch)
    t.setStyle(TableStyle(
                        [('FONT',(0,0),(-1,-1), 'AbhayaLibre', 10),
                        ('GRID', (0, 0), (1, -3), 1, colors.black),
                        ('INNERGRID', (0, 0), (-1, -1), 1, colors.black),
                        ('BOX', (0, 0), (-1, -1), 1, colors.black),
                        ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
                        ('BACKGROUND', (0, 0), (-1, 0), colors.transparent),
                        ]
                    ))

    t.wrapOn(pdf, 800, 600)
    t.drawOn(pdf, 50, 595 - offset)


def create_central_section(pdf, date_start, date_end, date_hours_start, date_hours_end, price):
    pdf.setFont('AbhayaLibreB', 10)
    string = "&2"
    string_width = 595 / 2 - (stringWidth(string, 'AbhayaLibreB', 10) / 2)

    pdf.drawString(string_width, 575 - 276 , string)

    pdf.setFont('AbhayaLibre', 10)
    pdf.drawString(50, 560 - 276, "Wypożyczający oświadcza że jest właścicielem sprzętu będącego przedmiotem wporzyczenia")

    pdf.setFont('AbhayaLibreB', 10)
    string = "&3"
    string_width = 595 / 2 - (stringWidth(string, 'AbhayaLibreB', 10) / 2)

    pdf.drawString(string_width, 540 - 276 , string)

    data_od = date_start + ' ' + date_hours_start
    data_do = date_end + ' ' + date_hours_end

    pdf.setFont('AbhayaLibre', 10)
    pdf.drawString(50, 525 - 276, "1.) Umowa wypożyczenia zostaje zawarta na okres: od %s do %s" % (data_od , data_do))
    pdf.drawString(50, 510 - 276, "2.) Sprzęt zostaje wydany Korzystającemu w dniu podpisania umowy")
    pdf.drawString(50, 495 - 276, "3.) Sprzęt zostaje zwrócony do Wypożyczalni zgodnie z datą okresu wporzyczenia")

    pdf.setFont('AbhayaLibreB', 10)
    string = "&4"
    string_width = 595 / 2 - (stringWidth(string, 'AbhayaLibreB', 10) / 2)

    pdf.drawString(string_width, 475 - 276 , string)

    cena = "500zł"

    pdf.setFont('AbhayaLibre', 10)
    pdf.drawString(50, 460 - 276, "1.) Opłata za sprzęt w wyznaczonym okresie wynosi: %s" % price)
    pdf.drawString(50, 445 - 276, "2.) W przypadku niedotrzymania terminu oddania sprzętu, korzystający zostanie obciążony dodatkową kwotą")
    pdf.drawString(50, 430 - 276, "    za przedłużenie wypożyczenia stosownie do ceny wypożyczenia sprzętu")

    pdf.setFont('AbhayaLibreB', 10)
    string = "&5"
    string_width = 595 / 2 - (stringWidth(string, 'AbhayaLibreB', 10) / 2)

    pdf.drawString(string_width, 410 - 276 , string)

    pdf.setFont('AbhayaLibre', 10)
    pdf.drawString(50, 395 - 276, "Po kakończeniu umowy korzystający zobowiązany jest zwrócić Wynajmującemu sprzęt w ")
    pdf.drawString(50, 380 - 276, "stanie niepogorszonym z uwzglednieniem normalnego stopnia zużycia ")


def create_footer(pdf):

    styleText = ParagraphStyle(
        name='Normal',
        fontName='AbhayaLibreSb',
        fontSize=8,
    )


    pdf.rect(50, 10, 200, 70, fill=0)
    pdf.rect(345, 10, 200, 70, fill=0)
    storyExample2 = []
    frameExample2 = Frame(51, 9, 275, 70, showBoundary=0)
    storyExample2.append(Paragraph("Przedstawiciel wypożyczalni", styleText))
    frameExample2.addFromList(storyExample2, pdf)

    storyExample1 = []
    frameExample1 = Frame(345, 9, 275, 70, showBoundary=0)
    storyExample1.append(Paragraph("Klient", styleText))
    frameExample1.addFromList(storyExample1, pdf)



def create_pdf(wypozyczenie_id):
    load_settings()

    data = get_pdf_data(wypozyczenie_id)

    date_start = data['info']['wypozyczenie_od']
    date_end = data['info']['wypozyczenie_do']
    date_hours_start = data['info']['wypozyczenie_godz_od']
    date_hours_end = data['info']['wypozyczenie_godz_do']
    client_name = data['info']['klient_name']
    client_id = data['info']['klient_dowod']
    price = data['info']['price']

    items = [[x['nazwa'], x['wartosc'], x['cena']] for x in data['pozycje']]


    pdfmetrics.registerFont(TTFont('AbhayaLibre', 'app/pdf/font/AbhayaLibre.ttf'))
    pdfmetrics.registerFont(TTFont('AbhayaLibreB', 'app/pdf/font/AbhayaLibre-Bold.ttf'))
    pdfmetrics.registerFont(TTFont('AbhayaLibreSb', 'app/pdf/font/AbhayaLibre-SemiBold.ttf'))

    # Pdf path
    path_ = os.path.abspath('app/static/pdf/%s.pdf' % wypozyczenie_id)

    canvas_pdf = canvas.Canvas(path_, pagesize=A4)

    create_logo_section(canvas_pdf)

    # Header
    create_header_section(canvas_pdf, date_start, client_name, client_id)

    # Items Table
    create_items_talbe(canvas_pdf, items)

    # Central
    create_central_section(canvas_pdf, date_start, date_end, date_hours_start, date_hours_end, price)

    # Footer
    create_footer(canvas_pdf)

    canvas_pdf.save()
