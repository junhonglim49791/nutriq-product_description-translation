# <img src="lazada-removebg-preview-crop-bottom-removebg-preview.png" width="50"> **Lazada Product Description Translation**
A Python script to translate long, HTML-formatted product descriptions from English to Malay using **`py-googletrans`**.

## 🎯 Purpose

This script was created to address the challenge of translating long, HTML-formatted product descriptions from English to Malay, particularly in Lazada's bulk edit Excel files.

Initially, I attempted to use Google Sheets' built-in `GOOGLETRANSLATE` function, but it also translated HTML tags — breaking the formatting and structure. I then tried writing a custom Google Apps Script to isolate and translate only the text, but handling nested `<span>` tags required parsing the HTML into XML. End up spending extra time dealing with unexpected formatting issues. 

At that time, this issue was time-sensitive due to short notice that requires ecommerce stores to include Bahasa Malaysia in their product listings. To solve this properly, I switched to Python, where libraries like **`BeautifulSoup`** make it easy to extract and replace text nodes without touching the HTML structure. 

## 📌 Example

### Input:
```html
<p
  style="
    line-height: 1.7;
    text-align: left;
    text-indent: 0;
    margin-left: 0;
    margin-top: 0;
    margin-bottom: 0;
  "
>
  <span style="color: rgb(102, 102, 102); font-size: 18pt"
    >ActivMax Keto 3:1 is formulated specially to manage nutritional issues in
    ketogenic practices, which includes minimizing glucose crashes, nutrient
    deficiency and diarrhoea. ActivMax Keto 3:1 is a complete nutritional
    drink with vitamins, minerals, DHA, ALA, Omega-9, and calcium to promote
    healthy growth and development of children. With an advanced blend of
    healthy fats with medium-chain triglycerides (MCT) and long-chain fatty
    acids (LCFA), ActivMax Keto 3:1 provides both fast and slow release of
    ketone energy suitable for children. Moreover, it is lactose-free, high in
    soluble fiber and high-quality plant-based soy-isolated protein to
    minimize the risk of diarrhoea events throughout their ketogenic journey,
    providing maximum gut comfort.</span
  >
</p>

```
### Output:
```html
<p
  style="
    line-height: 1.7;
    text-align: left;
    text-indent: 0;
    margin-left: 0;
    margin-top: 0;
    margin-bottom: 0;
  "
>
  <span style="color: rgb(102, 102, 102); font-size: 18pt"
    >Activmax Keto 3: 1 dirumuskan khas untuk menguruskan isu pemakanan dalam
    amalan ketogenik, yang termasuk meminimumkan kemalangan glukosa,
    Kekurangan nutrien dan cirit -birit. Activmax Keto 3: 1 adalah minuman
    pemakanan lengkap dengan vitamin, mineral, DHA, Ala, Omega-9, dan kalsium
    untuk menggalakkan pertumbuhan dan perkembangan kanak -kanak yang sihat.
    Dengan campuran lemak yang sihat dengan trigliserida rantaian sederhana
    (MCT) dan asid lemak rantaian panjang (LCFA), Activmax Keto 3: 1
    menyediakan pelepasan tenaga keton yang cepat dan perlahan yang sesuai
    untuk kanak -kanak. Selain itu, Ia bebas laktosa, Tinggi serat larut dan
    protein berasaskan soya berasaskan loji yang berkualiti tinggi untuk
    meminimumkan risiko peristiwa cirit-birit sepanjang perjalanan ketogenik
    mereka, menyediakan keselesaan usus maksimum.</span
  >
</p>

```
## 🛠 Requirements

- Python 3.8 or later
- The following Python libraries:
  - pandas
  - openpyxl
  - beautifulsoup4
  - googletrans==4.0.2

## 🚀 How to Run

1. **Clone the repository:**

   ```bash
   git clone https://github.com/junhonglim49791/nutriq-product_description-translation.git
   
   cd nutriq-product_description-translation
   ```  
2. **Create a virtual environment:**  
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3. **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```
4. **Prepare your input Excel file:**  
  The script expects an excel file containing Lazada product data. There should be a column named **`Main Description`** which contains HTML-formatted product descriptions in English.

5. **Run the script:**
   ```bash
   python3 main.py
   ```
6. **Output:**

   After processing, a new Excel file will be generated. It will contain two columns:

   - **Main Description** – the original English HTML-formatted content
   - **Translated Description** – the Malay-translated version with HTML structure preserved

## 📝 Translation Notes

- **Comma-heavy content (ingredient lists)  cause duplicate translations (Solved):**  
  Long strings are translated in chunks to improve translation accuracy.

- **Translation quality disclaimer:**  
  May produce awkward or inaccurate translations for some words in a sentence. However, after testing on **75 product descriptions**, it still provides **satisfactory results in most cases**.  
  👉 See the [🔍 Translation Accuracy Comparison](#-translation-accuracy-comparison) section for detailed examples and recommendations.

- **Empty rows are skipped:**  
  Rows without content in the `Main Description` column are ignored.

- **Limitations:**  
  The script uses the unofficial `googletrans` library, which depends on Google Translate’s web API. Therefore, this will not work at all times or could be blocked at anytime.

- **Extra space in kata ganda (Not solve) :**  
  Translations of duplicated words (e.g., *kanak-kanak*) may include an unwanted space before the hyphen (*kanak -kanak*).

- **Missing space after bold text (Not solve):**  
   When bold formatting ends and is followed by a regular word, the space may be lost.

  For example:  
  `ACTIVMAX Keto 3:1 is` → `ACTIVMAX Keto 3:1adalah`

## 🔍 Translation Accuracy Comparison

The translation quality from `googletrans` is **not as accurate** as the official Google Translate on web or ChatGPT.

### 📌 Example 1
**Input:**  
*Cartilage is the connective tissue that covers the ends of your bones to form a smooth, shock-absorbing surface for your joints.*

| Source        | Translated Output |
|---------------|-------------------|
| `googletrans` | Rawan adalah tisu penghubung yang meliputi hujung tulang anda untuk **membentuk permukaan yang menghilangkan dan menyerap yang licin** untuk sendi anda. |
| Google Web    | Rawan adalah tisu penghubung yang menutupi hujung tulang anda untuk **membentuk permukaan licin, menyerap kejutan untuk sendi anda.** |
| ChatGPT       | Rawan ialah tisu penghubung yang menutupi hujung tulang anda untuk **membentuk permukaan yang licin dan menyerap hentakan** bagi sendi-sendi anda. |

---

### 📌 Example 2
**Input:**  
*Choosing the right calcium is important, and elemental calcium is key because it represents the actual amount your body absorbs for bone growth and other health benefits.*

| Source        | Translated Output |
|---------------|-------------------|
| `googletrans` | Memilih kalsium yang betul adalah **kalsium penting dan elemen adalah kunci** kerana ia adalah jumlah sebenar kalsium badan anda menyerap untuk pertumbuhan tulang dan manfaat kesihatan yang lain. |
| Google Web    | Memilih kalsium yang betul adalah **penting dan unsur kalsium adalah kunci** kerana ia adalah jumlah sebenar kalsium yang diserap oleh badan anda untuk pertumbuhan tulang dan manfaat kesihatan yang lain. |
| ChatGPT       | Memilih kalsium yang tepat **adalah penting, dan kalsium elemental merupakan kunci** kerana ia adalah jumlah sebenar kalsium yang diserap oleh tubuh anda untuk pertumbuhan tulang dan manfaat kesihatan yang lain. |

---

> ⚠️ **Recommendation:**  
> This script was designed as a **quick fix** to help adapt product listings in response to sudden e-commerce policy changes requiring Bahasa Malaysia descriptions.
>
> It prioritizes **speed and HTML handling** over translation accuracy. If **high-quality translation** is critical for your use case:
> - Use service like the **Google Cloud Translation API**
> - Export the cleaned/plain text and translate using **Google Translate Web** or **ChatGPT**



