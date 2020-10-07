# __Time__ : 2020/10/7 下午10:45
# __Author__ : '__YDongY__'

import requests
import pprint


def get_books():
    resp = requests.get("http://127.0.0.1:8000/books/")
    pprint.pprint(resp.json())


def get_book(bid):
    resp = requests.get(f"http://127.0.0.1:8000/books/{bid}/")
    pprint.pprint(resp.json())


def post_books():
    dic = {
        "title": "三国演义",
        "pub_date": "1990-02-03"
    }

    resp = requests.post("http://127.0.0.1:8000/books/", json=dic)
    pprint.pprint(resp.json())


def put_book(bid):
    dic = {
        "title": "三国演义（第二版）",
        "pub_date": "1990-02-03"
    }
    resp = requests.put(f"http://127.0.0.1:8000/books/{bid}/", json=dic)
    pprint.pprint(resp.json())


def delete_book(bid):
    resp = requests.delete(f"http://127.0.0.1:8000/books/{bid}/")
    pprint.pprint(resp)


if __name__ == '__main__':
    get_books()
    print("*" * 50)
    get_book(2)
    print("*" * 50)
    post_books()
    print("*" * 50)
    put_book(9)
    print("*" * 50)
    delete_book(11)
