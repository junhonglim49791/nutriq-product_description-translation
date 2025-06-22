import pandas as pd
import time
import asyncio
from bs4 import BeautifulSoup
from googletrans import Translator

# async def translate_bulk():
#     async with Translator() as translator:
#         translations = await translator.translate(["""Skimmed Milk Powder (31%), 
#         Milk Proteins [Calcium Caseinate (19%), Sodium Caseinate (10%)], 
#         Maltodextrin (Corn)', 'Vegetable Oil (Canola, Sunflower), 
#         Minerals (Potassium Citrate, Sodium Chloride, Magnesium Carbonate, 
#         Potassium Phosphate, Ferric Pyrophosphate, Calcium Phosphate, Zinc Sulphate, 
#         Copper Gluconate, Manganese Sulphate, Sodium Fluoride, Potassium Iodide, 
#         Sodium Selenite, Sodium Molybdate, Chromium Chloride), Vegetable Gum (414), 
#         Fructo-oligosaccharide, Flavours, Inulin, Medium Chain Triglycerides, Glucose Syrup (Corn), Sugar, 
#         Fish Oil, Parsley, Emulsifiers (472c, Soy Lecithin, 471), Flavour Enhancer (621), Antioxidants (301, 304, 306), 
#         Vitamins (Vitamin E Acetate, Nicotinamide, Calcium Pantothenate, Sodium Ascorbate, Pyridoxine Hydrochloride, Thiamine Hydrochloride, 
#         Vitamin A Acetate, Riboflavin, Folic Acid, Phytomenadione, Cholecalciferol, Cyanocobalamin, Biotin), 
#         Colour (Curcumin)."""], dest='ms')
#         for translation in translations:
#             print(translation.origin, ' -> ', translation.text)


# asyncio.run(translate_bulk())

"""----------------------------------------------------------------------------------------------------------------------------------------------------------------"""
df = pd.read_excel("product_description_ubuntu.xlsx", header=0, skiprows=[1,2,3])


start_time = time.time()

async def translate_text_in_bulk(text_list):
     async with Translator(timeout=20.0) as translator:
         translated_objects = await translator.translate(text_list, src="en", dest="ms")
         translated_text = []
         for translated_object in translated_objects:
            translated_text.append(translated_object.text)
         return translated_text

async def translate_text(text):
     async with Translator(timeout=10.0) as translator:
         translate_obj = await translator.translate(text, src="en", dest="ms")
         return translate_obj.text

translated_html_string_list = []
original_text = []
for i in range(0,  df.shape[0]):

    if(pd.isna(df.loc[i, "Main Description"])): #added check to pass current loop
        translated_html_string_list.append("")
        continue

    soup = BeautifulSoup(df.loc[i, "Main Description"], 'html.parser')
    print(f"Current row index: {i}")

    for text in soup.find_all(string=True):
        try:
            if text.strip():
                # print(f"Current text: {text}")
                # print(f"Current text length: {len(text)}")
                if(text.count(",") > 10):
                    chunks = text.strip().split(",")
                    translated_chunks_list = []
                    for chunk in chunks:
                        translated_chunk = asyncio.run(translate_text(chunk.strip()))
                        translated_chunks_list.append(translated_chunk)
                    translated_text = ", ".join(translated_chunks_list)
                else:
                    translated_text = asyncio.run(translate_text(text.strip()))

                text.replace_with(translated_text)    
                # print(f"Translated text: {translated_text}")            
                # original_text.append(text.strip())
                # print(f"Current text: {text}")
                # print(asyncio.run(translate_text(text.strip())).text)
                # text.replace_with(asyncio.run(translate_text(text.strip())))

        except Exception as e:
            print(f"Error Message: {e}")
    # print(f"Original text list : {original_text}")
    # batch_size = 1
    # translated_text = []
    # for i in range(0, len(original_text), batch_size):
    #     batch = original_text[i: i+batch_size]
    #     translated_batch = asyncio.run(translate_text_in_bulk(batch))
    #     translated_text.extend(translated_batch)

    # translated_text_index = 0
    # for text in soup.find_all(string=True):
    #     if text.strip():
    #         print(f"Translated text: {translated_text[translated_text_index]}")
    #         text.replace_with(translated_text[translated_text_index])
    #         translated_text_index += 1
    
    translated_html_string_list.append(str(soup))

df["Translated Description"] = translated_html_string_list

df.to_excel("translated_product_description_ubuntu.xlsx", index=False)

end_time = time.time()

print(f"Time used: {end_time-start_time} seconds")

""" Use to test single row 

soup = BeautifulSoup(df.loc[0, "Main Description"], 'html.parser')

# print(soup.prettify())
# translator = Translator()

# for text in soup.find_all(string=True):
#     # print(text.strip())
#     # print(translator.translate(text.strip(), src="en", dest="ms").text)
#     text.replace_with(translator.translate(text.strip(), src="en", dest="ms").text)


# print(soup.prettify()) # return string
print(str(soup)) # return string

with open('single.html', 'w', encoding="utf-8") as f:
     f.write(str(soup))
"""


"""Challenges
API time out
Data formatting
old version doesnt support exception which doesn't show whats wrong
return repeated translations because the responses might be corrupted using free api (especially long text nodes like ingredients)
"""
"""Solution 1: App script
cant handle html tags properly

Solution 2: XML parser
need to clean html to convert to xml without issues, can settle nested tags which solution 1 cannot there might be too many conditions to be considered

Solution 3: Bulk vs Basic
According to gpt bulk is inefficient, but bulk call i use ~1300s, basic call i used ~311s

problem:
1. ingredient list with alot of comma and too long, causes repeated mistranslations. solved by passing the long string in chunks

"""
"""What's next?
Get only text node insert as string, but no column for malay. (currently no need, translation works)


try to simply type something for a few products and download the excel file, see new column will be generated or not, so that i can just copy paste the malay description
if not need to first upload malay -> copy malay description to target block in seller center -> reupload english


"""

""" Test cases (row number follow excel)
row 2 ok
row 3 ok
"""