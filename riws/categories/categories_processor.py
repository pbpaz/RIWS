path = 'categories.txt'

file = open(path, 'r', encoding='utf-8')
content = [linea.strip() for linea in file.readlines()]

unique_categories = list(set(content))

result = open('paz_unique_categories.txt', 'w', encoding='utf-8')
for line in unique_categories:
    result.write(line + '\n')
