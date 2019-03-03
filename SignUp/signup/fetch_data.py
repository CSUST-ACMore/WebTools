
import json, psycopg2, time


def fetch_team(cursor, contest_id):
    jsn = {}
    data = []
    sql = "SELECT * FROM submission WHERE contest_id="+str(contest_id)+" ORDER BY create_time ASC;"
    cursor.execute(sql)
    results = cursor.fetchall()
    for submition in results:
        mp = {}
        mp['team_id'] = submition[4]
        sql = "SELECT * FROM user_profile WHERE user_id=" + str(submition[4])
        cursor.execute(sql)
        res = cursor.fetchall()
        mp['nickname'] = str(submition[11])
        mp['real_name'] = str(res[0][13])
        data.append(mp)
    jsn['data'] = data
    with open('static/signup/data/teamData.json', 'w') as f:
        json.dump(jsn, f)


def fetch_submit(cursor, contest_id):
    jsn = {}
    data = []
    sql = "SELECT * FROM problem WHERE contest_id="+str(contest_id)+" AND visible=true ORDER BY id ASC;"
    cursor.execute(sql)
    results = cursor.fetchall()
    pro_mp = {}
    for pro in results:
        pro_mp[pro[0]] = pro[26]
    pro_num = pro_mp.__len__()
    sql = "SELECT * FROM submission WHERE contest_id="+str(contest_id)+" ORDER BY create_time ASC;"
    cursor.execute(sql)
    results = cursor.fetchall()
    for submition in results:
        if submition[2] in pro_mp:
            mp = {}
            mp['team_id'] = submition[4]
            mp['submit_id'] = str(submition[0])
            mp['problem_id'] = ord(pro_mp[submition[2]])-65
            t = time.strptime(str(submition[3])[0:19], "%Y-%m-%d %H:%M:%S")
            mp['submit_time'] = time.strftime("%Y-%m-%d %H:%M:%S", t)
            verdict = [0, 2, 2, 3, 5, 8, -1, -1, 4, 7, 4]
            mp["status"] = verdict[submition[6]]
            data.append(mp)
    jsn['data'] = data
    with open('static/signup/data/submitData.json', 'w') as f:
        json.dump(jsn, f)
    return pro_num


def fetch_data(contest_id):
    db = psycopg2.connect(host='172.17.0.1', port='6666', dbname='onlinejudge', user='onlinejudge',
                          password='onlinejudge')
    cursor = db.cursor()
    sql = "SELECT * FROM contest WHERE id="+str(contest_id)+";"
    cursor.execute(sql)
    results = cursor.fetchall()
    start_time = results[0][6]
    fetch_team(cursor, contest_id)
    pro_num = fetch_submit(cursor, contest_id)
    cursor.close()
    db.close()
    mp = {'start_time': start_time, 'pro_num': pro_num}
    return mp


if __name__ == "__main__":
    fetch_data(1)


