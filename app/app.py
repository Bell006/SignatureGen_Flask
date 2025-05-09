import os
import tempfile
from flask import request, jsonify, Flask
from flask_cors import CORS
from PIL import Image, ImageDraw, ImageFont
from googleapiclient.http import MediaFileUpload

from app.utils import format_phone_number, get_state_abbreviation, validate_name
from app.google_api import GoogleAPI
from app.app_error import AppError

##Setting application
app = Flask(__name__)
CORS(app)

google_api = GoogleAPI()
    
@app.errorhandler(AppError)

@app.route('/create_signature', methods=['POST'])

def create_email_signature():
    try:

        data = request.get_json()

        email = data.get('email', '')
        name = data.get('name', '').upper()
        phone = data.get('phone', '')
        department = data.get('department', '').upper()
        city = data.get('city', '').upper()
        state = data.get('state', '').upper()
        regional = data.get('regional', '').upper()

        if not name or not department or not phone:
           raise AppError('Preencha todos os campos.', 400)
        
        # Format the phone number
        formatted_phone = format_phone_number(phone)

        # Validates name
        validate_name(name)
        
        if regional:
            state_text = f'REGIONAL {regional}'
        else:
            # Get state abbreviation
            state_abbreviation = get_state_abbreviation(state)
            state_text = state_abbreviation
        
        # Use url_for to get the correct path to the image
        template_image_path = os.path.join(app.root_path, 'static', 'assets', 'signature_template.jpg')
        if not os.path.exists(template_image_path):
            return jsonify({'message': 'Template image not found'}), 404

        image = Image.open(template_image_path)
        
        # Define the font and size using os.path.join
        font_path_black = os.path.join(app.root_path, 'static', 'fonts', 'Lato-Black.ttf')
        font_path_regular = os.path.join(app.root_path, 'static', 'fonts', 'Lato-Regular.ttf')
        font_path_bold = os.path.join(app.root_path, 'static', 'fonts', 'Lato-Bold.ttf')
        
        if not os.path.exists(font_path_black) or not os.path.exists(font_path_regular) or not os.path.exists(font_path_bold):
            return jsonify({'message': 'Font file not found'}), 404
        
        font_title_size = 23
        fontTitle = ImageFont.truetype(font_path_black, font_title_size)
        fontSubTitle = ImageFont.truetype(font_path_regular, 12)
        fontSubTitleBold = ImageFont.truetype(font_path_bold, 12)
        
        # Create a drawing context
        draw = ImageDraw.Draw(image)

        # Use url_for to get the correct path to the icon
        template_icon_path = os.path.join(app.root_path, 'static', 'assets', 'icon.png')
        if not os.path.exists(template_icon_path):
            return jsonify({'message': 'Template icon not found'}), 404

        icon = Image.open(template_icon_path)

        # Resize icon
        icon_size = (12, 10) 
        icon_resized = icon.resize(icon_size)

        text_wrapper = f'{department}  | '
        
        # Define positions for the text 
        name_position = (33.77, 22.12)
        phone_position = (56.39, 86)
        text_wrapper_position = (43, 54.5)

        # Draw the text on the image
        while True:
            # Get name's max width
            name_width = draw.textbbox((0, 0), name, font=fontTitle)[2]
            fontTitle = ImageFont.truetype(font_path_black, font_title_size)

            if name_width <= 306 or font_title_size == 21:
                break

            font_title_size -= 0.5

        draw.text(name_position, name, font=fontTitle, fill="#657725")
        draw.text(phone_position, formatted_phone, font=fontSubTitleBold, fill="#38372f")
        draw.text(text_wrapper_position, text_wrapper, font=fontSubTitle, fill="#38372f")

        # Calculate the width of text_wrapper1
        text_bbox = draw.textbbox((0, 0), text_wrapper, font=fontSubTitle)
        text_wrapper_width = text_bbox[2] - text_bbox[0]

        # Calculate the width of the city text
        if regional:
            city_state_text = f'{state_text}'
        else:
            city_state_text = f'{city} - {state_text}'
            
        city_state_width = draw.textbbox((0, 0), city_state_text, font=fontSubTitle)[2]

        # Total width for the rounded rectangle
        total_width = text_wrapper_width + icon_size[0] + city_state_width + 2

        # Draw the icon at the end of text_wrapper
        icon_position = (int(text_wrapper_position[0] + text_wrapper_width + 1), int(text_wrapper_position[1] + 3))
        image.paste(icon_resized, icon_position, icon_resized)

        # Draw the city and state text after the icon
        city_state_position = (icon_position[0] + icon_size[0] + 1, text_wrapper_position[1])
        draw.text(city_state_position, city_state_text, font=fontSubTitle, fill="#38372f")

        # Draw the rounded rectangle around the text, icon, and city
        rect_x0 = 34
        rect_y0 = 52
        rect_x1 = rect_x0 + total_width + 18
        rect_y1 = 71
        draw.rounded_rectangle((rect_x0, rect_y0, rect_x1, rect_y1), outline="#657725", width=2, radius=8)

        google_api.add_to_google_sheet(data)

        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
            output_filename = f'{name.replace(" ", "_")}_assinatura.jpg'
            output_path = temp_file.name

            image.save(output_path, format='JPEG')

            # Google Drive upload
            file_metadata = {
                'name': output_filename,
                'parents': [google_api.credentials_info["google_drive_folder_id"]],
            }

            drive_service = google_api.get_google_drive_service()

            media = MediaFileUpload(output_path, mimetype='image/jpeg', resumable=True)
            uploaded_file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()

            # Get link
            file_id = uploaded_file.get('id')
            file = drive_service.files().get(fileId=file_id, fields='webContentLink').execute()
            file_link = file.get('webContentLink')

        return jsonify({'image_url': file_link}), 200
    except AppError as e:
        return jsonify({'message': e.message}), e.status_code
    except Exception as e:
        print(e)
        return jsonify({'message': 'Erro ao criar a assinatura. Por favor, tente novamente mais tarde.'}), 500


if __name__ == '__main__':
    app.run(debug=True)