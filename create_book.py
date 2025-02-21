import json
import os
import scribus

json_file_path = 'C:/Users/dorra/Desktop/book.json'

if not os.path.exists(json_file_path):
    scribus.messageBox('Error', 'The JSON file was not found.', scribus.ICON_WARNING, scribus.BUTTON_OK)
    exit()

with open(json_file_path, 'r', encoding='utf-8') as file:
    try:
        book_data = json.load(file)
    except json.JSONDecodeError:
        scribus.messageBox('Error', 'The JSON file is malformed.', scribus.ICON_WARNING, scribus.BUTTON_OK)
        exit()

paper_size = scribus.PAPER_A4
margins = (10, 10, 10, 10)
orientation = 0
num_pages = 1
unit = scribus.UNIT_MM
first_page = 1
columns = 1
gutter = 0

scribus.newDocument(paper_size, margins, orientation, num_pages, unit, first_page, columns, gutter)

page_id = 1
text_frame1 = scribus.createText(50, 50, 500, 100, str(page_id))
scribus.setText(book_data["title"], text_frame1)
scribus.setFontSize(36, text_frame1)
scribus.setLineSpacing(45, text_frame1)

text_frame2 = scribus.createText(50, 150, 500, 100, str(page_id))
scribus.setText("by " + book_data["author"], text_frame2)
scribus.setFontSize(24, text_frame2)
scribus.setFont("Times New Roman Italic", text_frame2)
scribus.setLineSpacing(30, text_frame2)

page_id += 1

for chapter in book_data["chapters"]:
    scribus.newPage(-1)
    
    text_frame3 = scribus.createText(50, 50, 500, 100, str(page_id))
    scribus.setText(chapter["title"], text_frame3)
    scribus.setFontSize(24, text_frame3)
    scribus.setLineSpacing(30, text_frame3)
    
    y_offset = 100
    for content in chapter["content"]:
        if content["type"] == "text":
            text_frame4 = scribus.createText(50, y_offset, 500, 100, str(page_id))
            scribus.setText(content["value"], text_frame4)
            scribus.setFontSize(18, text_frame4)
            scribus.setLineSpacing(25, text_frame4)
            y_offset += 120

        elif content["type"] == "image":
            image_path = os.path.join('C:/Users/dorra/Desktop/', content["src"])
            if os.path.exists(image_path):
                image_frame = scribus.createImage(50, y_offset, 200, 200, str(page_id))
                scribus.loadImage(image_path, image_frame)
                y_offset += 220
            else:
                scribus.messageBox('Error', f'The image {content["src"]} is missing.', scribus.ICON_WARNING, scribus.BUTTON_OK)

    page_id += 1
