import re

def capitalize_words(string, delimiters=[" "]):
  regex = "|".join(delimiters)
  splitted = re.split(regex, string)
  return " ".join([word.capitalize() for word in splitted])