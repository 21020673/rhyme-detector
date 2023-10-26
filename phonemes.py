# Import the g2p_en module
from g2p_en import G2p
g2p = G2p()

import re
from syllabifier import syllabifyARPA

# Hyphenate a word based on its phonemes
def syllabify(pronunciation):
    syllabified = []
    try:
        for syllable in syllabifyARPA(pronunciation):
            syllabified.append(syllable.split(" "))
    except ValueError:
        syllabified.append(pronunciation)
    return syllabified

# Get the unstressed pronounciation of a word
def get_unstressed(word):
    phonemes = g2p(word)
    unstressed = []
    for phoneme in phonemes:
        # Remove stress markers
        unstressed.append(re.sub(r"\d+", "", phoneme))
    return unstressed

# Get the phonemes for a text
def get_phonemes(text):
    out = []
    for line in text:
        line = re.sub(r"[,?!.]", "", line)
        line_out = []
        for word in line.split(" "):
            # Seperate the syllables with hyphens
            syllables = syllabify(get_unstressed(word))
            line_out.append(syllables)
        out.append(line_out)
    return out

# Print the phonemes for a text to a file
def print_phonemes(text, output_file):
    f = open(output_file, "w")
    for line in text:
        f.write(line)
        line = re.sub(r"[,?!.]", "", line)
        for word in line.split(" "):
            # Seperate the syllables with hyphens
            syllables = syllabify(get_unstressed(word))
            for syllable in syllables:
                for phoneme in syllable:
                    f.write(phoneme)
                if syllable != syllables[-1]:
                    f.write("-")
            if word != line.split(" ")[-1]:
                f.write(" ")
        f.write("\n")
    f.close()

class Token:
    def __init__(self, word):
        self.word = word
        self.syllables = []

    class Syllable:
        def __init__(self, phonemes):
            self.phonemes = phonemes
            self.group = 0

    def add_syllables(self, syllables):
        for syllable in syllables:
            self.syllables.append(Token.Syllable(syllable))

    
def tokenize(lines):
    tokens = []
    for line in lines:
        token_line = []
        line = re.sub(r"[,?!.]", "", line)
        for word in line.split(" "):
            # Seperate the syllables with hyphens
            token_word = Token(word)
            token_word.add_syllables(syllabify(get_unstressed(word)))
            token_line.append(token_word)
        tokens.append(token_line)
    return tokens