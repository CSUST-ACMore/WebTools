
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
        sql = "SELECT * FROM user_profile WHERE id=" + str(submition[4])
        cursor.execute(sql)
        res = cursor.fetchall()
        mp['nickname'] = str(submition[11])
        mp['real_name'] = str(res[0][13])
        data.append(mp)
    jsn['data'] = data
    with open('signup/static/signup/data/teamData.json', 'w') as f:
        json.dump(jsn, f)


def fetch_submit(cursor, contest_id):
    jsn = {}
    data = []
    sql = "SELECT * FROM problem WHERE contest_id="+str(contest_id)+" ORDER BY id ASC;"
    cursor.execute(sql)
    min_pro_id = cursor.fetchall()[0][0]
    sql = "SELECT * FROM submission WHERE contest_id="+str(contest_id)+" ORDER BY create_time ASC;"
    cursor.execute(sql)
    results = cursor.fetchall()
    for submition in results:
        mp = {}
        mp['team_id'] = submition[4]
        mp['submit_id'] = str(submition[0])
        mp['problem_id'] = submition[2]-min_pro_id
        t = time.strptime(str(submition[3])[0:19], "%Y-%m-%d %H:%M:%S")
        lt = list(t)
        lt[3] = t.tm_hour+8
        t = tuple(lt)
        mp['submit_time'] = time.strftime("%Y-%m-%d %H:%M:%S", t)
        verdict = [0, 2, 2, 3, 5, 8, -1, -1, 4, 7, 4]
        mp["status"] = verdict[submition[6]]
        data.append(mp)
    jsn['data'] = data
    with open('signup/static/signup/data/submitData.json', 'w') as f:
        json.dump(jsn, f)


def fetch_data():
    db = psycopg2.connect(host='localhost', port='6666', dbname='onlinejudge', user='onlinejudge',
                          password='onlinejudge')
    cursor = db.cursor()
    sql = "SELECT * FROM contest ORDER BY create_time DESC;"
    cursor.execute(sql)
    results = cursor.fetchall()
    contest_id = results[0][0]
    fetch_team(cursor, contest_id)
    fetch_submit(cursor, contest_id)
    cursor.close()
    db.close()


if __name__ == "__main__":
    fetch_data()


