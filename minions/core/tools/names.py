import re
from string import capwords
from names_translator import Transliterator

TRANSLITERATOR = Transliterator()


def title(s):
    chunks = s.split()
    chunks = map(lambda x: capwords(x, "-"), chunks)
    return " ".join(chunks)


def parse_fullname(person_name):
    # Extra care for initials (especialy those without space)
    person_name = re.sub("\s+", " ",
                         person_name.replace(".", ". ").replace('\xa0', " "))

    chunks = person_name.strip().split(" ")

    last_name = ""
    first_name = ""
    patronymic = ""
    dob = ""

    numeric_chunks = list(
        filter(lambda x: re.search("\d+\.?", x), chunks)
    )

    chunks = list(
        filter(lambda x: re.search("\d+\.?", x) is None, chunks)
    )

    if len(chunks) == 2:
        last_name = title(chunks[0])
        first_name = title(chunks[1])
    elif len(chunks) > 2:
        last_name = title(" ".join(chunks[:-2]))
        first_name = title(chunks[-2])
        patronymic = title(chunks[-1])

    if numeric_chunks:
        dob = "".join(numeric_chunks)

    return last_name, first_name, patronymic, dob
