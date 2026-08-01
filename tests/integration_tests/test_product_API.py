async def test_get_products(client, admin_token):
    await client.post(
        "/categories/",
        json={"name": "name"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    await client.post(
        "/products/",
        json={"name": "product", "category_id": 1},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    await client.post(
        "/products/",
        json={"name": "product2", "category_id": 1},
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    response = await client.get(
        "/products/", headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 200
    assert response.json() == [
        {"name": "product", "category_id": 1, "id": 1},
        {"name": "product2", "category_id": 1, "id": 2},
    ]


async def test_get_product_by_id(client, admin_token):
    await client.post(
        "/categories/",
        json={"name": "name"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    await client.post(
        "/products/",
        json={"name": "product", "category_id": 1},
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    response = await client.get(
        "/products/1", headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 200
    assert response.json() == {"name": "product", "category_id": 1, "id": 1}


async def test_add_product(client, admin_token):
    await client.post(
        "/categories/",
        json={"name": "name"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    response = await client.post(
        "/products/",
        json={"name": "product", "category_id": 1},
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    assert response.status_code == 200
    assert response.json() == {"name": "product", "category_id": 1, "id": 1}


async def test_delete_product(client, admin_token):
    await client.post(
        "/categories/",
        json={"name": "name"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    await client.post(
        "/products/",
        json={"name": "product", "category_id": 1},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    response = await client.delete(
        "/products/1", headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 200
    assert response.json() == {"name": "product", "category_id": 1, "id": 1}


async def test_get_product_by_id_raises_404(client, admin_token):
    response = await client.get(
        "/products/999", headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 404


async def test_add_product_raises_404(client, admin_token):
    response = await client.post(
        "/products/",
        json={"name": "name", "category_id": 9999},
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    assert response.status_code == 404


async def test_delete_product_raises_404(client, admin_token):
    response = await client.delete(
        "/products/1", headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 404
