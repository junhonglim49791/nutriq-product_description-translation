import pandas as pd
import time
import asyncio
from bs4 import BeautifulSoup
from googletrans import Translator



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

df = pd.read_excel("basic300734464062export1750487488629_0621-14-31-28.xlsx", header=0, skiprows=[1,2,3])

start_time = time.time()

translated_html_string_list = []
for i in range(0,  df.shape[0]):

    # Skip empty rows
    if(pd.isna(df.loc[i, "Main Description"])): 
        translated_html_string_list.append("")
        continue

    soup = BeautifulSoup(df.loc[i, "Main Description"], 'html.parser')
    print(f"Current row index: {i}")

    for text in soup.find_all(string=True):
        try:
            if text.strip():
                print(f"Current text: {text}")
                # Ingredients come with alot of "," that affects translations accurcy, send them in chunks to translate
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
                print(f"Translated text: {translated_text}")            

        except Exception as e:
            print(f"Error Message: {e}")

    
    translated_html_string_list.append(str(soup))

df["Translated Description"] = translated_html_string_list

df.to_excel("translated_product_description_ubuntu.xlsx", index=False)

end_time = time.time()

print(f"Time used: {end_time-start_time} seconds")