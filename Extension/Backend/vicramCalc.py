import requests
import time  # Don't forget to import the time module

def vicramcalc1(role, url):
    port = "8081"
    server = "http://localhost:"
    vicram= "/visual-complexity/"
    url = url
    width = 1920
    height = 1800
    agent = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:27.0) Gecko/20100101 Firefox/27.0"
    explainRoles = False

    # In case of fails, limit retries to 3
    sleep_time = 2
    num_retries = 3

    for retry in range(0, num_retries):
        req = requests.post(server + port+vicram, json={
            "url": url,
            "width": width,
            "height": height,
            "agent": agent,
            "explainRoles": explainRoles
        })

        if req.status_code == 200:
            #print("Success")
            #print(req.json())  # Use req.json() to properly deserialize the JSON response
            if 'result' in req.json():
                vicram_score = req.json()['result'].get('vicram')
            return vicram_score
            break
        else:
            ##print(f"Request failed (Attempt {retry + 1}/{num_retries})")
            if retry < num_retries - 1:
                #print(f"Retrying in {sleep_time} seconds...")
                time.sleep(sleep_time)
            else:
                print("Max retries reached. Exiting.")


#role = "example_role"
#url = "https://www.youtube.com/"
#vicrascore=vicramcalc1(role, url)
#print("your score :",vicrascore)