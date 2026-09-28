"""Seed de demonstração para o WMS Operacional.

Este script cria dados fictícios necessários para a aplicação funcionar
em modo de demonstração, incluindo produtos, EANs, SKUs, contas, usuários
e pedidos.
"""

import uuid
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.models import Product, EAN, SKU, Account, User, Order
from app.database import Base, engine, SessionLocal


def create_demo_data():
    """Cria todos os dados de demonstração necessários."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Criar contas
        accounts = [
            Account(id=1, name="Conta Principal", type="asset"),
            Account(id=2, name="Conta de Estoque", type="asset"),
            Account(id=3, name="Conta de Vendas", type="revenue"),
        ]
        for acc in accounts:
            db.add(acc)
        db.commit()

        # Criar usuários
        users = [
            User(
                id=1,
                username="admin",
                email="admin@wms.com",
                full_name="Administrador WMS",
                is_active=True,
                is_superuser=True,
            ),
            User(
                id=2,
                username="operador",
                email="operador@wms.com",
                full_name="Operador de Estoque",
                is_active=True,
                is_superuser=False,
            ),
            User(
                id=3,
                username="gerente",
                email="gerente@wms.com",
                full_name="Gerente de Logística",
                is_active=True,
                is_superuser=False,
            ),
        ]
        for user in users:
            db.add(user)
        db.commit()

        # Criar produtos com EANs e SKUs
        products_data = [
            {
                "name": "Camiseta Algodão P",
                "sku": "CAM-P001",
                "ean": "7891234000001",
                "price": 29.90,
                "quantity": 150,
            },
            {
                "name": "Camiseta Algodão M",
                "sku": "CAM-P002",
                "ean": "7891234000002",
                "price": 29.90,
                "quantity": 120,
            },
            {
                "name": "Camiseta Algodão G",
                "sku": "CAM-P003",
                "ean": "7891234000003",
                "price": 29.90,
                "quantity": 100,
            },
            {
                "name": "Calça Jeans Masculina",
                "sku": "CAL-M001",
                "ean": "7891234000010",
                "price": 89.90,
                "quantity": 60,
            },
            {
                "name": "Calça Jeans Feminina",
                "sku": "CAL-F001",
                "ean": "7891234000011",
                "price": 89.90,
                "quantity": 50,
            },
            {
                "name": "Tênis Esportivo",
                "sku": "TEN-E001",
                "ean": "7891234000020",
                "price": 149.90,
                "quantity": 30,
            },
            {
                "name": "Mochila Universitária",
                "sku": "MCH-U001",
                "ean": "7891234000030",
                "price": 69.90,
                "quantity": 40,
            },
            {
                "name": "Garrafa Térmica",
                "sku": "GAR-T001",
                "ean": "7891234000040",
                "price": 45.90,
                "quantity": 80,
            },
        ]

        products = []
        for pd in products_data:
            product = Product(
                id=uuid.uuid4(),
                name=pd["name"],
                sku=pd["sku"],
                ean=pd["ean"],
                price=pd["price"],
                quantity=pd["quantity"],
                is_active=True,
            )
            db.add(product)

            # Criar registro de EAN
            ean = EAN(
                id=uuid.uuid4(),
                product_id=product.id,
                ean_code=pd["ean"],
                is_active=True,
            )
            db.add(ean)

            # Criar registro de SKU
            sku = SKU(
                id=uuid.uuid4(),
                product_id=product.id,
                sku_code=pd["sku"],
                is_active=True,
            )
            db.add(sku)

        db.commit()

        # Criar pedidos de demonstração
        now = datetime.now()
        orders_data = [
            {
                "order_code": "ORG-001",
                "user_id": 2,
                "status": "completed",
                "created_at": now - timedelta(days=5),
                "items": [
                    {"product_name": "Camiseta Algodão P", "quantity": 2, "price": 29.90},
                    {"product_name": "Calça Jeans Masculina", "quantity": 1, "price": 89.90},
                ],
            },
            {
                "order_code": "ORG-002",
                "user_id": 3,
                "status": "shipped",
                "created_at": now - timedelta(days=2),
                "items": [
                    {"product_name": "Tênis Esportivo", "quantity": 1, "price": 149.90},
                ],
            },
            {
                "order_code": "ORG-003",
                "user_id": 2,
                "status": "pending",
                "created_at": now - timedelta(days=1),
                "items": [
                    {"product_name": "Mochila Universitária", "quantity": 2, "price": 69.90},
                ],
            },
        ]

        for od in orders_data:
            order = Order(
                id=uuid.uuid4(),
                order_code=od["order_code"],
                user_id=od["user_id"],
                status=od["status"],
                total_amount=sum(item["quantity"] * item["price"] for item in od["items"]),
                created_at=od["created_at"],
                shipping_address="Rua das Flores, 100 - São Paulo/SP",
            )
            db.add(order)

            # Reduzir estoque ao criar pedidos
            for item in od["items"]:
                product_name = item["product_name"]
                quantity = item["quantity"]
                # Encontrar o produto e reduzir estoque
                product = db.query(Product).filter(Product.name == product_name).first()
                if product:
                    product.quantity = max(0, product.quantity - quantity)

        db.commit()

        print("Seed de demonstração criado com sucesso!")
        print("- 3 contas criadas")
        print("- 3 usuários criados (admin, operador, gerente)")
        print("- 8 produtos com EANs e SKUs criados")
        print("- 3 pedidos de exemplo criados")

    except Exception as e:
        db.rollback()
        print(f"Erro ao criar seed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    create_demo_data()