from http.server import BaseHTTPRequestHandler
from datetime import datetime
import requests
import json
import smtplib
from email.mime.text import MIMEText

base_url = 'https://leetcode-cn.com'

def getTodayRecord():
    try:
        response = requests.post(base_url + "/graphql", json={
            "query": "\n    query questionOfToday {\n  todayRecord {\n    date\n    userStatus\n    question {\n      questionId\n      frontendQuestionId: questionFrontendId\n      difficulty\n      title\n      titleCn: translatedTitle\n      titleSlug\n      paidOnly: isPaidOnly\n      freqBar\n      isFavor\n      acRate\n      status\n      solutionNum\n      hasVideoSolution\n      topicTags {\n        name\n        nameTranslated: translatedName\n        id\n      }\n      extra {\n        topCompanyTags {\n          imgUrl\n          slug\n          numSubscribed\n        }\n      }\n    }\n    lastSubmission {\n      id\n    }\n  }\n}\n    "
        })
        leetcodeTitle = json.loads(response.text).get('data').get('todayRecord')[0].get("question").get('titleCn')
        return leetcodeTitle
    except requests.exceptions.RequestException as e:
        raise SystemExit(e) 
 
class handler(BaseHTTPRequestHandler):
 
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        try:
            todayRecord = getTodayRecord()
            self.wfile.write(todayRecord.encode())
        except requests.exceptions.RequestException as e:
            self.wfile.write("failure".encode)        
        return
