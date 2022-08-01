def binary(n, s=''):
    r = int(n % 2)
    n = (n - r) / 2
    s = str(r) + s
    if n != 0:
        binary(n, s)
    else:
        for i in range(len(s), 6):
            s = "0" + s
        return s


def encode_bin(
        string="Y3Jvc3MgdGhpcyBhbmQgZGl2aXNpb24gc3VidHJhY3Rpb24gcG9pbnRlciBhbmFseXNpcyBncmFwaCBhbGdvcml0aG1zMDEy"):
    enc_bin_main_string = ''
    for i in string:
        if (i.isupper()):
            enc_bin_main_string += binary(ord(i) - 65)
        elif (i.isdigit()):
            enc_bin_main_string += binary(ord(i) + 4)
        elif i in ('+'):
            enc_bin_main_string += binary(ord(i) + 4)
        elif i in ('/'):
            enc_bin_main_string += binary(ord(i) + 4)
        else:
            enc_bin_main_string += binary(ord(i) - 71)
    print(enc_bin_main_string)
    return enc_bin_main_string


bin_enc_main = encode_bin()


def decimal(string):
    n = 7
    a = 0
    for i in string:
        a += int(i) * (2 ** n)
        n -= 1
    if a in list(range(0, 26)):
        a = chr(a + 65)
    else:
        a = chr(a + 71)
    return a


def decode():
    s = ''
    for i in range(0, len(bin_enc_main), 8):
        bin_enc = bin_enc_main[i:i + 8]
        s += decimal(bin_enc)
    return s


print(decode())
