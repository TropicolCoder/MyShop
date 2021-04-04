html = '''<tr class="row{% cycle "1" "2" %}">'''
html = html.strip()
html = html.split('\n')

striped_html = []

for snip in html:
    new = snip.strip()
    striped_html.append(new)

html = '\n'.join(striped_html)
html = html.split('\n<')

new_html = []

for code in html:
    code = code.replace('"', "'")
    jinja = '{%'
    source = 'src='
    href = 'href='
    http = 'http'
    if source in code:
        no = code.find(source)
        no2 = code.find("'", no + 5)
        no = no + 4
        if code.find(http) == no + 1 or code.find(jinja) == no + 1:
            new_code = code
            new_html.append(new_code)
            continue

    elif href in code:
        no = code.find(href)
        no2 = code.find("'", no + 6)
        no = no + 5
        if code.find(http) == no + 1 or code.find(jinja) == no + 1:
            new_code = code
            new_html.append(new_code)
            continue
    else:
        new_code = code
        new_html.append(new_code)
        continue

    link = code[no:no2 + 1]

    new_code = '{0}"%s static {1} %s"{2}'.format(code[:no], link, code[no2 + 1:]) % ('{%', '%}')
    new_html.append(new_code)

new_html = '\n<'.join(new_html)
print('Your finished code:\n' + new_html)
