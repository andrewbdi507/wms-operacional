# Limitações Conhecidas

## Visão Geral

Este sistema possui as seguintes limitações conhecidas:

1. **Demonstração apenas**: Este projeto foi criado para fins de demonstração e não deve ser usado em produção sem as devidas adequações de segurança e escalabilidade.

2. **Banco de dados**: Usa SQLite para demonstração. Para produção, recomenda-se PostgreSQL.

3. **Funcionalidades limitadas**: Alguns recursos avançados de WMS podem não estar disponíveis na versão de demonstração.

4. **Desempenho**: Não otimizado para alto volume de transações.

5. **Integrações**: Integrações com Mercado Livre e Olist são simuladas para demonstração.

## Questões de Segurança

- Senhas e credenciais em .env.example são apenas exemplos
- Nunca use credenciais reais em ambientes públicos
- O sistema não armazena dados sensíveis em texto plano na versão demo