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
    
def find_data(file_path: str, search_column: str, search_row_key: str) -> list[dict]:
    """
    Lê um arquivo .csv e retorna uma lista de dicionários
    onde o valor da coluna `search_column` é igual a `search_row_key`.
    """
    try:
        with open(file_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)

            if search_column not in reader.fieldnames:
                raise ValueError(f"Column '{search_column}' not found in file.")

            results = [
                row
                for row in reader
                if row.get(search_column) == search_row_key
            ]

            return results

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found")
        return []


def update_data(file_path: str, search_column: str, search_row_key: str, field_name: str, new_value: str) -> bool:
    """
    Atualiza apenas a linha do CSV onde encontrar o respectivo search_column e search_row_key.
    """
    try:
        # 1. Ler todo o arquivo
        rows = []
        updated = False

        with open(file_path, "r", encoding="utf-8", newline="") as infile:
            reader = csv.DictReader(infile)
            fieldnames = reader.fieldnames

            for row in reader:
                if row.get(search_column) == search_row_key:
                    row[field_name] = new_value
                    updated = True
                rows.append(row)

        if not updated:
            print(f"No lines found at '{file_path}' in column '{search_column}' with key '{search_row_key}'")
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

def convert_date_to_raw_format(date: str):
    data = date.split('/')
    data.reverse()
    return '-'.join(data)