def test_author_crud(client):
    response = client.post("/authors", json={"name": "Лев Толстой"})
    assert response.status_code == 201
    author_id = response.json()["id"]

    response = client.get(f"/authors/{author_id}")
    assert response.json()["name"] == "Лев Толстой"

    response = client.put(f"/authors/{author_id}", json={"name": "Л. Н. Толстой"})
    assert response.json()["name"] == "Л. Н. Толстой"

    response = client.delete(f"/authors/{author_id}")
    assert response.status_code == 204

    response = client.get(f"/authors/{author_id}")
    assert response.status_code == 404


def test_cannot_issue_book_twice(client):
    client.post("/authors", json={"name": "Лев Толстой"})
    client.post("/books", json={"title": "Война и мир", "year": 1869, "author_id": 1})
    client.post("/readers", json={"name": "Иван Петров", "email": "ivan@mail.ru"})
    client.post("/readers", json={"name": "Анна Смирнова", "email": "anna@mail.ru"})

    response = client.post("/books/1/issue/1")
    assert response.status_code == 200

    response = client.post("/books/1/issue/2")
    assert response.status_code == 400


def test_reader_max_three_books(client):
    client.post("/authors", json={"name": "Лев Толстой"})
    client.post("/readers", json={"name": "Иван Петров", "email": "ivan@mail.ru"})
    for i in range(4):
        client.post("/books", json={"title": f"Книга {i}", "year": 1869, "author_id": 1})

    assert client.post("/books/1/issue/1").status_code == 200
    assert client.post("/books/2/issue/1").status_code == 200
    assert client.post("/books/3/issue/1").status_code == 200
    assert client.post("/books/4/issue/1").status_code == 400
