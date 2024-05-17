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
                break
            elif search:
                searched_item += item + " "
        searched_item = searched_item.replace("(", "").replace(")","")
        searched_item = searched_item.strip()
            
        return translation.replace(f"({searched_item})", ""), searched_item
    else:
        return translation, None

def get_wiktionary_list(lemmas: list, output = None, debug =  False) -> list:
    return [get_lemma(item, output, debug) for item in tqdm(lemmas)]

def get_translation(word: dict) -> str:
    def handle_duplicates(definitions: list) -> list:
        return list(set(definitions))
    
    def handle_additionals(additionals: list) -> str:
        try:
            for item in additionals:
                if not item:
                    return None
                else:
                    if "transitive" in item:
                        return item
                    elif len(item.split(" ")) < 2:
                        return item
            return None
        except:
            return None

    def convert_into_html(definitions: list) -> str:
        def correct_verb(temporary_hold: str) -> str:
            temporary_hold = temporary_hold.strip()
            if "to " in temporary_hold:
                result = ""
                for item in temporary_hold.split(" "):
                    if "to " in result:
                        if item == "to":
                            pass
                        else:
                            result += item+" "
                    else:
                        result += item+" "
                result = result.strip()
                return result
            else:
                return temporary_hold
            
        def correct_hold(hold: str) -> str:
            result = hold.strip().replace("  ", " ")
            result = result[:-1] if result.endswith(",") else result
            return result
            
        html_list = "<ul>" 
        temporary_hold = ""
        for item in definitions:
            temporary_hold += correct_verb(item) + ", "
            if len(temporary_hold.split(" ")) > 5: # the higher this integer, the fewer HTML lists in the result
                temporary_hold = correct_hold(correct_verb(temporary_hold))
                html_list += f"  <li>{temporary_hold}</li>" if temporary_hold not in html_list else ""
                final_hold = temporary_hold
                temporary_hold = ""
            else:
                final_hold = correct_hold(temporary_hold)

        try:
            if not final_hold in html_list:
                html_list += f"  <li>{final_hold}</li>"
        except:
            raise ValueError("There was some error inside the convert_into_html() function, please inspect.")
        if html_list.count("<li>") <= 1:
            return final_hold.strip()
        else:
            html_list += "</ul>"
            return html_list

    definitions = []
    for item in word[0]['definitions']:
        for i in range(len(item['text'])):
            if i == 0:
                pass
            else:
                if len(item['text'][i].split(" ")) > 20:
                    pass
                else:
                    definitions.append(item['text'][i])
    definitions2, additionals = [], []
    for item in definitions:
        translation, additional = format_translation(item)
        definitions2.append(translation)
        additionals.append(additional)

    definitions2 = handle_duplicates(definitions2)
    if len(definitions2) > 1:
        definitions2 = convert_into_html(definitions2)
    else:
        definitions2 = str(definitions2[0])

    return definitions2, handle_additionals(additionals)

def get_synonyms(word: dict) -> (str or None):
    try:
        data = word[0]['definitions'][0]['examples'][0]
        if data.startswith("Synonyms:"):
            data = data.replace("Synonyms: ","")
            if len(data.split(", ")) > 4:
                return ", ".join(data.split(", ")[0:5])
            else:
                return data
        else:
            return None
    except:
        return None
    
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
        formatted_translation, meaning_hint = get_translation(word)
        gender = determine_gender() if wordtype == "N" else None
        formatted_lemma = format_lemma(lemma, wordtype, gender)
        synonym_aid = get_synonyms(word)

        data = [formatted_lemma, formatted_translation, wordtype, gender, meaning_hint, synonym_aid]
        if debug: print(data)
        if output: 
            with open(output, "a", encoding="utf8", newline="") as f:
                csv.writer(f).writerow(data)
        return data
    except:
        print(f"\nNo defintion found for {lemma}")

if __name__ == "__main__":
    lemmas = ["agalla", "pues", "lindo", "copia", "mortal"]
    # lemmas = ['fumar', 'dañar', 'fascinante', 'docena', 'modelo', 'cien', 'correcto', 'miserable', 'gracia', 'estupidez', 'listo', 'fallar', 'opción', 'estructura', 'espiar', 'elegante', 'accidente', 'rubio', 'rayar', 'grano', 'generación', 'divorcio', 'faltar', 'punta', 'vacación', 'botón', 'fumar', 'honestamente', 'cariño', 'disfrutar', 'exacto', 'digno', 'celebrar', 'electricidad', 'detective', 'suicidio', 'voto', 'lobo', 'imbécil', 'adentro', 'victoria', 'increíble', 'pisar', 'interior', 'arco', 'bingo', 'arañar', 'absoluto', 'mercancía', 'crimen', 'enterrar', 'muñeca', 'nacimiento', 'impresión', 'valle', 'campar', 'derrota', 'criatura', 'pacífico', 'invisible']
    get_wiktionary_list(lemmas, output="test.csv")