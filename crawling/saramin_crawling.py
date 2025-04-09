import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0"
}

# 1페이지부터 60페이지까지 반복
for page in range(1, 61):
    url = f"https://www.saramin.co.kr/zf_user/jobs/public/list?page={page}&quick_apply=y&isAjaxRequest=y&page_count=100"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 공고 제목 추출 (사람인에서는 'a.str_tit' 안에 제목이 있음)
    titles = soup.select("a.str_tit")
    i = 0
    for title in titles:
        text = title.get_text(strip=True)
        if i % 2 == 0:
            print(text, end=" ")
        else:
            print(text)
        i += 1
