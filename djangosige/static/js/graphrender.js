// Manipulador para configurar os dados para cada tipo de gráfico
class RxD_item {
    borderWidth = 0;
    data = [];

    constructor(label, bgcolor) {
        this.label = label;
        this.backgroundColor = bgcolor;
    }

    set_data(data) {
        this.data = data
        return this
    }

    get_pie_data() {
        let out = []

        for (let i = 0; i < this.data.length; i++) {
            out.push({
                value: this.data[i].valor,
                highlight: this.brighter_color(this.color),
                date: this.format_date(new Date(this.data[i].data))
            })
        }

        return out;
    }

    get_bar_data() {
        return this
    }

    brighter_color(color, ratio=0.1) {
        return color
    }

    format_date(date) {
        let dia = date.toLocaleString('pt-br', { day: '2-digit' });
        let mes = date.toLocaleString('pt-br', {month: 'short'}).split('.')[0];

        return `${dia} ${mes[0].toUpperCase() + mes.substring(1)}`
    };
}

// Classe usados para configurar cada DataSet das tabelas
class Receitas extends RxD_item{

    constructor(data) {
        super("Receitas", "#129e3f")
        this.set_data(data)
    }
}

// Classe usados para configurar cada DataSet das tabelas
class Despesas extends RxD_item{

    constructor(data) {
        super("Despesas", "#d72638")
        this.set_data(data)
    }
}

// Retorna chave de segurança para interações com o backend
function get_csrf() {
    cookies = document.cookie
    return cookies.split("csrftoken=")[1].split(";")[0]
}

// Coleta as informações necessário no banco e constroi os gráficos e tabelas
function get_data(filter) {
    url = "/financeiro/lancamentos/graphdata/"

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

function response_handler(json) {
    
}

const test_data = {
    entradas: [
        {
            data: "2023-08-06",
            titulo: "Entradas genérica 1",
            valor: "1000.00",
            saldo_final: "0.0",
        },
        {
            data: "2023-08-13",
            titulo: "Entradas genérica 2",
            valor: "2000.00",
            saldo_final: "0.0",
        },
        {
            data: "2023-08-20",
            titulo: "Entradas genérica 3",
            valor: "3000.00",
            saldo_final: "0.0",
        },
        {
            data: "2023-08-27",
            titulo: "Entradas genérica 4",
            valor: "4000.00",
            saldo_final: "0.0",
        },
        {
            data: "2023-09-03",
            titulo: "Entradas genérica 5",
            valor: "5000.00",
            saldo_final: "0.0",
        },
    ],
    saidas: [
        {
            data: "2023-08-06",
            titulo: "Despesa genérica 1",
            valor: "1000.00",
            saldo_final: "0.0",
        },
        {
            data: "2023-08-13",
            titulo: "Despesa genérica 2",
            valor: "2000.00",
            saldo_final: "0.0",
        },
        {
            data: "2023-08-20",
            titulo: "Despesa genérica 3",
            valor: "3000.00",
            saldo_final: "0.0",
        },
        {
            data: "2023-08-27",
            titulo: "Despesa genérica 4",
            valor: "4000.00",
            saldo_final: "0.0",
        },
        {
            data: "2023-09-03",
            titulo: "Despesa genérica 5",
            valor: "5000.00",
            saldo_final: "0.0",
        },
    ],
};

// Renderiza o gráfico
function render(data) {
    const ctx = document.getElementById('graph-rece-desp').getContext('2d');
    const receitas = new Receitas(data.entradas)
    const despesas = new Despesas(data.saidas)
    const bar_graph_financeiro = new Chart(ctx, {
        type: 'bar',
        labels: [receitas.label, despesas.label],
        data: {
            datasets: [].concat(receitas.get_pie_data(), despesas.get_pie_data())
        },
        options: {
            parsing: {
                xAxisKey: "date",
                yAxisKey: "value"
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// Renderiza a tabela
function table_render() {

}

function main() {
    render(test_data)
}

main()