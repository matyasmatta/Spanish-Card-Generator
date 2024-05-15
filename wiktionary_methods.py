from wiktionaryparser import WiktionaryParser
from tqdm import tqdm
import csv

def format_wordtype(wordtype):
    map = {
        "noun": "N",
        "verb": "V",
        "adjective": "Adj",
        "adverb": "Adv",
        "conjuction": "Conj",
        "preposition": "Prep" 
    }
    return map[wordtype]

def format_lemma(lemma, wordtype, gender):
    match wordtype:
        case "N":
            match gender:
                case "m":
                    return f"el {lemma}"
                case "f":
                    return f"la {lemma}"
                case "m/f":
                    return f"el/la {lemma}"
        case "Adj":
            if lemma.endswith("o"):
                return f"{lemma}, {lemma[:-1]}a"
            else:
                return lemma
        case _:
            return lemma

def format_translation(translation):
    if "(" in translation:
        current_translation = translation.split(" ")
        search = False
        searched_item = str()
        for item in current_translation:
            if "(" in item and ")" in item:
                searched_item = item[1:-1]
                search = False
                break
            elif "(" in item:
                searched_item += item + " "
                search = True
            elif ")" in item:
                searched_item += item
                search = False
            elif search:
                searched_item += item + " "
        searched_item = searched_item.replace("(", "").replace(")","")
        searched_item = searched_item[:-1] if searched_item.endswith(" ") else searched_item
            
        return translation.replace(searched_item, "").replace("(", "").replace(")",""), searched_item
    else:
        return translation, None

def get_wiktionary_list(lemmas: list, output = None, debug =  False) -> list:
    return [get_lemma(item, output, debug) for item in tqdm(lemmas)]

def get_lemma(lemma: str, output, debug: bool) -> list:
    def determine_gender() -> None or str:
        nonlocal word
        original_string = word[0]['definitions'][0]['text'][0].replace("\xa0", " ")
        try:
            current_string = original_string.replace(original_string.split(" ")[0]+" ", "")
            if current_string.split(" ")[1] == "or":
                return "m/f"
            else:
                return current_string.split(" ")[0]
        except:
            return None
        
    try:
        parser = WiktionaryParser()
        word = parser.fetch(lemma, "spanish")
        wordtype = format_wordtype(word[0]['definitions'][0]['partOfSpeech'].split(" ")[0])
        translation = word[0]['definitions'][0]['text'][1]
        gender = determine_gender() if wordtype == "N" else None

        formatted_lemma = format_lemma(lemma, wordtype, gender)
        formatted_translation, meaning_hint = format_translation(translation)

        data = [formatted_lemma, formatted_translation, wordtype, gender, meaning_hint]
        if debug: print(data)
        if output: 
            with open(output, "a", encoding="utf8", newline="") as f:
                csv.writer(f).writerow(data)
        return data
    except:
        print(f"\nNo defintion found for {lemma}")

if __name__ == "__main__":
    lemmas = ['fascinante', 'docena', 'modelo', 'cien', 'correcto', 'dañar', 'miserable', 'gracia', 'estupidez', 'listo', 'fallar', 'opción', 'estructura', 'espiar', 'elegante', 'accidente', 'rubio', 'rayar', 'grano', 'generación', 'divorcio', 'faltar', 'punta', 'vacación', 'botón', 'fumar', 'honestamente', 'cariño', 'disfrutar', 'exacto', 'digno', 'celebrar', 'electricidad', 'detective', 'suicidio', 'voto', 'lobo', 'imbécil', 'adentro', 'victoria', 'increíble', 'pisar', 'interior', 'arco', 'bingo', 'arañar', 'absoluto', 'mercancía', 'crimen', 'enterrar', 'muñeca', 'nacimiento', 'impresión', 'valle', 'campar', 'derrota', 'criatura', 'pacífico', 'invisible']
    get_wiktionary_list(lemmas, output="test.csv")