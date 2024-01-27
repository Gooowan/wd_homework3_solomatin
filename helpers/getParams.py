from urllib.parse import urlparse, parse_qs

def get_params_from_url(url):
    parsed_url = urlparse(url)
    params = parse_qs(parsed_url.query)
    return params


# params = get_params_from_url('/books?id=2')
# print(params)