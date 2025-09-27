document.addEventListener("DOMContentLoaded", () => {
  // URL da sua API local (certifique-se de que a API Flask está rodando)
  const api_url = "https://rede-alpha-fitness-desafio.onrender.com/api/dados";

  fetch(api_url)
    .then((response) => {
      if (!response.ok) {
        throw new Error(`Erro de rede: ${response.statusText}`);
      }
      return response.json();
    })
    .then((data) => {
      // // Converte a string JSON para um objeto JavaScript
      // const parsedData = JSON.parse(data);

      const table = document.getElementById("data-table");
      const thead = table.querySelector("thead tr");
      const tbody = table.querySelector("tbody");

      if (data.length > 0) {
        // Cria os cabeçalhos da tabela
        const headers = Object.keys(data[0]);
        headers.forEach((headerText) => {
          const th = document.createElement("th");
          th.textContent = headerText;
          thead.appendChild(th);
        });

        // Preenche o corpo da tabela com os dados
        data.forEach((item) => {
          const tr = document.createElement("tr");
          headers.forEach((header) => {
            const td = document.createElement("td");
            td.textContent = item[header];
            tr.appendChild(td);
          });
          tbody.appendChild(tr);
        });
      } else {
        tbody.innerHTML =
          '<tr><td colspan="100%">Nenhum dado encontrado.</td></tr>';
      }
    })
    .catch((error) => {
      console.error("Erro ao buscar dados da API:", error);
      alert(
        "Erro ao carregar os dados. Verifique o console para mais detalhes."
      );
    });
});

const input = document.getElementById("search-input");
const button_filter = document.getElementById("filter");
const button_text = document.getElementById("button_text");

const options = ["nome", "cpf", "número"];
let index = 0;
let opcao;
button_filter.addEventListener("click", () => {
  index = (index + 1) % options.length;
  button_text.textContent = options[index];
  opcao = options[index];
});

input.addEventListener("keydown", (event) => {
  let valorInput = input.value;
  console.log(valorInput);

  const api_url = `/api/buscar/${opcao}/${valorInput}`;

  fetch(api_url).then((response) => {
    if (!response.ok) {
      throw new Error(`Erro de rede: ${response.statusText}`);
    }
    return response.json();
  });
});
