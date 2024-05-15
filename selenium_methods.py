from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm

def process_data(word: str, translation: str, type: str) -> list:
    gender = None
    ### process data
    if "NOUN" in type:
        #### formatted for Anki Duolingo Format, i.e. with articles
        if translation.startswith("la" or "las"):
            gender = "f"
        if translation.startswith("el" or "los"):
            gender = "m"
        if "FEMININE" in type:
            gender = "f"
            word = "la " + word
        if "MASCULINE" in type:
            gender = "m"
            word = "el " + word
        #### fix for words that work with both genders
        if word.startswith("el la"):
            word = "el/la " + word[6:]
            gender = "m/f"
        type = "N"
    ### make sure to use " VERB" due to adverbs conflicting!
    if " VERB" in type:
        type = "V"
    if "ADJECTIVE" in type:
        #### adjectives are formatted into Anki Duolingo Format, i.e. inflected for both genders
        type = "Adj"
        if word.endswith("ado"):
            word = word + ", " + word[:-3] + "ada"
        elif word.endswith("ada"):
            word = word[:-3] + "ado" + ", " + word
    if "INTERJECTION" in type:
        type = "Conj"
    if "PREPOSITION" in type:
        type = "Prep"
    if "ADVERB" in type:
        type = "Adv"
    
    return [word, translation, type, gender]

def get_spanish_dict_data(lemmas: list, output = None, debug = False, headless = False) -> list:

    print(f"Initialising Selenium WebDriver instance with options: debug = {debug}, headless = {headless}, output = {output}.")

    # Create a Firefox WebDriver instance
    options = Options()
    service = Service(GeckoDriverManager().install())
    options.headless = headless  # Run Firefox in headless mode (without GUI)
    driver = webdriver.Firefox(service=service, options=options)

    def accept_cookies(driver=driver):
        button = driver.find_element(By.CLASS_NAME, "css-1mour4p")
        button.click()

    # Initialize an empty list to store the results
    results = []

    try:
        for lemma in tqdm(lemmas):
            try:
                try:
                    timeout = 5
                    driver.get(f"https://www.spanishdict.com/translate/{lemma}")
                    WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.ID, "quickdef1-es")))  # Wait for Spanish definition
                    try:
                        accept_cookies()
                    except:
                        pass
                except TimeoutException:
                    print(f"\nTimeout: Failed to load SpanishDict page for '{lemma}' in {timeout} seconds, skipping the lemma.")
                    continue

                # Find elements containing the translation, word type, and gender
                try:
                    translation = driver.find_element(By.ID, "quickdef1-es").text
                except:
                    translation = driver.find_element(By.ID, "quickdef1-en").text
                type = driver.find_element(By.CLASS_NAME, "j9pFe8zP").text

                data = process_data(lemma, translation, type)
                results.append(data)
                if debug: print(data)
                if output: 
                    with open(output, "a", encoding="utf8") as f: 
                        f.write("%s\n" % data)
            except:
                pass
    finally:
        driver.quit()

    return results

if __name__ == "__main__":
    # Example list of lemmas
    lemmas = ['fascinante', 'docena', 'modelo', 'cien', 'correcto', 'dañar', 'miserable', 'gracia', 'estupidez', 'listo', 'fallar', 'opción', 'estructura', 'espiar', 'elegante', 'accidente', 'rubio', 'rayar', 'grano', 'generación', 'divorcio', 'faltar', 'punta', 'vacación', 'botón', 'fumar', 'honestamente', 'cariño', 'disfrutar', 'exacto', 'digno', 'celebrar', 'electricidad', 'detective', 'suicidio', 'voto', 'lobo', 'imbécil', 'adentro', 'victoria', 'increíble', 'pisar', 'interior', 'arco', 'bingo', 'arañar', 'absoluto', 'mercancía', 'crimen', 'enterrar', 'muñeca', 'nacimiento', 'impresión', 'valle', 'campar', 'derrota', 'criatura', 'pacífico', 'invisible']

    # Get data from SpanishDict
    lemma_data = get_spanish_dict_data(lemmas)

    with open("test.txt", "w", encoding="utf8") as f:
        for item in lemma_data:
            f.write("%s\n" % item)

    # Print the results
    for data in lemma_data:
        print(data)
