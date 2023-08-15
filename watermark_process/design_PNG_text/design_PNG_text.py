# from PIL import Image, ImageDraw, ImageFont
# import arabic_reshaper
# from bidi.algorithm import get_display
#
# def opacity_to_alpha(opacity_percent):
#     return round(255 * opacity_percent / 100)
#
# # Open the image
# image_path = 'empty.png'
# image = Image.open(image_path)
#
# # Create a drawing context on the image
# draw = ImageDraw.Draw(image)
#
# # Define the Arabic text
# arabic_text = "فلان الفلاني 2023"
# reshaped_text = arabic_reshaper.reshape(arabic_text)
# bidi_text = get_display(reshaped_text)
#
# # Define the font and initial size
# font_path = 'arial-font.ttf'  # Change this to the path of a font that supports Arabic
# font_size = 40
#
# # Get the width and height of the text to be added
# font = ImageFont.truetype(font_path, font_size)
# text_width = draw.textlength(bidi_text, font=font)
# text_height = font.getmask(bidi_text).getbbox()[3]
#
# # Reduce font size if text is too wide
# while text_width > image.width:
#     font_size -= 1
#     font = ImageFont.truetype(font_path, font_size)
#     text_width = draw.textlength(bidi_text, font=font)
#     text_height = font.getmask(bidi_text).getbbox()[3]
#
# # Calculate the x, y position of the text
# x = (image.width - text_width) / 2
# y = (image.height - text_height) / 2
#
# transparency_percent = 100
# opacity_percentage = opacity_to_alpha(transparency_percent)
#
# # Define shadow offset and color
# shadow_offset = (3, 3)
# shadow_color = (100, 100, 100, opacity_percentage)  # Gray color for shadow
#
# # Draw shadow text ✏️ اللاين الي تحت فيه ظل او لا
# draw.text((x + shadow_offset[0], y + shadow_offset[1]), bidi_text, font=font, fill=shadow_color)
#
# # Define stroke width and color using RGB
# # stroke_width = 1 #✏️ 1vs0
# # stroke_fill = (255, 0, 0)  # Red color in RGB
#
# # Draw main text with stroke
# draw.text((x, y), bidi_text, font=font, fill=(27, 27, 27, opacity_percentage))
#
# # Save the modified image
# output_path = 'output_watermark.png'
# image.save(output_path)
#
# print(f"Text added and saved to {output_path}")
