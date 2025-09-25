from sys import displayhook
import pandas as pd
from flask import Flask

urlDoArquivo = "https://docs.google.com/spreadsheets/d/1OO7gDKXv4YJiDfpfrIHaXIa_XUgDhl3rG2FQImQ-ixY/edit?gid=0#gid=0"

df = pd.read_csv(urlDoArquivo)

# print(df.head())

displayhook(df)

#app = Flask(__name__)

# Define uma rota de exemplo
# @app.route('/api/dados', methods=['GET'])
# def trazerInformações():
#     return {"mensagem": "Dados criados com sucesso"}, 201

# # Executa a aplicação
# if __name__ == '__main__':
#     app.run(debug=True)