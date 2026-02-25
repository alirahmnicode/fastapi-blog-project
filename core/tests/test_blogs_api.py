# retrieve tests

def test_blogs_list_api_response_200(anon_client):
    response = anon_client.get("/blogs/all")
    assert response.status_code == 200


def test_user_blogs_list_api_response_200(auth_client):
    response = auth_client.get("/blogs")
    assert response.status_code == 200


def test_user_blogs_list_unauthorized_api_response_401(anon_client):
    response = anon_client.get("/blogs")
    assert response.status_code == 401


def test_blog_detail_api_response_200(auth_client, random_blog):
    response = auth_client.get(f"/blogs/{random_blog.id}")
    assert response.status_code == 200


# create tests

def test_blog_create_api_response_201(auth_client, fake_blog_data):
    print(fake_blog_data)
    response = auth_client.post("/blogs", json=fake_blog_data)
    assert response.status_code == 201


def test_blog_create_invalid_data_response_422(auth_client):
    res = auth_client.post(
        "/blogs", json={"title": 123, "body": None})
    assert res.status_code == 422


def test_blog_create_unauthorized_response_401(anon_client, fake_blog_data):
    response = anon_client.post("/blogs", json=fake_blog_data)
    assert response.status_code == 401


# update tests

def test_blog_update_api_response_200(auth_client, random_blog):
    data = {
        "title": "updated blog",
        "slug": "slug",
        "content": "content of the new blog",
        "excerpt": "excerpt of the new blog",
        "image_url": f"https://picsum.photos/seed/800/400",
        "is_published": True,
        "published_at": "2024-06-01T12:00:00Z",
        "created_at": "2024-06-01T12:00:00Z",
        "updated_at": "2024-06-01T12:00:00Z",
        "tags": [],
    }
    response = auth_client.put(f"/blogs/{random_blog.id}", json=data)
    assert response.status_code == 200
    assert response.json()["title"] == "updated blog"


def test_update_blog_not_found_response_404(auth_client, fake_blog_data):
    response = auth_client.put(f"/blogs/999999", json=fake_blog_data)
    assert response.status_code == 404


def test_update_blog_invalid_data_response_422(auth_client):
    res = auth_client.put(
        "/blogs/1", json={"title": 123, "body": None})
    assert res.status_code == 422


def test_update_blog_unauthorized_response_401(anon_client, fake_blog_data):
    response = anon_client.put(f"/blogs/1", json=fake_blog_data)
    assert response.status_code == 401


# delete tests

def test_delete_blog_response(auth_client, random_blog):
    response = auth_client.delete(f"/blogs/{random_blog.id}")
    assert response.status_code == 204


def test_delete_blog_not_found_response_404(auth_client):
    response = auth_client.delete(f"/blogs/999999")
    assert response.status_code == 404


def test_delete_blog_unauthorized_response_401(anon_client):
    response = anon_client.delete(f"/blogs/1")
    assert response.status_code == 401
