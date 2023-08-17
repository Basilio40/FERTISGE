const ctx = document.getElementById('graph-rece-desp').getContext('2d');
class Receitas {
    label = "Receitass";
    backgroundColor = "#129e3f";
    borderWidth = 0;
    data = [];

    constructor(data) {
        this.data = data
    }
}

class Despesas {
    label = "Despesas";
    backgroundColor = "#d72638";
    borderWidth = 0;
    data = [];

    constructor(data) {
        this.data = data
    }
}

function get_data(filter) {
    url= "/financeiro/lancamentos/graphdata/"    

    fetchOptions = {
        method: "POST",
        headers: {
            "X-CSRFToken": get_csrf(),
        },
        body: {
            table: document.querySelector("#tab-relatorio").querySelector("div.active").id,
            filter: filter
        },
    };

    fetch(url, fetchOptions).then(
        (response) => {
            response.json().then(c)
        }
    )
}

function get_csrf() {
    cookies = document.cookie
    return cookies.split("csrftoken=")[1].split(";")[0]
}


const myChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels : ["06 Ago", "13 Ago", "20 Ago", "27 Ago", "03 Set"],
        datasets: [
            new Receitas([0.1, 0.5]),
            new Despesas([0.14, 0.6])
        ]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

function render() {

}

function main() {
    let tela = document.querySelector(".container-box-relatorio")
    tela.addEventListener("change", render);
}

main()