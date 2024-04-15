#抓取PTT八卦版網頁原始碼(HTML)
import urllib.request as req
def getTime(url):
    request=req.Request(url, headers={
        "cookie":"over18=1",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    })
    with req.urlopen(request) as response:
        data=response.read().decode("utf-8")

    import bs4 #安裝Beautifulsoup, 指令:pip3 install beautifulsoup4
    root=bs4.BeautifulSoup(data, "html.parser") # 讓Beautifulsoup 協助我們解析 HTML格式文件

    meta_values = root.find_all("span", class_="article-meta-value")
    if meta_values:
        last_meta_value = meta_values[-1].text 
        # print(last_meta_value)
        return last_meta_value
    return None

def getData(url):
    #建立一個Request物件，附加 Request Headers 的資訊
    request=req.Request(url, headers={
        "cookie":"over18=1",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    })
    with req.urlopen(request) as response:
        data=response.read().decode("utf-8")

    #解析原始碼，取得每篇文章的標題
    import bs4 #安裝Beautifulsoup, 指令:pip3 install beautifulsoup4
    root=bs4.BeautifulSoup(data, "html.parser") # 讓Beautifulsoup 協助我們解析 HTML格式文件
    # titles=root.find_all("div", class_="title") #尋找 class="title" 的div 標籤

    # for title in titles:
    #     if title.a !=None: #如果標題包含 a 標籤(沒有被刪除) 印出來
    #         print(title.a.string)
    # 尋找所有包含標題和 nrec 的元素
    entries = root.find_all("div", class_="r-ent")
   
    for entry in entries:
        if entry.a !=None: 
            title_div = entry.find("div", class_="title")
            nrec_div = entry.find("div", class_="nrec")
            title_link = title_div.a if title_div else None
            article_link=title_div.find("a")

            if title_link:
                title_text = title_link.string
                article_href = "https://www.ptt.cc"+article_link['href']
                get_final_time = getTime(article_href)
                nrec_text = nrec_div.find("span").string if nrec_div and nrec_div.find("span") else "0"
                # print(f'{title_text},{nrec_text},{get_final_time}')
                file.write(f"{title_text},{nrec_text},{get_final_time}\n")                
        
    #抓取上一頁的連結        
    nextLink=root.find("a", string="‹ 上頁") #找到內文是 ‹ 上頁 的 a 標籤
    return nextLink["href"]
#主程序: 抓取多個頁面的標題
pageURL="https://www.ptt.cc/bbs/Lottery/index.html"
# pageURL=getData(pageURL)
# print(pageURL)
count=0
with open("article.csv", "w", encoding="utf-8-sig") as file:
    while count<3:
        pageURL="https://www.ptt.cc"+getData(pageURL)
        count+=1