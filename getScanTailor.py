import requests, os, zipfile



#code taken from https://stackoverflow.com/a/39225272
def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)    

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)



file_id = "1kMWg4CIHcz6aoW36a7m2wuZlSpvh43KB"
destination = "scantailor.zip"
print("downloading...",end="")
download_file_from_google_drive(file_id, destination)
print("done\nunzipping...",end="")
with zipfile.ZipFile("scantailor.zip", "r") as zipRef:
    zipRef.extractall(".")
print("done")
