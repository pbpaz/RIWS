file = open('riws\paz_categories\cats_buscalibre.txt', "r", encoding='utf-8')
out = open('riws\paz_categories\\buscalibre_unique_categories.txt', "w", encoding='utf-8')
count = 1
comillas = 0
content = file.read()
comillas = comillas + content.count("'")
# Find all matches inside single quotes
content = content.replace('\n', ' ')
matches = content.split("',")

# Print each match on a new line
for match in matches:
        cat = match.strip().strip(",'").replace('\n','')
        out.write(f"{cat}\n")
        count = count+1
print(count)
print(comillas)
