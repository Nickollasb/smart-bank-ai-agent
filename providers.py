import requests
import csv
from datetime import datetime
import pytz
import json

def http_request(method: str, url: str) -> dict:
    """Faz uma chamada HTTP para uma URL fornecida e retorna a resposta em JSON."""
    try:
        response = requests.request(method, url)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Ocorreu um erro ao realizar a chamada de API: {e}")
        return None
    
    
def read_data(file_path: str) -> list[dict]:
    """Lê o arquivos .csv e retorna uma lista de dicionários."""
    try:
        with open(file=file_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            return [row for row in reader]
    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado: {file_path}")
        return False
    
def update_data(file_path: str, column_name: str, row_id: str, value: str) -> bool:
    """
    Atualiza apenas a linha do CSV onde column_name == row_id.
    """
    try:
        # 1. Ler todo o arquivo
        rows = []
        updated = False

        with open(file_path, "r", encoding="utf-8", newline="") as infile:
            reader = csv.DictReader(infile)
            fieldnames = reader.fieldnames  # mantém as colunas originais

            for row in reader:
                if row.get(column_name) == row_id:
                    row["score"] = value      # altera SOMENTE o valor desejado
                    updated = True
                rows.append(row)

        if not updated:
            print(f"⚠️ Nenhuma linha encontrada com {column_name} = {row_id}")
            return False

        # 2. Reescrever o arquivo com a linha alterada
        with open(file_path, "w", encoding="utf-8", newline="") as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

        return True

    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado: {file_path}")
        return False
    
def insert_data(file_path: str, new_data: dict) -> list[dict]:
    """Adiciona um novo dado em arquivos .csv"""
    try:
        with open(file=file_path, mode="a", newline='', encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(dict_to_list(new_data))
    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado: {file_path}")
        return False

def get_current_datetime() -> str:
    """Retorna a data e hora atual no formato ISO 8601 com fuso horário de São Paulo (GMT -3)."""
    tz = pytz.timezone('America/Sao_Paulo')
    return datetime.now(tz).isoformat()

def dict_to_list(dict_data):
    return [str(value) for value in dict_data.values()]