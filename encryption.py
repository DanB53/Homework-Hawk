
priv_seed = 5486416585555566
def make_definition(seed):
    import string
    charset = string.ascii_letters + string.digits + " " + string.punctuation 
    definition = []
    for i in charset:
        pos = charset.find(i)
        key = ""
        counter = -1
        for char in charset:
            counter += 1
            if char == i:
                pos = counter
                for j in range(5):
                    pos += seed
                    pos %= len(charset)

                    key = key + charset[pos]

                break
        definition.append(key)
    return definition



def encrypt(seed, text):
    import string
    charset = string.ascii_letters + string.digits + " " + string.punctuation 
    definition = make_definition(seed)
    output = ""
    for i in text:
        pos = charset.find(i)
        new_char = definition[pos]
        output = output + new_char
    return output

def decrypt(seed, text):
    import string
    charset = string.ascii_letters + string.digits + " " + string.punctuation 
    definition = make_definition(seed)
    counter = -1
    current_string = ""
    all_strings = []
    output=""
    for i in text:
        counter += 1
        if counter % 5 == 0 and counter != 0:

            all_strings.append(current_string)
            current_string = ""
            current_string = current_string + i
        else:
            current_string = current_string + i

    all_strings.append(current_string)
    positions = []
    for j in all_strings:
        counter = -1
        for k in definition:
            counter += 1
            if j == definition[counter]:
                positions.append(counter)
    for l in positions:
        output = output + charset[l]
    return output

# print(make_definition(priv_seed))
print(encrypt(priv_seed,"yo"))