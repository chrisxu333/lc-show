from http.server import BaseHTTPRequestHandler
import requests
import re
import json
from requests_toolbelt import MultipartEncoder

session = requests.Session()
user_agent = r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
base_url = 'https://leetcode-cn.com'

def getTodayRecord():
    try:
        response = requests.post(base_url + "/graphql", json={
            "query": "\n    query questionOfToday {\n  todayRecord {\n    date\n    userStatus\n    question {\n      questionId\n      frontendQuestionId: questionFrontendId\n      difficulty\n      title\n      titleCn: translatedTitle\n      titleSlug\n      paidOnly: isPaidOnly\n      freqBar\n      isFavor\n      acRate\n      status\n      solutionNum\n      hasVideoSolution\n      topicTags {\n        name\n        nameTranslated: translatedName\n        id\n      }\n      extra {\n        topCompanyTags {\n          imgUrl\n          slug\n          numSubscribed\n        }\n      }\n    }\n    lastSubmission {\n      id\n    }\n  }\n}\n    "
        })
        data = json.loads(response.text).get('data')
        title = data.get('todayRecord')[0].get("question").get('title')
        difficulty = data.get('todayRecord')[0].get("question").get('difficulty')
        acRate = data.get('todayRecord')[0].get("question").get('acRate')
        return title, difficulty, acRate
    except requests.exceptions.RequestException as e:
        raise SystemExit(e) 

def getPersonalProgress(username):
    response = requests.post(base_url + "/graphql", json={
        "query":"\n    query userQuestionProgress($userSlug: String!) {\n  userProfileUserQuestionProgress(userSlug: $userSlug) {\n    numAcceptedQuestions {\n      difficulty\n      count\n    }\n    numFailedQuestions {\n      difficulty\n      count\n    }\n    numUntouchedQuestions {\n      difficulty\n      count\n    }\n  }\n}\n    ","variables":{"userSlug":username}
    })
    data = json.loads(response.text).get('data')
    easy_count = data.get('userProfileUserQuestionProgress').get("numAcceptedQuestions")[0].get('count')
    return easy_count
 
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path
        path = path.replace("'", '"')
        user_reg = re.compile(r'user="(.*?)"')
        user = user_reg.findall(path)[0]
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

        try:
            # todayRecordName, difficulty, acRate = getTodayRecord()
            # displaystr = "Problem: " + todayRecordName + "\nDifficulty: " + difficulty + "\nAccept Rate: " + str(acRate)
            displaystr = getPersonalProgress(user)
            self.wfile.write(displaystr.encode())
        except requests.exceptions.RequestException as e:
            self.wfile.write("failure".encode())        
        return
