import os
import re
import requests
import shutil

from module.customPdf import PDF
from PIL import Image
from urllib.parse import urlparse

def uriValidate(uri) -> bool:
    try:
        result = urlparse(uri)
        return all([result.scheme, result.netloc])
    except:
        return False

def processDifficulty(url: str, easy_difficulty: str = 'easy', medium_difficulty: str = 'medium', hard_difficulty: str = 'hard') -> dict:
    urls = {}

    if len(re.findall(r'/' + easy_difficulty, url)):
        urls["easy"] = url
        urls["medium"] = re.sub(r'/' + easy_difficulty, r'/' + medium_difficulty, url)
        urls["hard"] = re.sub(r'/' + easy_difficulty, r'/' + hard_difficulty, url)
    elif len(re.findall(r'/' + medium_difficulty, url)): # This is a medium question
        urls["easy"] = re.sub(r'/' + medium_difficulty, r'/' + easy_difficulty, url)
        urls["medium"] = url
        urls["hard"] = re.sub(r'/' + medium_difficulty, r'/' + hard_difficulty, url)
    elif len(re.findall(r'/' + hard_difficulty, url)): # This is a hard question
        urls["easy"] = re.sub(r'/' + hard_difficulty, r'/' + easy_difficulty, url)
        urls["medium"] = re.sub(r'/' + hard_difficulty, r'/' + medium_difficulty, url)
        urls["hard"] = url

    return urls

def extractImgFromHtml(image_list):
    for i in range(len(image_list)):
        image_list[i] = re.sub("'", '"', str(image_list[i]))
        image_list[i] = re.findall('img.*?src="(.*?)"', str(image_list[i]))

        ret = [item for item in image_list if item != []]

        return ret

def extractImgToPdf(image_list, pdf_name: str, width: int = 210, height: int = 297) -> None:
    print("Now processing: " + pdf_name)
    print(image_list)
    image_name = []

    for i in range(len(image_list)):
        for j in range(len(image_list[i])):
            print(i, j)
            print(image_list[i][j])
            response = requests.get(image_list[i][j], stream=True)

            name = pdf_name + str(i) + str(j) + ".png"
            with open(name, "wb") as out_file:
                shutil.copyfileobj(response.raw, out_file)
                image_name.append(name)

    pdf = PDF()
    for image in image_name:
        pdf.add_page()
        im = Image.open(image)
        w, h = im.size

        # Resize both, just in case :wink
        if (w > width):
            h = int(h * (width / w))
            w = width

        if (h > height):
            w = int(w * (height / h))
            h = height

        pdf.image(image, x = 0, y = 0, w = w, h = h)
        im.close()

        os.remove(image)

    pdf.output(pdf_name + ".pdf")
