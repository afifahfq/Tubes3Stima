from ReadFile import read_json

dictionary = read_json('dict.json')
def get_sinonim(string):
    if string in dictionary:
        return dictionary[string]['sinonim']
    else:
        return []