from prior import p4
from prior import read4

# ---
lal = [
    "Tooth decay",
    "Angular cheilitis",
    "Bad breath",
    "Leukoplakia",
    "Periodontal disease",
    "Tonsil stones",
]
# ---

all, allen = p4.start_test(links=lal)

read4.work_test(all, allen)

# ---
x = 'https://books.google.ca/books?id=JaOoXdSlT9sC&pg=PA11'
# ---
# prased = url_parser(x)
# print(prased)
# ---
#
# if 'books.google' in x: x = re.sub(r'google\.\w+/', 'google.com/', x)
# ---
