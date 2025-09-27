document.addEventListener("DOMContentLoaded", () => {
  const searchInput = document.getElementById("search-input");
  const filterButton = document.getElementById("filter");
  const buttonText = document.getElementById("button_text");
  const dataTable = document.getElementById("data-table");
  const tableHead = dataTable.querySelector("thead tr");
  const tableBody = dataTable.querySelector("tbody");

  const options = ["nome", "número", "email", "cpf"];
  let index = 0;

  /**
   * Popula a tabela com um conjunto de dados.
   * Limpa a tabela antes de adicionar os novos dados.
   * @param {Array<Object>} data - Os dados para exibir.
   */
  function popularTabela(data) {
    tableHead.innerHTML = "";
    tableBody.innerHTML = "";

    if (!data || data.length === 0) {
      tableBody.innerHTML =
        '<tr><td colspan="100%">Nenhum resultado encontrado.</td></tr>';
      return;
    }

    const headers = Object.keys(data[0]);
    headers.forEach((headerText) => {
      const th = document.createElement("th");
      th.textContent = headerText;
      tableHead.appendChild(th);
    });

    data.forEach((item) => {
      const tr = document.createElement("tr");
      headers.forEach((header) => {
        const td = document.createElement("td");
        td.textContent = item[header];
        td.setAttribute("data-label", header);
        tr.appendChild(td);
      });
      tableBody.appendChild(tr);
    });
  }

  /**
   * Busca dados na API com base no filtro e termo de busca.
   */
  async function buscarDadoDaAPI() {
    const filterType = options[index];
    const searchTerm = searchInput.value.trim();

    // Se o termo de busca for vazio, busca todos os dados. Senão, busca o termo específico.
    const apiUrl = searchTerm
      ? `https://rede-alpha-fitness-desafio.onrender.com/api/buscar/${filterType}/${searchTerm}`
      : `https://rede-alpha-fitness-desafio.onrender.com/api/dados`;

    tableBody.innerHTML = '<tr><td colspan="100%">Buscando...</td></tr>';

    try {
      const response = await fetch(apiUrl);
      if (response.status === 404) {
        popularTabela([]); // Chama a função com um array vazio
        return;
      }
      if (!response.ok) {
        throw new Error(`Erro de rede: ${response.statusText}`);
      }
      const data = await response.json();
      popularTabela(data);
    } catch (error) {
      console.error("Erro ao buscar na API:", error);
      tableBody.innerHTML = `<tr><td colspan="100%" style="color: red;">Falha na busca.</td></tr>`;
    }
  }

  filterButton.addEventListener("click", () => {
    index = (index + 1) % options.length;
    buttonText.textContent = options[index];
  });

  searchInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
      buscarDadoDaAPI();
    }
  });

  buscarDadoDaAPI();
});

// document.addEventListener("DOMContentLoaded", () => {
//   const searchInput = document.getElementById("search-input");
//   const filterButton = document.getElementById("filter");
//   const buttonText = document.getElementById("button_text");
//   const dataTable = document.getElementById("data-table");
//   const tableHead = dataTable.querySelector("thead tr");
//   const tableBody = dataTable.querySelector("tbody");
//   // URL da sua API local (certifique-se de que a API Flask está rodando)
//   const filterOptions = ["nome", "cpf", "numero"];
//   let currentFilterIndex = 0;

//   async function popularTabela() {
//     const api_url = "https://rede-alpha-fitness-desafio.onrender.com/api/dados";

//     tableBody.innerHTML =
//       '<tr><td colspan="100%">Carregando dados...</td></tr>';

//     try {
//       const response = await fetch(api_url);
//       if (!response.ok) {
//         throw new Error(`Erro de rede ${response.statusText}`);
//       }

//       const data = await response.json();

//       if (data && data > 0) {
//         const header = Object.keys[data[0]];
//         header.forEach((headerText) => {
//           const th = document.createElement("th");
//           th.textContent = headerText;
//           tableHead.appendChild(th);
//         });
//         data.forEach((item) => {
//           const tr = document.createElement("tr");
//           header.forEach((header) => {
//             const td = document.createElement("td");
//             td.textContent = item[header];
//             // Adiciona um atributo 'data-label' para responsividade no CSS
//             td.setAttribute("data-label", header);
//             tr.appendChild(td);
//           });
//           tableBody.appendChild(tr);
//         });
//       } else {
//         tableBody.innerHTML =
//           '<tr><td colspan="100%">Nenhum dado encontrado.</td></tr>';
//       }
//     } catch (error) {
//       console.error("Erro ao buscar dados da API:", error);
//       tableBody.innerHTML = `<tr><td colspan="100%" style="color: red;">Falha ao carregar dados. Tente recarregar a página.</td></tr>`;
//     }
//   }

//   async function fetchDataFromAPI() {
//     const filterType = filterOptions[currentFilterIndex];
//     const searchTerm = searchInput.value.trim();

//     // Se o termo de busca for vazio, busca todos os dados. Senão, busca o termo específico.
//     const apiUrl = searchTerm
//       ? `https://rede-alpha-fitness-desafio.onrender.com/api/buscar/${filterType}/${searchTerm}`
//       : `https://rede-alpha-fitness-desafio.onrender.com/api/dados`;

//     tableBody.innerHTML = '<tr><td colspan="100%">Buscando...</td></tr>';

//     try {
//       const response = await fetch(apiUrl);
//       // A API retorna 404 para "nenhum resultado", o que é OK.
//       if (response.status === 404) {
//         populateTable([]); // Chama a função com um array vazio
//         return;
//       }
//       if (!response.ok) {
//         throw new Error(`Erro de rede: ${response.statusText}`);
//       }
//       const data = await response.json();
//       populateTable(data);
//     } catch (error) {
//       console.error("Erro ao buscar na API:", error);
//       tableBody.innerHTML = `<tr><td colspan="100%" style="color: red;">Falha na busca.</td></tr>`;
//     }
//   }

//   // --- 4. EVENT LISTENERS ---

//   filterButton.addEventListener("click", () => {
//     currentFilterIndex = (currentFilterIndex + 1) % filterOptions.length;
//     buttonText.textContent = filterOptions[currentFilterIndex];
//   });

//   // Busca ao pressionar "Enter"
//   searchInput.addEventListener("keydown", (event) => {
//     if (event.key === "Enter") {
//       fetchDataFromAPI();
//     }
//   });

//   // --- 5. INICIALIZAÇÃO ---
//   // Carrega todos os dados ao iniciar a página
//   fetchDataFromAPI();
// });
//   fetch(api_url)
//     .then((response) => {
//       if (!response.ok) {
//         throw new Error(`Erro de rede: ${response.statusText}`);
//       }
//       return response.json();
//     })
//     .then((data) => {
//       // // Converte a string JSON para um objeto JavaScript
//       // const parsedData = JSON.parse(data);

//       const table = document.getElementById("data-table");
//       const thead = table.querySelector("thead tr");
//       const tbody = table.querySelector("tbody");

//       if (data.length > 0) {
//         // Cria os cabeçalhos da tabela
//         const headers = Object.keys(data[0]);
//         headers.forEach((headerText) => {
//           const th = document.createElement("th");
//           th.textContent = headerText;
//           thead.appendChild(th);
//         });

//         // Preenche o corpo da tabela com os dados
//         data.forEach((item) => {
//           const tr = document.createElement("tr");
//           headers.forEach((header) => {
//             const td = document.createElement("td");
//             td.textContent = item[header];
//             tr.appendChild(td);
//           });
//           tbody.appendChild(tr);
//         });
//       } else {
//         tbody.innerHTML =
//           '<tr><td colspan="100%">Nenhum dado encontrado.</td></tr>';
//       }
//     })
//     .catch((error) => {
//       console.error("Erro ao buscar dados da API:", error);
//       alert(
//         "Erro ao carregar os dados. Verifique o console para mais detalhes."
//       );
//     });
// });

// const input = document.getElementById("search-input");
// const button_filter = document.getElementById("filter");
// const button_text = document.getElementById("button_text");

// const options = ["nome", "cpf", "número"];
// let index = 0;
// let opcao;
// button_filter.addEventListener("click", () => {
//   index = (index + 1) % options.length;
//   button_text.textContent = options[index];
//   opcao = options[index];
// });

// input.addEventListener("keydown", (event) => {
//   if (event.key !== "Enter") {
//     return;
//   }

//   let valorInput = input.value.trim();
//   console.log(valorInput);

//   if (!valorInput) {
//     console.log("Input inválido");
//     return;
//   }

//   const api_url = `/api/buscar/${opcao}/${valorInput}`;

//   fetch(api_url)
//     .then((response) => {
//       if (!response.ok) {
//         return response.json().then((errorData) => {
//           // Lançamos um erro personalizado com a mensagem da sua API
//           throw new Error(
//             errorData.mensagem || errorData.erro || `Erro ${response.status}`
//           );
//         });
//       }
//       return response.json();
//     })
//     .then((data) => {
//       console.log(`Dado recebido ${data}`);
//     });
// });
