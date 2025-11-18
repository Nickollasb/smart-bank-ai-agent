import requests
import csv

#TODO: Add error handling and logging

def http_request(method: str, url: str) -> dict:
    """Make an HTTP request to a given URL and return the response on JSON."""
    try:
        response = requests.request(method, url)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
    
    
def read_data(file_path: str) -> list[dict]:
    """Lê o arquivos .csv e retorna uma lista de dicionários."""
    try:
        with open(file=file_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            return [row for row in reader]
    except FileNotFoundError:
        print("⚠️ Erro: Arquivo clientes.csv não encontrado.")
        return []
    
def update_data(file_path: str, column_name: str, row_id: str, value: str) -> bool:
    """
    Atualiza apenas a linha do CSV onde column_name == row_id.
    Exemplo: update_data("clientes.csv", "cpf", "05613638110", "850")
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
        print(f"❌ Erro: Arquivo não encontrado: {file_path}")
        return False
