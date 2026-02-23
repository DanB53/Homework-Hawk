import requests
import json


def splitText(text):
    text = text.replace("\n", " ")
    text = text.replace("\t", " ")
    text = text.replace("\r", " ")
    splitTextInWords = text.split(" ")
    sectionedText = []
    counter = 0
    array = 0
    for word in range((len(splitTextInWords) // 3000) + 1):
        sectionedText.append([])
        counter += 1
    counter = -1
    string = ""
    for word in splitTextInWords:
        counter += 1
        if counter == 3000:
            string = string[:-1]
            sectionedText[array].append(string)
            array += 1
            string = ""
            counter = 0
        string = string + word + " "
    if string != "" and string != " ":
        sectionedText[array].append(string)
    else:
        sectionedText.pop()
    return sectionedText

def aiScan(student_id, assignment_id, text):
    if len(text.split()) < 50:
        return "Error", None
    url = "https://api.originality.ai/api/v1/scan/ai"
    headerKey = "Insert API Key Here"
    sendData = json.dumps({
        "content": text,
        "title": str(student_id) + "," + str(assignment_id),
        "aiModelVersion": "2",
        "storeScan": "\"false\""
    })
    headers = {
        "X-OAI-API-KEY": headerKey,
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    response = requests.request("POST", url, headers=headers, data=sendData)
    response = json.loads(response.text)
    return response["title"], response["score"]["ai"]


def plScan(student_id, assignment_id, text, minFlagPercentage):
    if len(text.split()) < 50:
        return "Error", None
    sectionedText = splitText(text)
    if len(sectionedText) == 1:
        url = "https://api.originality.ai/api/v1/scan/plag"
        headerKey = "API Key Here"
        sendData = json.dumps({
            "content": text,
            "title": str(student_id) + "," + str(assignment_id),
            "storeScan": "\"false\""
        })
        headers = {
            "X-OAI-API-KEY": headerKey,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        response = requests.request("POST", url, headers=headers, data=sendData)
        response = json.loads(response.text)
        return response["title"], response["total_text_score"]
    elif len(sectionedText) >= 2:
        for set in range(len(sectionedText)):
            url = "https://api.originality.ai/api/v1/scan/plag"
            headerKey = "i1fxjcv9p2wsumrdtq4keh837znly6ag"
            sendData = json.dumps({
                "content": text,
                "title": str(student_id) + "," + str(assignment_id),
                "storeScan": "\"false\""
            })
            headers = {
                "X-OAI-API-KEY": headerKey,
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            response = requests.request("POST", url, headers=headers, data=sendData)
            response = json.loads(response.text)
            if int((response[:-1]))/100 >= minFlagPercentage:
                return response["title"], response["total_text_score"]

def aiplScan(student_id, assignment_id, text):
    if len(text.split()) < 50:
        return "Error", None, None
    url = "https://api.originality.ai/api/v1/scan/ai-plag"
    headerKey = "i1fxjcv9p2wsumrdtq4keh837znly6ag"
    sendData = json.dumps({
        "content": text,
        "title": str(student_id) + "," + str(assignment_id),
        "aiModelVersion": "2",
        "storeScan": "\"false\""
    })
    # print(sendData)
    headers = {
        "X-OAI-API-KEY": headerKey,
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    response = requests.request("POST", url, headers=headers, data=sendData)
    response = json.loads(response.text)
    try:
        return response["title"], response["ai"]["score"]["ai"], response["plagiarism"]["total_text_score"]
    except:
        return "Error", None, None


def plManualUpload(user_id, text, minFlagPercentage):
    if len(text.split()) < 50:
        return "Error"
    minFlagPercentage = int(minFlagPercentage)/100
    sectionedText = splitText(text)
    if len(sectionedText) == 1:
        url = "https://api.originality.ai/api/v1/scan/plag"
        headerKey = "i1fxjcv9p2wsumrdtq4keh837znly6ag"
        sendData = json.dumps({
            "content": text,
            "title": str(user_id)+" Manual Upload",
            "storeScan": "\"false\""
        })
        headers = {
            "X-OAI-API-KEY": headerKey,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        response = requests.request("POST", url, headers=headers, data=sendData)
        response = json.loads(response.text)
        return response["title"], response["total_text_score"]
    elif len(sectionedText) >= 2:
        for set in range(len(sectionedText)):
            url = "https://api.originality.ai/api/v1/scan/plag"
            headerKey = "i1fxjcv9p2wsumrdtq4keh837znly6ag"
            sendData = json.dumps({
                "content": text,
                "title": str(user_id)+" Manual Upload",
                "storeScan": "\"false\""
            })
            headers = {
                "X-OAI-API-KEY": headerKey,
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            response = requests.request("POST", url, headers=headers, data=sendData)
            response = json.loads(response.text)
            if int((response[:-1]))/100 >= minFlagPercentage:
                return "Pl"
        return "Clear"

def aiManualUpload(user_id, text):
    if len(text.split()) < 50:
        return "Error"
    url = "https://api.originality.ai/api/v1/scan/ai"
    headerKey = "i1fxjcv9p2wsumrdtq4keh837znly6ag"
    sendData = json.dumps({
        "content": text,
        "title": str(user_id)+" Manual Upload",
        "aiModelVersion": "2",
        "storeScan": "\"false\""
    })
    headers = {
        "X-OAI-API-KEY": headerKey,
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    response = requests.request("POST", url, headers=headers, data=sendData)
    response = json.loads(response.text)
    return response["score"]["ai"]





def aiplManualUpload(user_id, text):
    if len(text.split()) < 50:
        return "Error", None
    url = "https://api.originality.ai/api/v1/scan/ai-plag"
    headerKey = "i1fxjcv9p2wsumrdtq4keh837znly6ag"
    sendData = json.dumps({
        "content": text,
        "title": str(user_id)+" Manual Upload",
        "aiModelVersion": "2",
        "storeScan": "\"false\""
    })
    headers = {
        "X-OAI-API-KEY": headerKey,
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    response = requests.request("POST", url, headers=headers, data=sendData)
    response = json.loads(response.text)
    try:
        return response["ai"]["score"]["ai"], response["plagiarism"]["total_text_score"]
    except:
        return "Error", None