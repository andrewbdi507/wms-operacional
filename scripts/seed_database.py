"""Script para popular o banco de dados com dados de demonstração.

Executa o seed_com_codigos_fixos.py e verifica se os dados foram
criados corretamente.
"""

from app.seed_com_codigos_fixos import create_demo_data

if __name__ == "__main__":
    create_demo_data()
    print("Banco de dados populado com sucesso!")