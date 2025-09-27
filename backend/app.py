from sys import displayhook
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from flask import Flask, jsonify, request
from flask_apscheduler import APScheduler
from flask_cors import CORS
import logging
from datetime import datetime

CREDENTIALS_FILE = 'credentials.json'
SPREADSHEET_ID = '1OO7gDKXv4YJiDfpfrIHaXIa_XUgDhl3rG2FQImQ-ixY'

dados_da_planilha_cache = None
linhas_atuais_cache = None

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler("sheets.log"),
        logging.StreamHandler()
    ]
)

def buscar_planilha():
    global dados_da_planilha_cache, linhas_atuais_cache
    logging.info("Iniciando a busca e atualização da planilha.")
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

      if dados_da_planilha_cache is not None:
         novas_linhas = len(df) - len(dados_da_planilha_cache)
         if novas_linhas > 0:
            logging.info(f"DETECTADO: {novas_linhas} novas linhas adicionadas.")
      
      dados_da_planilha_cache = df
      linhas_atuais_cache = len(df)
      logging.info(f"Dados da planilha atualizados. Total de linhas: {linhas_atuais_cache}.")

    except Exception as e:
       logging.error(f"Erro ao buscar dados da planilha: {e}")
       dados_da_planilha_cache = None

# esse método seria para a utilização de um filtro para buscar dados na planilha
# tipo_de_busca = filtro(no caso da planilha teriamos como opção nome, id, cpf e numero)
# dado_buscado = busca(nesse caso, seria o dado que o usuario colocaria no input para fazer a busca)
def buscar(tipo_de_busca, dado_buscado):
   if not isinstance(dados_da_planilha_cache, pd.DataFrame) or dados_da_planilha_cache.empty:
        buscar_planilha()
        if not isinstance(dados_da_planilha_cache, pd.DataFrame) or dados_da_planilha_cache.empty:
            logging.warning('Tentativa de busca falhou, cache vazio')
            return jsonify({'erro': 'Não foi possível buscar os dados da planilha para a pesquisa.'}), 500
        
   try:
        nome_coluna = tipo_de_busca
        df_filtrado = dados_da_planilha_cache[
            dados_da_planilha_cache[nome_coluna].astype(str).str.contains(dado_buscado, case=False, na=False)
        ]

        if df_filtrado.empty:
            logging.info(f"Nenhum resultado foi encontrado para '{dado_buscado}' em '{nome_coluna}'. ")
            return jsonify({'mensagem': f'Nenhum resultado encontrado para o dado: {dado_buscado}'}), 404

        dado_json = df_filtrado.to_json(orient='records')
        logging.info(f"Busca por '{dado_buscado}' em '{nome_coluna}' concluída com sucesso.")
        return dado_json, 200
   
   except KeyError:
        logging.error(f"A coluna '{nome_coluna}' nao foi encontrada.")
        return jsonify({'erro': f"A coluna '{nome_coluna}' nao foi encontrada nos dados da planilha. Verifique o nome da coluna."}), 500
   except Exception as e:
        logging.error(f"Erro ao processar a busca: {e}")
        return jsonify({'erro': f'Erro ao processar a busca: {e}'}), 500


app = Flask(__name__)
CORS(app)

scheduler = APScheduler()
app.config.from_mapping(SCHEDULER_API_ENABLED=True)

#Modificação no nome da função/método/endpoint
@app.route('/api/dados', methods=['GET'])
def trazer_dados():
    # Verifica se o cache existe e não está vazio usando isinstance() e .empty
  if isinstance(dados_da_planilha_cache, pd.DataFrame) and not dados_da_planilha_cache.empty:
    dado_json = dados_da_planilha_cache.to_json(orient='records', force_ascii=False)
    return dado_json, 200 # Alterado para 200, que é o código padrão para sucesso
  else:
        # Se o cache estiver vazio ou não for um DataFrame, tenta buscar
    buscar_planilha()
        
        # Após a busca, verifica novamente se o cache foi preenchido corretamente
    if isinstance(dados_da_planilha_cache, pd.DataFrame) and not dados_da_planilha_cache.empty:
      dado_json = dados_da_planilha_cache.to_json(orient='records', force_ascii=False)
      return dado_json, 200
    else:
      return jsonify({'erro': 'Não foi possível buscar os dados da planilha.'}), 500


@app.route('/api/buscar/<string:filtro>/<string:dado>', methods=['GET'])
def buscar_dado(filtro, dado):
   return buscar(filtro, dado)


# Executa a aplicação
if __name__ == '__main__':
    scheduler.init_app(app)
    scheduler.add_job(id='Tarefa Atualização de Planilha', func=buscar_planilha, trigger='interval', minutes=5)
    scheduler.start()

    buscar_planilha()

    app.run(debug=True)