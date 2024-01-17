from flask import Flask, request, jsonify
from flask_cors import CORS
from bs4 import BeautifulSoup
import requests


app = Flask(__name__)
CORS(app)

@app.route('/search', methods=['POST'])
def post_data():
    data1 = request.get_json()

    name = data1['key1']
    name= name.replace(" ", "+")
    print(name)
    url = f"https://allnovelbook.com/search?q={name}"
    print(url)
    response = requests.get(url)
    doc = BeautifulSoup(response.text, "html.parser")
    div_element = doc.find('div', class_='special')
    print(div_element!=None)
    if div_element !=None:        
        NovelLink = div_element.find_all('a')
        data={
            "result":[]
        }
        for a in NovelLink:
            img = a.find('img')
            if img:
                items = {
                    "title": a['title'],
                    "url": a['href'],
                    "img":img['data-src']
                }
                data['result'].append(items)
        next = div_element.find('ul', class_="pagination")
        if next:
            numList = next.find_all("a", class_="page-link")
            num = [p.text for p in numList]
            val = len(num)
            i=0
            while i<val-1:
                if i==int(num[-2]):
                    break
                a = int(num[i])
                url =f"https://allnovelbook.com/search?q={name}&page={num[i]}"
                response = requests.get(url)
                doc = BeautifulSoup(response.text, "html.parser")
                div_element = doc.find('div', class_='special')
                if div_element:
                    NovelLink = div_element.find_all('a')
                    for a in NovelLink:
                        img = a.find('img')
                        if img:
                            items = {
                                "title": a['title'],
                                "url": a['href'],
                                "img":img['data-src']
                            }
                            data['result'].append(items)
                i+=1
            
    else:
        data ={
            "result":"No results for your search."
        }

    return jsonify(data)
@app.route('/detail', methods=['POST'])
def post_data1():
    data1 = request.get_json()
    url = data1['url']
    print(url)
    def getDetails(u):
        response = requests.get(u)
        doc = BeautifulSoup(response.text, "html.parser")
        div_element = doc.find('div',  class_ ="introduce")
        if div_element:
            print("yes")
            img = div_element.find('img')
            title = div_element.find('h2')
            author_div = div_element.find("div", class_="author")
            cat_div = div_element.find("div", class_="cat")
            status_div = div_element.find("div", class_="status")
            description_div = doc.find("div", class_="description")
            chapters_div = doc.find("div", class_="total-chapter")
            Description = description_div.find_all("p")
            Genres = cat_div.find_all('a')
            status = status_div.find('a')
            author = author_div.find('a')
            chapter = chapters_div.text
            gen = [p.text for p in Genres]
            des = [p.text for p in Description]
            data ={
                "title":title.text,
                "Genres":gen,
                "status":status.text,
                "author":author.text,
                "imgUrl": img['src'],
                "summary":des,
                "TotalChapters":chapter,
            }
            return data
  
    Det =getDetails(url)
    L=[]
    val=[]
    def getChapters(u):
        response = requests.get(u)
        doc = BeautifulSoup(response.text, "html.parser")
        div_element = doc.find('div',  id ="viewchapter")
        if div_element:
            NovelLink = div_element.find_all('a')
            print(div_element)
            data={
                "chap":[]
            }
            for a in NovelLink:
                title = a.get("title")
                if title is not None:
                    items = {
                        "chapter": a['title'],
                        "url": a['href'],
                    }
                    data['chap'].append(items)
                    L.append(items)
            next = div_element.find('ul', class_="pagination")
            if next:
                print("next page available")
                numList = next.find_all("a",class_="page-link")
                # print(numList)
                num = [p.text for p in numList]
                val.append(num[-2]) 
                i=0
                print(num[-2])
            #     while i<val-1:
            #         print(num,i)
            #         if i==int(num[-2]):
            #             break
            #         a = int(num[i])
            #         url =f"{u}?page={num[i]}"
            #         print(url)
            #         response = requests.get(url)
            #         doc = BeautifulSoup(response.text, "html.parser")
            #         div_element = doc.find('div',  id ="viewchapter")
            #         if div_element:
            #             print("yes")
            #             NovelLink = div_element.find_all('a')
            #             # print(div_element)
            #             for a in NovelLink:
            #                 title = a.get("title")
            #                 if title is not None:
            #                     items = {
            #                         "chapter": a['title'],
            #                         "url": a['href'],
            #                     }
            #                     data['chap'].append(items)
            #                     L.append(items)
            #         i+=1
            # return data
            return data

    chap = getChapters(url)
    data = {
        "Detail":Det,
        "chapters":chap, 
        "pagination":val[0],   
    }

    return jsonify(data)
@app.route('/chPage', methods=['POST'])
def post_data3():
    data1 = request.get_json()
    url = data1['url']
    print(url)
    data ={
        "chapters":[]
    }
    val=[]
    def getChapters(u):
        response = requests.get(url)
        doc = BeautifulSoup(response.text, "html.parser")
        div_element = doc.find('div',  id ="viewchapter")
        next = div_element.find('ul', class_="pagination")
        NovelLink = div_element.find_all('a')
        for a in NovelLink:
            title = a.get("title")
            if title is not None:
                print(a)  
                items = {
                    "chapter": a['title'],
                    "url": a['href'],
                }
                data['chapters'].append(items)
        return data

    chap = getChapters(url)
    data = {
        "chapters":chap, 
    }

    return jsonify(data)


@app.route('/chRead', methods=['POST'])
def post_data2():
    data1 = request.get_json()

    url = data1['url']

    
    response = requests.get(url)
    doc = BeautifulSoup(response.text, "html.parser")
    para = doc.find_all('p')
    title = doc.find('h2')
    text_content_list = [p.text for p in para]
    data = {
        "title":title.text,
        "paragraph" :text_content_list,
    }

    return jsonify(data)

@app.route('/api', methods=['GET'])
def get_data():
    # Process the data (you can replace this with your own logic)
    data = {'message': 'Hello, this is a GET request'}
    print(data)
    # Return a JSON response
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
    # app.run() for production
