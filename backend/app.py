from sys import displayhook
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from flask import Flask, jsonify
from flask_apscheduler import APScheduler
from flask_cors import CORS

#URL está modificada para conseguir ser lida
# urlDoArquivo = "https://docs.google.com/spreadsheets/d/1OO7gDKXv4YJiDfpfrIHaXIa_XUgDhl3rG2FQImQ-ixY/export?format=csv&gid=0"

CREDENTIALS_FILE = 'credentials.json'
SPREADSHEET_ID = '1OO7gDKXv4YJiDfpfrIHaXIa_XUgDhl3rG2FQImQ-ixY'

dados_da_planilha_cache = None

#Antes era mostrar_planilha
def buscar_planilha():
    global dados_da_planilha_cache
    try:
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
      dados = pagina_planilha.get_all_records()
      df = pd.DataFrame(dados)
      
      dados_da_planilha_cache = df
      print("Dados da planilha atualizados com sucesso.")

    except Exception as e:
       print(f"Erro ao buscar dados da planilha: {e}")
       dados_da_planilha_cache = None


app = Flask(__name__)
CORS(app)

scheduler = APScheduler()
app.config.from_mapping(SCHEDULER_API_ENABLED=True)

#Modificação no nome da função/método/endpoint
@app.route('/api/dados', methods=['GET'])
def trazer_dados():
  if dados_da_planilha_cache:
    dado_json = dados_da_planilha_cache.to_json(orient='records')
    return dado_json, 201
  else:
     buscar_planilha()
     if dados_da_planilha_cache:
      dado_json = dados_da_planilha_cache.to_json(orient='records')
      return dado_json, 200
     else:
      return jsonify({'erro': 'Não foi possível buscar os dados da planilha.'}), 500

# def filtrar_dados():
#    return 0



# Executa a aplicação
if __name__ == '__main__':
    scheduler.init_app(app)
    scheduler.add_job(id='Tarefa Atualização de Planilha', func=buscar_planilha, trigger='interval', minutes=5)
    scheduler.start()

    buscar_planilha()

    app.run(debug=True)

#TO DO: Fazer endpoit de busca de usuario pelo nome/cpf/id.
#TO DO: Fazer logs para a identificação de novas adições na planilha (teste).

# worksheet = df.sheet1
# dataframe = pd.DataFrame(worksheet.get_all_records())
# print(df.head()) #mostra apenas 4 linhas do arquivo
# print(df.index) #não entendi o que mostra...
# print(df.sort_values(by="id"))
# print(df["nome"] == "Sra. Isabelly Lopes")
# # displayhook(df)