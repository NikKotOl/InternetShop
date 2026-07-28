async def test_get_products(client):
    await client.post("/categories/", json={"name": "name"})
    await client.post("/products/", json={"name": "product", "category_id": 1})
    await client.post("/products/", json={"name": "product2", "category_id": 1})

    response = await client.get("/products/")

    assert response.status_code == 200
    assert response.json() == [
        {"name": "product", "category_id": 1, "id": 1},
        {"name": "product2", "category_id": 1, "id": 2},
    ]


async def test_get_product_by_id(client):
    await client.post("/categories/", json={"name": "name"})
    await client.post("/products/", json={"name": "product", "category_id": 1})

    response = await client.get("/products/1")

    assert response.status_code == 200
    assert response.json() == {"name": "product", "category_id": 1, "id": 1}


async def test_add_product(client):
    await client.post("/categories/", json={"name": "name"})
    response = await client.post(
        "/products/", json={"name": "product", "category_id": 1}
    )

    assert response.status_code == 200
    assert response.json() == {"name": "product", "category_id": 1, "id": 1}


async def test_delete_product(client):
    await client.post("/categories/", json={"name": "name"})
    await client.post("/products/", json={"name": "product", "category_id": 1})
    response = await client.delete("/products/1")

    assert response.status_code == 200
    assert response.json() == {"name": "product", "category_id": 1, "id": 1}


async def test_get_product_by_id_raises_404(client):
    response = await client.get("/products/999")

    assert response.status_code == 404


async def test_add_product_raises_404(client):
    response = await client.post(
        "/products/", json={"name": "name", "category_id": 9999}
    )

    assert response.status_code == 404


async def test_delete_product_raises_404(client):
    response = await client.delete("/products/1")

    assert response.status_code == 404
