from selenium import webdriver
from selenium.webdriver.common.by import By
from flask import Flask, render_template, request,jsonify,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from selenium.webdriver.chrome.options import Options

import json
import time


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///scraped_data.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

def get_url(url):
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    return driver

def get_info(driver):
    poster=driver.find_element(By.XPATH,'//*[@class="poster"]/span/img')
    poster_src=poster.get_attribute("src")
    title=driver.find_element(By.XPATH,'//*[@class="info"]/h1')
    title_text=title.text
    year=driver.find_element(By.XPATH,'//*[@class="meta"]/div[3]/span[2]')
    year_text=year.text
    info_dic={"poster":poster_src,"title":title_text,"year":year_text}
    return info_dic
def get_iframes_src(driver):
    iframes=[]
    servers=driver.find_elements(By.XPATH,'//*[@id="servers"]/div')
    for i in range(1,len(servers)):
        print(servers[i].text)
        servers[i].click()
        servers=driver.find_elements(By.XPATH,'//*[@id="servers"]/div')
        time.sleep(3)
        iframe_element = driver.find_element(By.XPATH,'//*[@id="iframe"]')
        iframe_src = iframe_element.get_attribute("src")
        iframes.append(iframe_src)
    return iframes
def get_episodes_len(driver):
    episodes=driver.find_elements(By.XPATH,'//*[@class="episode"]')
    episodes_number=len(episodes)-1
    return episodes_number
def get_season_episodes_len(driver):
    drop_down=driver.find_element(By.ID,"seasons")
    list_items=drop_down.find_elements(By.XPATH,"//ul[@class='dropdown-menu']/li")

    final_len_list=[]
    for i in range(1,len(list_items)):
        item=list_items[i]
        drop_down.click()
        item.click()
        time.sleep(2)
        episodes_number=get_episodes_len(driver)
        final_len_list.append(episodes_number)

    return final_len_list
def modify_link(base_link, new_s_value, new_e_value):
    parts = base_link.split('&')
    s_part = next((part for part in parts if part.startswith('s=')), None)
    e_part = next((part for part in parts if part.startswith('e=')), None)
    if s_part is not None:
        new_s_part = f's={new_s_value}'
        base_link = base_link.replace(s_part, new_s_part)
    if e_part is not None:
        new_e_part = f'e={new_e_value}'
        base_link = base_link.replace(e_part, new_e_part)
    return base_link

def get_data(url):
    list=[]
    driver=get_url(url)
    iframes=get_iframes_src(driver=driver)
    info=get_info(driver=driver)
    episods=get_season_episodes_len(driver=driver)
    for s in range(len(episods)):
        dic={}
        dic['Season']=s+1
        for e in range(episods[s]):
            dic[f'Episode{e+1}']=[modify_link(iframes[i],s+1,e+1) for i in range(3)]
        list.append(dic)
    
    dic={'info':info,'Episodes':list} 
    driver.quit()
    print('finished')
    return dic

class ScrapedData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    poster = db.Column(db.String)
    title = db.Column(db.String)
    year = db.Column(db.String)
    episodes = db.Column(db.String)

@app.route('/', methods=['GET'])
def index():
    scraped_data = ScrapedData.query.all()

    serialized_data = []
    for entry in scraped_data:
        serialized_entry = {
            'id': entry.id,
            'poster': entry.poster,
            'title': entry.title,
            'year': entry.year,
            'episodes': [{
                              "Season": season_data["Season"],
                              "Episodes": [{
                                  "Episode": int(key.split("Episode")[1]),
                                  "URLs": urls
                              } for key, urls in season_data.items() if key.startswith("Episode")]
                          } for season_data in json.loads(entry.episodes)],

            'delete_url': url_for('delete', entry_id=entry.id)  

        }

        serialized_data.append(serialized_entry)

    return render_template('index.html', scraped_data=serialized_data)

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        url = request.form.get('url')
        data = get_data(url)

        new_entry = ScrapedData(
            poster=data['info']['poster'],
            title=data['info']['title'],
            year=data['info']['year'],
            episodes=json.dumps(data['Episodes'])
        )
        db.session.add(new_entry)
        db.session.commit()

        return jsonify({"message": "Data successfully stored."})

    return redirect('/')
@app.route('/delete/<int:entry_id>', methods=['POST'])
def delete(entry_id):
    entry = ScrapedData.query.get_or_404(entry_id)
    db.session.delete(entry)
    db.session.commit()
    return redirect('/')
if __name__ == '__main__':
    app.run(debug=True)
    






