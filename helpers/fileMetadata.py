import re
def file_metadata(filename, search_string):
    try:
        with open(filename, 'r') as file:
            content = file.read()
            length = len(content)
            alphanumeric_count = len(re.findall(r'[A-Za-z0-9]', content))
            occurrences = len(re.findall(search_string.lower(), content.lower()))

        return {
            'length of whole text': length,
            'amount of alphanumeric symbols': alphanumeric_count,
            'number of occurrences of that string': occurrences
        }
    except Exception as e:
        return {'error': str(e)}