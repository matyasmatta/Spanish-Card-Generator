def get_lemmas(file: str, output=None) -> list:
    with open(file, "r", encoding="utf8") as f:
        lines = f.readlines()
        lemmas = [item.split("\t")[0] for item in lines]
        filtered_lemmas = [s for s in lemmas if not s[0].isupper()]
        filtered_lemmas = [s.replace('la ', '').replace('el ', '').replace('/ ', '') for s in filtered_lemmas]
        filtered_lemmas = [s.lstrip() for s in filtered_lemmas]
        filtered_lemmas = [s.split(',')[0] if ',' in s else s for s in filtered_lemmas]
        print(filtered_lemmas)

    if output: 
        with open(output, "w", encoding="utf8") as file:
            for item in filtered_lemmas:
                file.write("%s\n" % item)

    return filtered_lemmas

def get_new_lemmas(current: str, additional: str, output=None) -> list:
    with open(current, "r", encoding="utf8") as f:
        lines = f.readlines()
        current_list = [item.replace("\n", "").split()[0] for item in lines]
    with open(additional, "r", encoding="utf8") as f:
        lines = f.readlines()
        additional_list = [item.replace("\n", "").split()[0] for item in lines]
        additional_list = [s for s in additional_list if not s[0].isupper()]
        additional_list = [s for s in additional_list if len(s) > 3]

    
    new_lemmas = list(set(additional_list) - set(current_list))

    if output: 
        with open(output, "w", encoding="utf8") as file:
            for item in new_lemmas:
                file.write("%s\n" % item)
    
    return new_lemmas

get_new_lemmas("lemmas.txt", "frequency_lists/processed-1.txt")
