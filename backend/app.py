from sys import displayhook
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from flask import Flask, jsonify
from flask_cors import CORS
#URL está modificada para conseguir ser lida
urlDoArquivo = "https://docs.google.com/spreadsheets/d/1OO7gDKXv4YJiDfpfrIHaXIa_XUgDhl3rG2FQImQ-ixY/export?format=csv&gid=0"

CREDENTIALS_FILE = 'credentials.json'
SPREADSHEET_ID = '1OO7gDKXv4YJiDfpfrIHaXIa_XUgDhl3rG2FQImQ-ixY'

scopes = [
  "https://spreadsheets.google.com/feeds",
  "https://www.googleapis.com/auth/drive",
]
creds = ServiceAccountCredentials.from_json_keyfile_name(
  CREDENTIALS_FILE,
  scopes,
)
client = gspread.authorize(creds) #cliente criado e autorizado para ler/modificar a planilha

planilha_completa = client.open_by_key(SPREADSHEET_ID)
pagina_planilha = planilha_completa.get_worksheet(0)#pega a aba/página especifica para ser lida/modificada

def mostrar_planilha():
  dados = pagina_planilha.get_all_records()
  df = pd.DataFrame(dados)
  # print(df)
  return df




# worksheet = df.sheet1
# dataframe = pd.DataFrame(worksheet.get_all_records())
# print(df.head()) #mostra apenas 4 linhas do arquivo
# print(df.index) #não entendi o que mostra...
# print(df.sort_values(by="id"))
# print(df["nome"] == "Sra. Isabelly Lopes")
# # displayhook(df)

app = Flask(__name__)
CORS(app)

@app.route('/api/dados', methods=['GET'])
def trazerInformacao():
  dados_json = mostrar_planilha().to_json(orient='records')
  return jsonify(dados_json), 201

# Executa a aplicação
if __name__ == '__main__':
    app.run(debug=True)

# Fazer endpoit de busca de usuario pelo nome/cpf/id.
# Fazer logs para a identificação de novas adições na planilha (teste).