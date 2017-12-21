my_word = "_ l _ p _"
my_word = my_word.replace(" ", "")
length_match = ['ahead', 'alarm', 'amble', 'amigo', 'anent', 'angst', 'apple', 
                'arias', 'asked', 'bedew', 'birch', 'bleak', 'boles', 'bowel', 
                'bract', 'bulls', 'burns', 'bursa', 'cable', 'chaff', 'close', 
                'cocci', 'codex', 'congo', 'crane', 'craws', 'cream', 'crock', 
                'damns', 'dents', 'dicta', 'doves', 'dwell', 'elope', 'embed', 
                'equal', 'fetch', 'fired', 'flesh', 'floss', 'foots', 'forms', 
                'frock', 'galas', 'galls', 'gasps', 'gauge', 'getup', 'gleam', 
                'gloom', 'guava', 'hazed', 'henna', 'hutch', 'idler', 'jilts', 
                'kited', 'korea', 'leery', 'level', 'lipid', 'loose', 'motif', 
                'notes', 'obese', 'odder', 'orbed', 'pasta', 'pawns', 'payee', 
                'popes', 'pubic', 'quern', 'rests', 'ruder', 'ruler', 'scoff', 
                'serge', 'sewed', 'sigma', 'sills', 'silos', 'snaky', 'snore', 
                'sprit', 'stony', 'swine', 'tasks', 'their', 'token', 'troll', 
                'truth', 'tuned', 'udder', 'wages', 'waxed', 'windy', 'wound', 
                'wrist', 'yells']
word_match = length_match[:]

i, j = 0, 0
i_letter = ""
j_word = ""
ij_letter = ""
while i < len(my_word):
    i_letter = my_word[i]
    if my_word[i] == "_":
        pass
    else:
        for j in range(len(length_match)):
            j_word = length_match[j]
            ij_letter = length_match[j][i]
            if length_match[j][i] != my_word[i]:
                try:
                    word_match.remove(length_match[j])
                except:
                    continue
    i += 1
    j = 0