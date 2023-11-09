def upload_avatar(img,filename):
    import requests

    url = "https://api.imgbb.com/1/upload"
    params = {
        "key": "f4a5b3dc5e4d2513dfed80351c125295"
    }

    files = {
        "image": (filename, img)
    }

    response = requests.post(url, params=params, files=files)
    
    return response.json()['data']['url']