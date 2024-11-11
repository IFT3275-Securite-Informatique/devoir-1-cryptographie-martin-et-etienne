from collections import Counter
from crypt import cut_string_into_pairs, load_text_from_web
from itertools import permutations


url = "https://www.gutenberg.org/ebooks/13846.txt.utf-8"  # Example URL (replace with your desired URL)
text = load_text_from_web(url)
url = "https://www.gutenberg.org/ebooks/4650.txt.utf-8"  # Example URL (replace with your desired URL)
text = text + load_text_from_web(url)
url = "https://www.gutenberg.org/cache/epub/65578/pg65578.txt"  # Example URL (replace with your desired URL)
text = text + load_text_from_web(url)
url = "https://www.gutenberg.org/cache/epub/67102/pg67102.txt"  # Example URL (replace with your desired URL)
text = text + load_text_from_web(url)
url = "https://www.gutenberg.org/cache/epub/11494/pg11494.txt"  # Example URL (replace with your desired URL)
text = text + load_text_from_web(url)
url = "https://www.gutenberg.org/cache/epub/35878/pg35878.txt"  # Example URL (replace with your desired URL)
text = text + load_text_from_web(url)
url = "https://www.gutenberg.org/cache/epub/58501/pg58501.txt"  # Example URL (replace with your desired URL)
text = text + load_text_from_web(url)
url = "https://www.gutenberg.org/cache/epub/15871/pg15871.txt"  # Example URL (replace with your desired URL)
text = text + load_text_from_web(url)
url = "https://www.gutenberg.org/cache/epub/35390/pg35390.txt"  # Example URL (replace with your desired URL)
text = text + load_text_from_web(url)
url = "https://www.gutenberg.org/cache/epub/42300/pg42300.txt"  # Example URL (replace with your desired URL)
text = text + load_text_from_web(url)
url = "https://www.gutenberg.org/cache/epub/43315/pg43315.txt"  # Example URL (replace with your desired URL)
text = text + load_text_from_web(url)
# url = "https://www.gutenberg.org/cache/epub/42377/pg42377.txt"  # Example URL (replace with your desired URL)
# text = text + load_text_from_web(url)
# url = "https://www.gutenberg.org/cache/epub/43501/pg43501.txt"  # Example URL (replace with your desired URL)
# text = text + load_text_from_web(url)

corpus = text

caracteres = list(set(list(corpus)))
nb_caracteres = len(caracteres)
nb_bicaracteres = 256-nb_caracteres
bicaracteres = [item for item, _ in Counter(cut_string_into_pairs(corpus)).most_common(nb_bicaracteres)]
symboles = caracteres + bicaracteres
# symboles = ['b', 'j', '\r', 'J', '”', ')', 'Â', 'É', 'ê', '5', 't', '9', 'Y', '%', 'N', 'B', 'V', '\ufeff', 'Ê', '?', '’', 'i', ':', 's', 'C', 'â', 'ï', 'W', 'y', 'p', 'D', '—', '«', 'º', 'A', '3', 'n', '0', 'q', '4', 'e', 'T', 'È', '$', 'U', 'v', '»', 'l', 'P', 'X', 'Z', 'À', 'ç', 'u', '…', 'î', 'L', 'k', 'E', 'R', '2', '_', '8', 'é', 'O', 'Î', '‘', 'a', 'F', 'H', 'c', '[', '(', "'", 'è', 'I', '/', '!', ' ', '°', 'S', '•', '#', 'x', 'à', 'g', '*', 'Q', 'w', '1', 'û', '7', 'G', 'm', '™', 'K', 'z', '\n', 'o', 'ù', ',', 'r', ']', '.', 'M', 'Ç', '“', 'h', '-', 'f', 'ë', '6', ';', 'd', 'ô', 'e ', 's ', 't ', 'es', ' d', '\r\n', 'en', 'qu', ' l', 're', ' p', 'de', 'le', 'nt', 'on', ' c', ', ', ' e', 'ou', ' q', ' s', 'n ', 'ue', 'an', 'te', ' a', 'ai', 'se', 'it', 'me', 'is', 'oi', 'r ', 'er', ' m', 'ce', 'ne', 'et', 'in', 'ns', ' n', 'ur', 'i ', 'a ', 'eu', 'co', 'tr', 'la', 'ar', 'ie', 'ui', 'us', 'ut', 'il', ' t', 'pa', 'au', 'el', 'ti', 'st', 'un', 'em', 'ra', 'e,', 'so', 'or', 'l ', ' f', 'll', 'nd', ' j', 'si', 'ir', 'e\r', 'ss', 'u ', 'po', 'ro', 'ri', 'pr', 's,', 'ma', ' v', ' i', 'di', ' r', 'vo', 'pe', 'to', 'ch', '. ', 've', 'nc', 'om', ' o', 'je', 'no', 'rt', 'à ', 'lu', "'e", 'mo', 'ta', 'as', 'at', 'io', 's\r', 'sa', "u'", 'av', 'os', ' à', ' u', "l'", "'a", 'rs', 'pl', 'é ', '; ', 'ho', 'té', 'ét', 'fa', 'da', 'li', 'su', 't\r', 'ée', 'ré', 'dé', 'ec', 'nn', 'mm', "'i", 'ca', 'uv', '\n\r', 'id', ' b', 'ni', 'bl']


def get_symbols_frequencies():
    text = corpus
    frequencies = {}
    i = 0

    for symbole in symboles:
        frequencies[symbole] = 0

    while i < len(text):
        # Check pairs of characters
        if i + 1 < len(text):
            pair = text[i] + text[i + 1]
            if pair in frequencies:
                frequencies[pair] += 1

                i += 2  # Skip the two characters used
                continue

        # Check single character
        if text[i] in frequencies:
            frequencies[text[i]] += 1
        i += 1

    nb_total = sum(frequencies.values())

    for symbol in frequencies:
        frequencies[symbol] /= nb_total

    return dict(sorted(frequencies.items(), key=lambda item: item[1], reverse=True))

from collections import Counter



def get_pairs_frequencies():
    text = corpus

    char_list = list(text)

    frequencies = {pair : 0 for pair in permutations(symboles, 2)}

    for i in range(len(char_list)):
        pairs = []

        if i + 1 < len(char_list):
            pairs.append((char_list[i], char_list[i+1]))

            if i + 2 < len(char_list):
                pairs.append((char_list[i], char_list[i+1] + char_list[i+2]))
                pairs.append((char_list[i] + char_list[i+1],  char_list[i+2]))

                if i + 3 < len(char_list):
                    pairs.append((char_list[i] + char_list[i+1], char_list[i+2] + char_list[i+3]))

        for pair in pairs:
            if pair in frequencies:
                frequencies[pair] += 1
    
    nb_pairs = sum(frequencies.values())

    for pair in frequencies:
        frequencies[pair] /= nb_pairs

    return dict(sorted(frequencies.items(), key=lambda item: item[1], reverse=True))