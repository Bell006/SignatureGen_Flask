﻿# Gerador de Assinaturas Buriti Empreendimentos


## Descrição

SignatureGen é uma API para gerar assinaturas personalizadas. Este repositório contém o código backend da aplicação, desenvolvido em Python com Flask, que lida com o tratamento de dados, criação do arquivo de imagem personalizado e integração com o Google Drive.

### Linguagens e Frameworks

- **Python**: Linguagem de programação principal utilizada no desenvolvimento do backend.
- **Flask**: Framework web utilizado para construir a API da aplicação.
- **Gunicorn**: Servidor WSGI para servidores Unix, utilizado para gerenciar a aplicação Flask em produção.

### Bibliotecas

- **PIL (Pillow)**: Biblioteca de processamento de imagens utilizada para manipulação e geração de imagens.
- **re**: Módulo para expressões regulares em Python, utilizado para validação de entradas.
- **unidecode**: Biblioteca para remover acentos e caracteres especiais, utilizada na normalização de nomes de estados.
- **dotenv**: Biblioteca para carregar variáveis de ambiente a partir de um arquivo `.env`.
- **google-auth**: Biblioteca para autenticação e autorização utilizando Google OAuth 2.0.
- **google-api-python-client**: Cliente Python para acessar APIs do Google, utilizado para integração com o Google Drive.

### Outras Ferramentas

- **virtualenv**: Utilizado para criar ambientes virtuais Python isolados.
- **Render**: Plataforma de deploy utilizada para hospedar a aplicação em produção.
