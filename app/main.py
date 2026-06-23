import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.database import get_connection, create_tables


APP_NAME = os.getenv("APP_NAME", "ServiceDesk Cloud API")
APP_ENV = os.getenv("APP_ENV", "development")


app = FastAPI(
    title=APP_NAME,
    description=f"API REST para gerenciamento de chamados internos. Ambiente: {APP_ENV}.",
    version="1.0.0"
)


class ChamadoCreate(BaseModel):
    titulo: str
    descricao: str
    setor: str
    prioridade: str


class ChamadoUpdateStatus(BaseModel):
    status: str


@app.on_event("startup")
def startup():
    create_tables()


@app.get("/")
def home():
    return {
        "mensagem": "ServiceDesk Cloud API em execução",
        "documentacao": "/docs",
        "healthcheck": "/health"
    }


@app.get("/health")
def healthcheck():
    return {
        "status": "ok",
        "servico": "ServiceDesk Cloud API"
    }


@app.post("/chamados")
def criar_chamado(chamado: ChamadoCreate):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO chamados (titulo, descricao, setor, prioridade)
        VALUES (?, ?, ?, ?)
    """, (
        chamado.titulo,
        chamado.descricao,
        chamado.setor,
        chamado.prioridade
    ))

    connection.commit()
    chamado_id = cursor.lastrowid
    connection.close()

    return {
        "mensagem": "Chamado criado com sucesso",
        "id": chamado_id
    }


@app.get("/chamados")
def listar_chamados():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, titulo, descricao, setor, prioridade, status, criado_em
        FROM chamados
        ORDER BY id DESC
    """)

    chamados = [dict(row) for row in cursor.fetchall()]
    connection.close()

    return chamados


@app.get("/chamados/{chamado_id}")
def consultar_chamado(chamado_id: int):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, titulo, descricao, setor, prioridade, status, criado_em
        FROM chamados
        WHERE id = ?
    """, (chamado_id,))

    chamado = cursor.fetchone()
    connection.close()

    if chamado is None:
        raise HTTPException(status_code=404, detail="Chamado não encontrado")

    return dict(chamado)


@app.patch("/chamados/{chamado_id}/status")
def atualizar_status(chamado_id: int, dados: ChamadoUpdateStatus):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE chamados
        SET status = ?
        WHERE id = ?
    """, (dados.status, chamado_id))

    connection.commit()

    if cursor.rowcount == 0:
        connection.close()
        raise HTTPException(status_code=404, detail="Chamado não encontrado")

    connection.close()

    return {
        "mensagem": "Status atualizado com sucesso",
        "id": chamado_id,
        "novo_status": dados.status
    }


@app.delete("/chamados/{chamado_id}")
def excluir_chamado(chamado_id: int):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM chamados
        WHERE id = ?
    """, (chamado_id,))

    connection.commit()

    if cursor.rowcount == 0:
        connection.close()
        raise HTTPException(status_code=404, detail="Chamado não encontrado")

    connection.close()

    return {
        "mensagem": "Chamado excluído com sucesso",
        "id": chamado_id
    }