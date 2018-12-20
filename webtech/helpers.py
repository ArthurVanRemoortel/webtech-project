from .models import *
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import requests

LOREM_1_P = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. " \
            "In vestibulum ex ut pellentesque gravida. Nunc fermentum, tortor ut " \
            "finibus rhoncus, nibh mi mollis erat, eu convallis nisi orci sit amet tortor. " \
            "Aliquam hendrerit enim nunc, at ultrices quam laoreet at. " \
            "Nulla pretium neque in magna fermentum sollicitudin. " \
            "Donec efficitur convallis tristique. Nunc bibendum sollicitudin " \
            "felis eget interdum. Pellentesque dignissim, augue in efficitur imperdiet, lectus " \
            "mauris iaculis quam, sed maximus eros elit quis tellus. "

LOREM_2_P = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. " \
            "In vestibulum ex ut pellentesque gravida. Nunc fermentum, tortor ut " \
            "finibus rhoncus, nibh mi mollis erat, eu convallis nisi orci sit amet tortor. " \
            "Aliquam hendrerit enim nunc, at ultrices quam laoreet at. " \
            "Nulla pretium neque in magna fermentum sollicitudin. " \
            "Donec efficitur convallis tristique. Nunc bibendum sollicitudin " \
            "felis eget interdum. Pellentesque dignissim, augue in efficitur imperdiet, lectus " \
            "mauris iaculis quam, sed maximus eros elit quis tellus. " \
            "\n" \
            "Suspendisse et elit at leo consectetur porttitor nec et augue. " \
            "Donec tellus risus, ultricies at ante tempor, blandit laoreet metus. " \
            "Praesent scelerisque bibendum mi, sit amet efficitur arcu malesuada quis. " \
            "Nulla sit amet massa scelerisque est porttitor ullamcorper non vel nibh. " \
            "Praesent ut justo non risus varius malesuada a et tortor. Sed tempus, quam at convallis imperdiet, " \
            "risus lorem bibendum elit, nec molestie lacus lacus nec neque. Integer a mauris " \
            "ut turpis sagittis hendrerit nec in libero. Maecenas vel dolor est. Fusce auctor " \
            "lorem consequat blandit fermentum. Cras eros nulla, finibus ut lorem a, " \
            "iaculis consequat elit. Mauris vulputate neque quis sem eleifend, vel vestibulum " \
            "nunc placerat. Ut id placerat magna."


def django_image_from_url(url):
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))
    file = BytesIO()
    image.save(file, 'JPEG')
    file.seek(0)
    image_name = url.split("/")[-1]
    if ".jpeg" not in image_name and ".jpg" not in image_name and ".png" not in image_name:
        image_name += '.jpg'
    return ContentFile(file.read(), image_name)


def django_image_from_file(path):
    image = Image.open(path)
    file = BytesIO()
    image.save(file, 'JPEG')
    file.seek(0)
    image_name = path.split("/")[-1]
    return ContentFile(file.read(), image_name)