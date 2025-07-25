import customtkinter as tk
import requests
import json
import sys
# from time import sleep





# typewriter effect
# def type(words: str):
#     for char in words:
#         sleep(0.015)
#         sys.stdout.write(char)
#         sys.stdout.flush()
#     print()
def type(words: str):
    print(words)



def scan_file(file_path, update_path_display, colors, index, log):

    url = "https://www.virustotal.com/vtapi/v2/file/scan"

    api = open("vt-api.txt", "r").read()

    # file_path = input(colorama.Fore.YELLOW + "Enter the path of the file >> ")
    params = { "apikey": api }

    try:
        file_to_upload = { "file": open(file_path, "rb") }

        response = requests.post(url, files=file_to_upload, params=params)
        file_url = f"https://www.virustotal.com/api/v3/files/{(response.json())["sha1"]}"

        headers = { "accept": "application.json", "x-apikey": api }
        log("\nAnalysing....\n", "yellow")

        response = requests.get(file_url, headers=headers)

        report = response.text
        report = json.loads(report)

        if "data" not in report:
            colors[index] = "unfound"
            log(f"\nError\n", "red")
            update_path_display()
            return

        name = (report["data"]["attributes"]).get("meaningful_name", "unable to fetch")
        hash = (report["data"]["attributes"])["sha256"]
        descp = (report["data"]["attributes"])["type_description"]
        size = (report["data"]["attributes"])["size"] * 10 ** -3
        result = (report["data"]["attributes"])["last_analysis_results"]

        log(f"\nName: {name}\n", "yellow")
        log(f"Size: {size}\n KB", "yellow")
        log(f"Description: {descp}\n", "yellow")
        log(f"SHA-256 Hash: {hash}\n", "yellow")

        malicious_count = 0

        for key, values in result.items():
            key = key
            verdict = values["category"]
            if verdict == "undetected":
                verdict = "undetected"
            
            elif verdict == "type-unsupported":
                verdict = "type-unsupported"
            
            elif verdict == "malicious":
                malicious_count += 1
                verdict = "malicious"
            
            log(f"{key}: {verdict}\n\n", "green" if verdict == "undetected" else "red")


        if malicious_count == 0:
            colors[index] = "clean"
            log("no antivirus found the given file malicious !!\n\n", "green")
        else:
            colors[index] = "malicious"
            log(f"{malicious_count} antivirus found the given file malicious !!\n\n", "red")

        print(f"Done! {index}")
        
    except:
        colors[index] = "unfound"
        print("file path invalid")
        log(f"\nfile path invalid\n", "red")

    update_path_display()
