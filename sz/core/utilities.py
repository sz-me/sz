import re

def words(text): return re.findall(ur'[а-яА-Яa-zA-z]+', text.lower()) 