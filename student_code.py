from frequencies import get_symbols_frequencies, get_pairs_frequencies

def load_french_words(file_path):
    # Load French words into a set
    with open(file_path, 'r', encoding='utf-8') as f:
        french_words = {line.strip().lower() for line in f}
    return french_words

def get_french_distance(text, french_words_set):
    words = text.split()
    words = [item.replace('\n', '').replace('\r', '') for item in words]
    # Count how many words are in the French words set
    french_count = sum(1 for word in words if word.lower() in french_words_set)
    
    total_words = len(words)
    if total_words == 0:
        return 0  # Avoid division by zero
    
    return (french_count / total_words) * 100

french_words_set = load_french_words('mots.txt')

symbols_frequencies = get_symbols_frequencies()
pairs_frequencies = get_pairs_frequencies()

def replace_bytes_by_symbols(bytes_list, bytes_frequencies, symbols_frequencies):
    pairs_frequencies_copy = list(pairs_frequencies.keys())
    for i in range(len(bytes_frequencies)):
        current_byte = bytes_frequencies[i]
        prev_symbol = bytes_list[bytes_list.index(current_byte) - 1]
        if len(prev_symbol) == 8:
            corresp_symbol = symbols_frequencies[i]
            bytes_list = [corresp_symbol if byte == current_byte else byte for byte in bytes_list]
        else:
            freq_pairs = [symbols for symbols in pairs_frequencies_copy if symbols[0] == prev_symbol]
            symbol = freq_pairs[0][1]
            bytes_list = [symbol if elem == current_byte else elem for elem in bytes_list]
            pairs_frequencies_copy.remove(freq_pairs[0])

    return "".join(bytes_list)

def decrypt(C):
    global symbols_frequencies
    global french_words_set

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

    # Trier les fréquences
    bytes_frequencies = dict(sorted(bytes_frequencies.items(), key=lambda item: (-item[1], byte_list.index(item[0]))))

    # Transformer le dictionnaire de fréquence des bytes en liste
    bytes_frequencies = list(bytes_frequencies.keys())
    symbols_frequencies = list(symbols_frequencies.keys())
    
    # Phase de déchiffrement
    french_distance = 0
    i = 0
    while french_distance < 15:
        max_french = 0
        max_perm = 0
        for j in range(-5, 6):
            if i + j < 0 or i + j >= len(bytes_frequencies):
                continue
            bf_copy = bytes_frequencies.copy()
            bf_copy[i], bf_copy[i + j] = bf_copy[i + j], bf_copy[i]
            decrypted_message = replace_bytes_by_symbols(byte_list.copy(), bf_copy, symbols_frequencies.copy())
            actual_french_distance = get_french_distance(decrypted_message, french_words_set)
            if actual_french_distance > max_french:
                max_french = actual_french_distance
                max_perm = j
        print(max_french)
        french_distance = max_french
        bytes_frequencies[i], bytes_frequencies[i + max_perm] = bytes_frequencies[i + max_perm], bytes_frequencies[i]
        i = (i + 1) % len(bytes_frequencies) 

    M = replace_bytes_by_symbols(byte_list, bytes_frequencies, symbols_frequencies)

    return M