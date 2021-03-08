import cv2
import pytesseract
from pdf2image import convert_from_path

# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# poppler_path = r"C:\Users\xia.he\AppData\Local\Programs\poppler-21.02.0\Library\bin"

# images = convert_from_path("./data/scannedPDFs/test.pdf", poppler_path)


# pdfs = r"provide path to pdf file"
# pages = convert_from_path(pdfs, 350)

# i = 1
# for page in pages:
#     image_name = "Page_" + str(i) + ".jpg"  
#     page.save(image_name, "JPEG")
#     i = i+1        

img = cv2.imread("./data/scannedPDFs/BB_Feldbau_40_2006.png")
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

text = pytesseract.image_to_string(img,lang="deu")
print(text)

cv2.imshow("Result", img)

cv2.waitKey(0)