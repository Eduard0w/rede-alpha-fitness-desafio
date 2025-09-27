# rede-alpha-fitness-desafio

# Desafio Rede Alpha Fitness: Leitor de Planilhas

Este projeto é uma aplicação web completa que lê dados de uma planilha do Google Sheets, os exibe em uma tabela interativa e permite que o usuário realize buscas dinâmicas em tempo real. A aplicação é composta por um backend em Flask (Python) que serve uma API e um frontend em HTML, CSS e JavaScript puro.

## ✨ Funcionalidades Principais

- **Leitura de Planilha Google Sheets**: O backend se conecta de forma segura à API do Google Sheets para buscar os dados.
- **Cache de Dados**: Os dados da planilha são mantidos em um cache no servidor, que é atualizado periodicamente (a cada 5 minutos) para otimizar a performance e evitar chamadas excessivas à API.
- **API RESTful**: Um servidor Flask expõe endpoints para buscar todos os dados ou para realizar buscas filtradas.
- **Tabela Dinâmica**: O frontend busca os dados da API e constrói a tabela de forma dinâmica, incluindo os cabeçalhos.
- **Busca Inteligente em Tempo Real**:
  - **Filtros Dinâmicos**: O usuário pode alternar entre diferentes colunas para a busca (Nome, CPF, Número).
  - **Busca "Começa Com"**: A pesquisa filtra os resultados que começam com o texto digitado.
  - **Ignora Maiúsculas/Minúsculas**: A busca não diferencia letras maiúsculas de minúsculas.
  - **Ignora Acentos**: Pesquisar por "joao" encontra "João".
  - **Campos Numéricos**: A busca por CPF e número funciona mesmo que os dados contenham ou não pontuação.
- **Design Responsivo**: A interface se adapta a diferentes tamanhos de tela, de desktops a dispositivos móveis.

## 🛠️ Tecnologias Utilizadas

### Backend

- **Python 3**: Linguagem principal do servidor.
- **Flask**: Micro-framework web para criar a API.
- **Pandas**: Para manipulação e filtragem eficiente dos dados em memória.
- **GSpread & oauth2client**: Para autenticação e comunicação com a API do Google Sheets.
- **Flask-APScheduler**: Para agendar a tarefa de atualização periódica do cache da planilha.
- **Flask-Cors**: Para permitir que o frontend acesse a API.

### Frontend

- **HTML5**: Estrutura da página.
- **CSS3**: Estilização e responsividade.
- **JavaScript (Vanilla JS)**: Para interatividade, chamadas à API e manipulação do DOM.

### Deploy

- **Render**: A aplicação está configurada para deploy na plataforma Render. Deploy da API.
- **Vercel**: Deploy da aplicação FrontEnd

### 6. Acessando site:

Acesse `https://rede-alpha-fitness-desafio.vercel.app` no seu navegador para ver a aplicação funcionando.

## ⚙️ Estrutura da API

A API Flask expõe os seguintes endpoints:

- `GET /api/dados`

  - Retorna todos os dados da planilha em formato JSON. Utiliza o cache para respostas rápidas.

- `GET /api/buscar/<filtro>/<dado>`
  - Realiza uma busca filtrada nos dados.
  - `filtro`: A coluna onde a busca será realizada (ex: `nome`, `cpf` ).
  - `dado`: O termo a ser buscado.

## Autor

- **Eduardo Brito** - [Eduard0w](https://github.com/Eduard0w)
