async def test_add_category(client, admin_token):
    response = await client.post(
        "/categories/",
        json={"name": "name"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    assert response.status_code == 200
    assert response.json()["name"] == "name"
    assert "id" in response.json()


async def test_get_categories(client, admin_token):
    await client.post(
        "/categories/",
        json={"name": "name"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    response = await client.get(
        "/categories/", headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 200
    assert response.json() == [{"name": "name", "id": 1}]


async def test_get_category_by_id(client, admin_token):
    await client.post(
        "/categories/",
        json={"name": "name"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    response = await client.get(
        "/categories/1", headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 200
    assert response.json() == {"name": "name", "id": 1}


async def test_delete_category(client, admin_token):
    await client.post(
        "/categories/",
        json={"name": "name"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    response = await client.delete(
        "/categories/1", headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 200
    assert response.json() == {"name": "name", "id": 1}


async def test_get_products_by_category_id(client, admin_token):
    await client.post(
        "/categories/",
        json={"name": "name"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    await client.post(
        "/categories/",
        json={"name": "name2"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    await client.post(
        "/products/",
        json={"name": "name1", "category_id": 1, "price": 100},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    await client.post(
        "/products/",
        json={"name": "name2", "category_id": 1, "price": 100},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    await client.post(
        "/products/",
        json={"name": "name3", "category_id": 2, "price": 100},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    await client.post(
        "/products/",
        json={"name": "name4", "category_id": 1, "price": 100},
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    products = [
        {"name": "name1", "category_id": 1, "price": "100.00", "id": 1},
        {"name": "name2", "category_id": 1, "price": "100.00", "id": 2},
        {"name": "name3", "category_id": 2, "price": "100.00", "id": 3},
        {"name": "name4", "category_id": 1, "price": "100.00", "id": 4},
    ]

    response = await client.get(
        "categories/1/products", headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 200
    assert response.json()[0] == products[0]


async def test_delete_category_raises_not_found_error(client, admin_token):
    response = await client.delete(
        "/categories/9999", headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 404


async def test_get_category_by_id_raises_not_found_error(client, admin_token):
    response = await client.get(
        "/categories/999", headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 404
