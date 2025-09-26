from sys import displayhook
import pandas as pd
import gspread
from flask import Flask, jsonify
from flask_cors import CORS
#URL está modificada para conseguir ser lida
urlDoArquivo = "https://docs.google.com/spreadsheets/d/1OO7gDKXv4YJiDfpfrIHaXIa_XUgDhl3rG2FQImQ-ixY/export?format=csv&gid=0"

CREDENTIALS_FILE = 'credentials.json'
SPREADSHEET_ID = '1OO7gDKXv4YJiDfpfrIHaXIa_XUgDhl3rG2FQImQ-ixY'
WORKSHEET_NAME = 'Página1'

#Aqui: "on_bad_lines='warn'"; ele ignora as linhas problemáticas
#df = pd.read_csv(urlDoArquivo, on_bad_lines='warn')
df = pd.DataFrame()

def pegar_dados_planilha():
   try:
    gc = gspread.service_account(filename=CREDENTIALS_FILE)#usada para autenticar e autorizar uma aplicação Python, através do uso de uma conta de serviço (service account) de uma Conta Google, para aceder e interagir com o Google Sheets
    sh = gc.open_by_key(SPREADSHEET_ID)
    worksheet = sh.worksheet(WORKSHEET_NAME)

    records = worksheet.get_all_records()
    dataframe = pd.DataFrame(records)

    return dataframe
   except Exception as e:
    print(f"Erro ao ler dados da planilha: {e}")
    return pd.DataFrame()








worksheet = df.sheet1
dataframe = pd.DataFrame(worksheet.get_all_records())
# print(df.head()) #mostra apenas 4 linhas do arquivo
# print(df.index) #não entendi o que mostra...
# print(df.sort_values(by="id"))
# print(df["nome"] == "Sra. Isabelly Lopes")
# # displayhook(df)

app = Flask(__name__)
CORS(app)
# Define uma rota de exemplo
@app.route('/api/dados', methods=['GET'])
def trazerInformacao():
  dados_json = df.head().to_json(orient='records')
  return jsonify(dados_json), 201

# Executa a aplicação
if __name__ == '__main__':
    app.run(debug=True)

# Fazer endpoit de busca de usuario pelo nome/cpf/id.
# Fazer logs para a identificação de novas adições na planilha (teste).