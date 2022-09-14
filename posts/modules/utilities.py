def slugear(title):
    slug=''
    for char in title:
        if char not in "!'@#$'%^&8()_+=[]:/\|`~<>?'¿;":
            slug += char
        else:
            slug += ''
    return slug.replace(' ','-').lower()
            