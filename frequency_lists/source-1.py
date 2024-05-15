def process(source="frequency_lists\source-1.txt", output="processed-1.txt"):
    with open(source, "r", encoding="utf8") as f:
        lines = f.readlines()
        processed_lines = [item.replace("\t", "").replace("\n", "") for item in lines]
        lemmas = [item.split()[-1] for item in processed_lines]
        unique_lemmas = list(set(lemmas))
        print(unique_lemmas)
    
    if output: 
        with open(output, "w", encoding="utf8") as file:
            for item in unique_lemmas:
                file.write("%s\n" % item)

process()