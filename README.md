# ServiceDesk Cloud API

API REST simples para gerenciamento de chamados internos, desenvolvida em Python com FastAPI, containerizada com Docker e preparada para deploy em nuvem usando AWS EC2.

## Objetivo do projeto

O objetivo deste projeto é criar uma aplicação web simples, funcional e profissional para demonstrar o uso de Docker e computação em nuvem. A aplicação permite registrar, listar, consultar, atualizar e excluir chamados de suporte interno.

Este projeto foi desenvolvido como uma aplicação prática para estudo de containers, arquitetura em nuvem, persistência de dados, rede, porta, volume Docker e deploy em ambiente IaaS.

## Tecnologias utilizadas

* Python
* FastAPI
* Uvicorn
* SQLite
* Docker
* Docker Compose
* AWS EC2
* VS Code
* Git e GitHub

## Modelo de nuvem escolhido

O modelo escolhido para o projeto é IaaS, utilizando uma instância EC2 na AWS.

A escolha por IaaS permite maior controle sobre a infraestrutura, pois o desenvolvedor precisa configurar o sistema operacional, instalar o Docker, configurar portas, redes, segurança e realizar o deploy manual da aplicação.

Essa abordagem é ideal para aprendizado, pois permite compreender melhor os fundamentos de computação em nuvem, infraestrutura, containers e responsabilidade compartilhada.

## Funcionalidades da API

* Verificar se a API está online
* Verificar a saúde do serviço
* Criar chamados
* Listar chamados
* Consultar chamado por ID
* Atualizar status de chamado
* Excluir chamado

## Endpoints principais

| Método | Endpoint                      | Descrição                    |
| ------ | ----------------------------- | ---------------------------- |
| GET    | /                             | Página inicial da API        |
| GET    | /health                       | Verifica a saúde do serviço  |
| POST   | /chamados                     | Cria um novo chamado         |
| GET    | /chamados                     | Lista todos os chamados      |
| GET    | /chamados/{chamado_id}        | Consulta um chamado por ID   |
| PATCH  | /chamados/{chamado_id}/status | Atualiza o status do chamado |
| DELETE | /chamados/{chamado_id}        | Exclui um chamado            |

## Estrutura do projeto

```text
servicedesk-cloud-api/
│
├── app/
│   ├── main.py
│   └── database.py
│
├── data/
│
├── .dockerignore
├── .env.example
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

## Como rodar localmente com ambiente virtual

Criar ambiente virtual:

```bash
python -m venv .venv
```

Ativar no Windows PowerShell:

```bash
.\.venv\Scripts\Activate.ps1
```

Instalar dependências:

```bash
pip install -r requirements.txt
```

Rodar aplicação:

```bash
uvicorn app.main:app --reload
```

Acessar no navegador:

```text
http://localhost:8000
```

Documentação da API:

```text
http://localhost:8000/docs
```

## Como rodar com Docker

Construir e iniciar o container:

```bash
docker compose up -d --build
```

Verificar containers em execução:

```bash
docker ps
```

Acessar a aplicação:

```text
http://localhost:8000
```

Acessar a documentação:

```text
http://localhost:8000/docs
```

Ver logs:

```bash
docker compose logs -f
```

Parar a aplicação:

```bash
docker compose down
```

Parar e remover também o volume:

```bash
docker compose down -v
```

Atenção: o comando `docker compose down -v` remove o volume Docker e apaga o banco de dados persistente.

## Persistência de dados

A aplicação utiliza SQLite como banco de dados e armazena o arquivo do banco em um volume Docker.

O volume configurado é:

```text
servicedesk_data
```

Esse volume permite que os dados continuem salvos mesmo quando o container é parado ou recriado.

## Rede Docker

O projeto utiliza uma rede Docker própria chamada:

```text
servicedesk_network
```

Essa rede isola a comunicação da aplicação e simula uma configuração mais próxima de ambientes profissionais.

## Porta utilizada

A aplicação roda na porta interna `8000` do container e é exposta na porta `8000` da máquina local.

```text
localhost:8000 -> container:8000
```

## Healthcheck

O Docker Compose possui um healthcheck configurado para verificar periodicamente se a API está respondendo corretamente.

Endpoint usado:

```text
GET /health
```

Quando a aplicação está saudável, o container aparece com status:

```text
healthy
```

## Estratégia de deploy em nuvem

A estratégia inicial de deploy será manual em uma instância AWS EC2 com Amazon Linux 2023.

Etapas previstas:

1. Criar conta AWS.
2. Configurar alerta de orçamento.
3. Criar instância EC2 Free Tier.
4. Configurar Security Group.
5. Liberar apenas as portas necessárias.
6. Acessar a instância via SSH.
7. Instalar Docker e Docker Compose.
8. Clonar o repositório GitHub.
9. Executar a aplicação com Docker Compose.
10. Testar a API pelo IP público da instância.

## Segurança

Boas práticas consideradas no projeto:

* Não armazenar senhas no código.
* Utilizar `.env.example` como modelo de configuração.
* Executar a aplicação no container com usuário não-root.
* Expor apenas a porta necessária.
* Usar Security Group na AWS.
* Restringir o SSH ao IP do desenvolvedor.
* Utilizar volume persistente para os dados.
* Aplicar o conceito de responsabilidade compartilhada em nuvem.

## Arquitetura

A documentação da arquitetura do projeto está disponível em: 
docs/arquitetura.md

## Evoluções futuras

Possíveis melhorias futuras:

* Criar uma interface web para consumir a API.
* Adicionar autenticação de usuários.
* Trocar SQLite por PostgreSQL.
* Utilizar Amazon RDS para banco gerenciado.
* Criar pipeline CI/CD com GitHub Actions.
* Publicar imagem no Docker Hub ou Amazon ECR.
* Migrar o deploy para AWS App Runner, ECS ou Fargate.
* Adicionar monitoramento e logs centralizados.
* Configurar domínio e HTTPS.

## Autor

Projeto desenvolvido para fins acadêmicos e práticos, com o objetivo de aplicar conceitos de Docker, API REST, computação em nuvem e deploy em ambiente IaaS.

:::writing{variant="document" id="27184"}
## Estratégia de deploy em nuvem

A estratégia inicial de deploy foi manual em uma instância AWS EC2 utilizando Amazon Linux 2023.

Etapas realizadas:

1. Criação da instância EC2 na AWS.
2. Configuração do Security Group.
3. Liberação da porta 22 para acesso SSH administrativo.
4. Liberação da porta 8000 para acesso à API.
5. Acesso à instância EC2 via terminal.
6. Instalação do Git, Docker e Docker Compose.
7. Clonagem do repositório GitHub na instância EC2.
8. Criação do arquivo `.env` no ambiente da EC2.
9. Execução da aplicação com Docker Compose.
10. Teste da API pelo IP público da instância.

Fluxo utilizado:

```text
Computador local → GitHub → AWS EC2 → Docker Compose → Container FastAPI
```