def count_shared_values(d):
    # Count occurrences of each value
    value_counts = Counter(d.values())

    # Count how many values have duplicates
    shared_value_count = sum(1 for count in value_counts.values() if count > 1)

    return shared_value_count


def ith_largest_unique_value(sorted_dict, i):
    # Extract unique values from the dictionary
    unique_values = list(set(sorted_dict.values()))
    # Sort unique values in descending order
    unique_values.sort(reverse=True)
    
    # Check if i is within bounds
    if i <= 0 or i > len(unique_values):
        return None  # Return None if i is out of bounds
    
    # Return the i-th largest unique value
    return unique_values[i - 1]


def position_in_descending_order(sorted_dict, value):
    # Extract unique values from the dictionary
    unique_values = list(set(sorted_dict.values()))
    # Sort unique values in descending order
    unique_values.sort(reverse=True)
    
    # Find the position of the value
    return unique_values.index(value) + 1  # +1 to convert index to position


def decrypt_symbols_frequence(C):

    byte_list = []  # Liste qui va contenir chaque byte du message en binaire

    # Diviser le message encodé en bytes et mettre chaque byte en ordre
    # dans la liste
    while C:
        byte_list.append(C[:8])
        C = C[8:]

    bytes_frequencies = {}

    for byte in byte_list:
        if byte in bytes_frequencies:
            bytes_frequencies[byte] += 1
        else:
            bytes_frequencies[byte] = 1

    for byte in bytes_frequencies:
        bytes_frequencies[byte] /= len(byte_list)

    bytes_frequencies = dict(sorted(bytes_frequencies.items(), key=lambda item: (-item[1], byte_list.index(item[0]))))

    for byte in bytes_frequencies.keys():
        first_symbol = next(iter(symbols_frequencies))
        symbols_frequencies.pop(first_symbol)
        byte_list = [first_symbol if x == byte else x for x in byte_list]

    M = "".join(byte_list)

    return M


def decrypt_symbols_and_pairs_frequence(C):
    
    decrypt_start = time.time()

    # Découper C en bytes
    byte_list = []
    while C:
        byte_list.append(C[:8])
        C = C[8:]

    # Prendre la fréquence de chaque byte dans C
    bytes_frequencies = {}
    for byte in byte_list:
        if byte in bytes_frequencies:
            bytes_frequencies[byte] += 1
        else:
            bytes_frequencies[byte] = 1

    # Normaliser les fréquences
    for byte in bytes_frequencies:
        bytes_frequencies[byte] /= len(byte_list)

    bytes_frequencies = dict(sorted(bytes_frequencies.items(), key=lambda item: (-item[1], byte_list.index(item[0]))))

    # --------
    # print(bytes_frequencies)
    # print("\n---------------------------\n")
    # print(symbols_frequencies)
    # print("\n---------------------------\n")
    # print(count_shared_values(symbols_frequencies))
    # print("\n---------------------------\n")
    # print(pairs_frequencies)
    # --------

    # Phase de déchiffrement
    for i in range(len(byte_list)):
        if len(byte_list[i]) != 8: # Si le byte a été déjà remplacé
            continue
        else:
            byte = byte_list[i]  # Byte actuel
            byte_frequence = bytes_frequencies[byte]  # Fréquence du byte dans C
            # Position de cette fréquence dans la liste des fréquences des bytes
            # dans C (on compte seulement les fréquences uniques)
            pos_freq_byte = position_in_descending_order(bytes_frequencies, byte_frequence)
            print(byte)
            print(pos_freq_byte)
            print("\n---------------------------\n")
            # Fréquence correspondante à la position dans la liste de fréquences 
            # des symboles
            target_frequency = ith_largest_unique_value(symbols_frequencies, pos_freq_byte)
            # Prendre tous les symboles avec cette fréquence
            selected_symbols = [symb for symb, freq in symbols_frequencies.items() if freq == target_frequency]
            # print(selected_symbols)
            if len(selected_symbols) == 1 or i == 0:
                byte_list = [selected_symbols[0] if elem == byte else elem for elem in byte_list]
                del symbols_frequencies[selected_symbols[0]]
                del bytes_frequencies[byte]
            else:
                if i != 0:
                    prev_symbol = byte_list[i-1]
                    freq_pairs = sorted([(symbols[1], frequence) for symbols, frequence in pairs_frequencies.items() if symbols[0] == prev_symbol], key=lambda x: x[1], reverse=True)
                    found_match = False
                    for pair in freq_pairs:
                        if pair[0] in selected_symbols:
                            byte_list = [pair[0] if elem == byte else elem for elem in byte_list]
                            del symbols_frequencies[pair[0]]
                            del bytes_frequencies[byte]
                            found_match = True
                            break
                    if not(found_match):
                        symbol = freq_pairs[0][0]
                        byte_list = [symbol if elem == byte else elem for elem in byte_list]
                        del symbols_frequencies[freq_pairs[0][0]]
                        del bytes_frequencies[byte]
                    
    M = "".join(byte_list)

    decrypt_end = time.time()

    print("Le temps pour déchiffrer C est : " + str(decrypt_end - decrypt_start))

    return M


def decrypt_pairs_frequence(C):
    # combinations_frequencies = {pair: 0 for pair in permutations(symboles, 2)}

    pairs_frequencies = {}
    
    byte_list = []  # Liste qui va contenir chaque byte du message en binaire

    # Diviser le message encodé en bytes et mettre chaque byte en ordre
    # dans la liste
    while C:
        byte_list.append(C[:8])
        C = C[8:]

    for i in range(len(byte_list)):
        if i + 1 < len(byte_list):
            pair = (byte_list[i], byte_list[i+1])
            if pair in pairs_frequencies:
                pairs_frequencies[pair] += 1
            else:
                pairs_frequencies[pair] = 1

    nb_pairs = sum(pairs_frequencies.values())

    for pair in pairs_frequencies:
        pairs_frequencies[pair] /= nb_pairs

    print( dict(sorted(pairs_frequencies.items(), key=lambda item: item[1], reverse=True)))





def test_prep():
    url = "https://www.gutenberg.org/ebooks/13846.txt.utf-8"  # Example URL (replace with your desired URL)
    text = load_text_from_web(url)
    url = "https://www.gutenberg.org/ebooks/4650.txt.utf-8"  # Example URL (replace with your desired URL)
    corpus = text + load_text_from_web(url)

    symboles = ['b', 'j', '\r', 'J', '”', ')', 'Â', 'É', 'ê', '5', 't', '9', 'Y', 
                '%', 'N', 'B', 'V', '\ufeff', 'Ê', '?', '’', 'i', ':', 's', 'C', 
                'â', 'ï', 'W', 'y', 'p', 'D', '—', '«', 'º', 'A', '3', 'n', '0', 
                'q', '4', 'e', 'T', 'È', '$', 'U', 'v', '»', 'l', 'P', 'X', 'Z', 
                'À', 'ç', 'u', '…', 'î', 'L', 'k', 'E', 'R', '2', '_', '8', 'é', 
                'O', 'Î', '‘', 'a', 'F', 'H', 'c', '[', '(', "'", 'è', 'I', '/', 
                '!', ' ', '°', 'S', '•', '#', 'x', 'à', 'g', '*', 'Q', 'w', '1', 
                'û', '7', 'G', 'm', '™', 'K', 'z', '\n', 'o', 'ù', ',', 'r', ']', 
                '.', 'M', 'Ç', '“', 'h', '-', 'f', 'ë', '6', ';', 'd', 'ô', 'e ', 
                's ', 't ', 'es', ' d', '\r\n', 'en', 'qu', ' l', 're', ' p', 'de', 
                'le', 'nt', 'on', ' c', ', ', ' e', 'ou', ' q', ' s', 'n ', 'ue', 
                'an', 'te', ' a', 'ai', 'se', 'it', 'me', 'is', 'oi', 'r ', 'er', 
                ' m', 'ce', 'ne', 'et', 'in', 'ns', ' n', 'ur', 'i ', 'a ', 'eu', 
                'co', 'tr', 'la', 'ar', 'ie', 'ui', 'us', 'ut', 'il', ' t', 'pa', 
                'au', 'el', 'ti', 'st', 'un', 'em', 'ra', 'e,', 'so', 'or', 'l ', 
                ' f', 'll', 'nd', ' j', 'si', 'ir', 'e\r', 'ss', 'u ', 'po', 'ro', 
                'ri', 'pr', 's,', 'ma', ' v', ' i', 'di', ' r', 'vo', 'pe', 'to', 
                'ch', '. ', 've', 'nc', 'om', ' o', 'je', 'no', 'rt', 'à ', 'lu', 
                "'e", 'mo', 'ta', 'as', 'at', 'io', 's\r', 'sa', "u'", 'av', 'os', 
                ' à', ' u', "l'", "'a", 'rs', 'pl', 'é ', '; ', 'ho', 'té', 'ét', 
                'fa', 'da', 'li', 'su', 't\r', 'ée', 'ré', 'dé', 'ec', 'nn', 'mm', 
                "'i", 'ca', 'uv', '\n\r', 'id', ' b', 'ni', 'bl']

    K = gen_key(symboles)

    dictionaire = gen_key(symboles)

    M = text[10500 : 13500]

    C = chiffrer(M, K, dictionaire)

    return (M, C)

M, C = test_prep()
