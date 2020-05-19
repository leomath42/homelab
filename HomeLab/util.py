import random
_chr_inicio = 33
_chr_fim = 126
def generate_random_sequence(num):
    aux = ""
    for i in range(num):
        aux += chr(random.randint(_chr_inicio, _chr_fim))

    return aux