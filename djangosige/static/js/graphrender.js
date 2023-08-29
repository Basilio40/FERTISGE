const test_data = {
    entradas: [
        {
            data: ["2023-08-06", "2023-08-12",],
            titulo: "Entradas genérica 1",
            valor: "1000.00",
            saldo_final: "0.0",
        },
        {
            data: ["2023-08-13", "2023-08-19"],
            titulo: "Entradas genérica 2",
            valor: "2000.00",
            saldo_final: "0.0",
        },
        {
            data: ["2023-08-20", "2023-08-26"],
            titulo: "Entradas genérica 3",
            valor: "3000.00",
            saldo_final: "0.0",
        },
        {
            data: ["2023-08-27", "2023-09-02"],
            titulo: "Entradas genérica 4",
            valor: "4000.00",
            saldo_final: "0.0",
        },
        {
            data: ["2023-09-03", "2023-09-10"],
            titulo: "Entradas genérica 5",
            valor: "5000.00",
            saldo_final: "0.0",
        },
    ],
    saidas: [
        {
            data: ["2023-08-06", "2023-08-12",],
            titulo: "Despesa genérica 1",
            valor: "-1000.00",
            saldo_final: "0.0",
        },
        {
            data: ["2023-08-13", "2023-08-19"],
            titulo: "Despesa genérica 2",
            valor: "-2000.00",
            saldo_final: "0.0",
        },
        {
            data: ["2023-08-20", "2023-08-26"],
            titulo: "Despesa genérica 3",
            valor: "-3000.00",
            saldo_final: "0.0",
        },
        {
            data: ["2023-08-27", "2023-09-02"],
            titulo: "Despesa genérica 4",
            valor: "-4000.00",
            saldo_final: "0.0",
        },
        {
            data: ["2023-09-03", "2023-09-10"],
            titulo: "Despesa genérica 5",
            valor: "-5000.00",
            saldo_final: "0.0",
        },
    ],
};

// Manipulador para configurar os dados para cada tipo de gráfico
class RxD_item {
    borderWidth = 0;
    mov_info = [];
    data = [];

    constructor(label, bgcolor) {
        this.label = label;
        this.backgroundColor = bgcolor;
    }

    set_data(data) {
        this.mov_info = data;
        return this;
    }

    map_doughnut_yaxis() {
        this.data = [];

        for (let i = 0; i < this.mov_info.length; i++) {
            this.data.push(this.mov_info[i].valor);
        }

        this.borderWidth = 1;
        this.hoverOffset = 10;

        return this;
    }

    map_doughnut_xaxis() {
        let out = [];
        
        for (let i = 0; i < this.mov_info.length; i++) {
            out.push(this.mov_info[i].titulo);
        }

        return out;
    }

    map_bar_yaxis() {
        this.data = [];

        for (let i = 0; i < this.mov_info.length; i++) {
            this.data.push({
                x: this.format_date(new Date(this.mov_info[i].data[0])),
                y: this.mov_info[i].valor,
            });
        }

        return this;
    }

    map_bar_xaxis() {
        let out = [];
        
        for (let i = 0; i < this.mov_info.length; i++) {
            out.push(this.format_date(new Date(this.mov_info[i].data[0])));
        }

        return out;
    }

    brighter_color(color, ratio=0.1) {
        return color;
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

function response_handler(json) {
    
}

// Renderiza o gráfico
function render(data) {
    const context = {
        rece_desp: document.getElementById('graph-rece-desp').getContext('2d'),
        graph_categorias_receitas: document.getElementById('graph-categorias-receitas').getContext('2d'),
        graph_categorias_despesas: document.getElementById('graph-categorias-despesas').getContext('2d'),
    }
    

    const receitas = new Receitas(data.entradas)
    const despesas = new Despesas(data.saidas)
    const default_options = (obj) => {

    }

    const bar_graph_financeiro = new Chart(context.rece_desp, {
        type: 'bar',
        data: {
            labels: receitas.map_bar_xaxis(),
            datasets: [receitas.map_bar_yaxis(), despesas.map_bar_yaxis()]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    display: false, // Isso esconde o eixo Y
                }
            },
        }
    });

    const doughnut_graph_financeiro_r = new Chart(context.graph_categorias_receitas,  {
        type: 'doughnut',
        data: { datasets: [receitas.map_doughnut_yaxis()] },
        options: {
            plugins: {
                legend: {
                    title: {
                        display: true,
                        text: receitas.label,
                        font: {
                            size: "20px",
                            weight: '500',
                            family: "Ruda, sans-serif",
                        }
                    }
                }
            }
        }
    })

    const doughnut_graph_financeiro_d = new Chart(context.graph_categorias_despesas,  {
        type: 'doughnut',
        data: { datasets: [despesas.map_doughnut_yaxis()] },
        options: {
            plugins: {
                legend: {
                    title: {
                        display: true,
                        text: despesas.label,
                        font: {
                            size: "20px",
                            weight: '500',
                            family: "Ruda, sans-serif",
                        }
                    }
                }
            }
        }
    })
}


class table_base {
    data = [];
    n_rows = 0;
    style = {
        neg: "#d72638",
        pos: "#129e3f",
    }

    constructor(n_rows, color=undefined) {
        this.data = this.set_data(data);
        this.n_rows = n_rows;
        
        if (color) {
            this.style = color;
        }
    }

    set_data(data) {
        self.data = data;
        return this;
    }

    create_row(format, data) {
        let tr = document.createElement("tr");
        for (let i = 0; i < this.n_rows; i++) {
            let td = document.createElement("td");
            let f_data = format[i](data);
            
            if (f_data.style) {
                td.style = f_data.style;
            }
            td.textContent = f_data.out

            tr.appendChild(td);
        }

        return tr
    }

    format_date(date) {
        let dia = date.toLocaleString('pt-br', { day: '2-digit' });
        let mes = date.toLocaleString('pt-br', {month: 'short'}).split('.')[0];

        return `${dia} ${mes[0].toUpperCase() + mes.substring(1)}`
    };
}

class table_detalhamento extends table_base{

    format = {
        0: function (data) {
            let ini = this.format_date(new Date(data[0])),
            fim = this.format_date(new Date(data[1]));

            return {out: `${ini} à ${fim}`};
        },
        1: function (data) {
            let out = {};
            out.out = data.entrada;
            out.style = `color:${(out.out < 0)? this.color.neg : this.color.pos}`;

            return out;
        },
        2: function (data) {
            let out = {};
            out.out = data.saida;
            out.style = `color:${(out.out < 0)? this.color.neg : this.color.pos}`;

            return out;
        },  
        4: function (data) {
            let out = {};
            out.out = data.valor
            out.style = `color:${(out.out < 0)? this.color.neg : this.color.pos}`;
            
            return out;
        },
    }

    constructor() {
        super(4)
    }

    create_table(table) {
        for( let i = 0; i < this.data.length; i++) {
            table.tBodies[0].appendChild(this.create_row(this.format, this.data[i]));
        }
    }

}

class table_categorias extends table_base{
    format = {
        0: function (data) {
            return data.title
        },
        1: function (data) {
            return data.entrada
        },
        2: function (data) {
            return data.saida
        },  
        4: function (data) {
            return data.total
        },
        5: function (data) {
            return data
        },
    }
    constructor(data){
        super(4, "#d72638")
    }
}



// Renderiza a tabela
function table_render(data) {

    const table = document.querySelector("#receitas-table");
    
    let tr = document.createElement("tr")
    tr.role = "row"

    for (let i = 0; i < 4; i++) {
        let td = document.createElement("td");
        td.textContent = i;
        tr.appendChild(td);
    }

    table.tBodies[0].appendChild(tr);
}

function main() {
    render(test_data)
    //table_render(test_data)
}

main()