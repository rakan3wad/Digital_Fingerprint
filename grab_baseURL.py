from urllib.parse import urlparse
def grab_base_URL(url):

    parsed_url = urlparse(url)

    if parsed_url.netloc == "salla.sa":
        path_parts = parsed_url.path.strip("/").split("/")
        # Check if the path has at least two parts
        if len(path_parts) >= 2:
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}/{path_parts[0]}"
        else:
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}/{path_parts[0]}"
    else:
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    return base_url

