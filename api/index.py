from http.server import BaseHTTPRequestHandler
import requests
import re
import json
from requests_toolbelt import MultipartEncoder

session = requests.Session()
user_agent = r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
base_url = 'https://leetcode-cn.com'

# def login(username, pwd):
#     login_url = base_url + '/accounts/login/'
#     cookies = session.get(login_url).cookies
#     for cookie in cookies:
#         if cookie.name == 'csrftoken':
#             csrftoken = cookie.value
    
#     params_data = {
#         'csrfmiddlewaretoken': csrftoken,
#         'login': username,
#         'password':pwd,
#         'next': '/problems'
#     }
#     headers = {'User-Agent': user_agent, 'Connection': 'keep-alive', 'Referer': login_url, "origin": base_url}
#     m = MultipartEncoder(params_data)   

#     headers['Content-Type'] = m.content_type
#     session.post(login_url, headers = headers, data = m, timeout = 10, allow_redirects = False)
#     is_login = session.cookies.get('LEETCODE_SESSION') != None
#     return is_login

def login():
    login_url = 'https://leetcode.cn/accounts/login/'
    print('Login to leetcode...')

    session = requests.Session()

    response = session.request('GET', login_url)
    if response.status_code != 200 or not session.cookies['csrftoken']:
        print('Error in get login page')
        print(response.status_code)
        print(response.text)
        return
    return session.cookies['csrftoken']

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
 
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path
        path = path.replace("'", '"')
        user_reg = re.compile(r'user="(.*?)"')
        pwd_reg = re.compile(r'pwd="(.*?)"')
        user = user_reg.findall(path)[0]
        pwd = pwd_reg.findall(path)[0]
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

        # login section
        token = login(user, pwd)
        try:
            todayRecordName, difficulty, acRate = getTodayRecord()
            displaystr = "Token: " + token + "\nProblem: " + todayRecordName + "\nDifficulty: " + difficulty + "\nAccept Rate: " + str(acRate)
            self.wfile.write(displaystr.encode())
        except requests.exceptions.RequestException as e:
            self.wfile.write("failure".encode())        
        return
