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
        let total = (() => { let r = 0; for (let i = 0; i < data.length; i++) { r += Number(data[i].valor) } return r; })();

        for (let i = 0; i < this.mov_info.length; i++) {
            this.mov_info[i].percentual = (Number(this.mov_info[i].valor) / total)
                .toLocaleString('pt-br', { style: 'percent', minimumFractionDigits: 2 });
        }
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

    brighter_color(color, ratio = 0.1) {
        return color;
    }

    format_date(date) {
        let dia = date.toLocaleString('pt-br', { day: '2-digit' });
        let mes = date.toLocaleString('pt-br', { month: 'short' }).split('.')[0];

        return `${dia} ${mes[0].toUpperCase() + mes.substring(1)}`
    };
}

// Classe usados para configurar cada DataSet das tabelas
class Receitas extends RxD_item {

    constructor(data) {
        super("Receitas", "#129e3f")
        this.set_data(data)
    }
}

// Classe usados para configurar cada DataSet das tabelas
class Despesas extends RxD_item {

    constructor(data) {
        super("Despesas", "#d72638")
        this.set_data(data)
    }
}


// Renderiza o gráfico
function render(data) {
    const context = {
        rece_desp: document.getElementById('graph-rece-desp').getContext('2d'),
        graph_categorias_receitas: document.getElementById('graph-categorias-receitas').getContext('2d'),
        graph_categorias_despesas: document.getElementById('graph-categorias-despesas').getContext('2d'),
    }


    let receitas = new Receitas(data.entradas),
        despesas = new Despesas(data.saidas),
        cat_receitas = new Receitas(data.categorias.receitas),
        cat_despesas = new Despesas(data.categorias.despesas);

    const tooltip_callbacks = {
        title: function (context_li) {
            let context = context_li[0];
            return context.dataset.mov_info[context.dataIndex].titulo;
        },
        label: function (context) {
            let prcnt_str = "Percentual: " +
                `${context.dataset.mov_info[context.dataIndex].percentual
                    .toLocaleString('pt-br', { style: 'percent', minimumFractionDigits: 2 })}`;

            return prcnt_str;
        }
    }

    const instances = {}
    let active_context;
    Chart.helpers.each(Chart.instances, function(instance){
        instances[instance.canvas.id] = instance;
    });
    
    active_context = instances[context.rece_desp.canvas.id]
    if (active_context) { 
        active_context.data = {
            labels: receitas.map_bar_xaxis(),
            datasets: [receitas.map_bar_yaxis(), despesas.map_bar_yaxis()]
        };
        active_context.update();
    }
    else { 
        new Chart(context.rece_desp, {
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
    }


    active_context = instances[context.graph_categorias_receitas.canvas.id]
    if (active_context) { 
        active_context.data.datasets = [
            cat_receitas.map_doughnut_yaxis()];
        active_context.update();
    }
    else { 
        new Chart(context.graph_categorias_receitas, {
            type: 'doughnut',
            data: { datasets:  [cat_receitas.map_doughnut_yaxis()]},
            options: {
                plugins: {
                    legend: {
                        title: {
                            display: true,
                            text: cat_receitas.label,
                            font: {
                                size: "20px",
                                weight: '500',
                                family: "Ruda, sans-serif",
                            }
                        },
                    },
                    tooltip: {
                        callbacks: tooltip_callbacks
                    },
                }
            }
        });
    }

    active_context = instances[context.graph_categorias_despesas.canvas.id]
    if (active_context) {
        active_context.data.datasets = [
            cat_despesas.map_doughnut_yaxis()];
        active_context.update();
    }
    else {
        new Chart(context.graph_categorias_despesas, {
            type: 'doughnut',
            data: { datasets: [cat_despesas.map_doughnut_yaxis()] },
            options: {
                plugins: {
                    legend: {
                        title: {
                            display: true,
                            text: cat_despesas.label,
                            font: {
                                size: "20px",
                                weight: '500',
                                family: "Ruda, sans-serif",
                            }
                        }
                    },
                    tooltip: {
                        callbacks: tooltip_callbacks
                    },
                }
            }
        })
    }

}


// Base para os geradores de cada tabela
class table_base {
    data = [];
    format = {};
    n_rows = 0;
    style = {
        neg: "#d72638",
        pos: "#129e3f",
    }

    constructor(n_rows, color = undefined) {
        this.n_rows = n_rows;

        if (color) {
            this.style = color;
        }
    }

    create_row(format, data) {
        let tr = document.createElement("tr");
        tr.role = "row";

        for (let i = 0; i < this.n_rows; i++) {
            let td = document.createElement("td");
            let f_data = format[`i${i}`](data);

            if (f_data.style) {
                td.style = f_data.style;
            }
            td.textContent = f_data.value


            tr.appendChild(td);
        }

        return tr;
    }

    create_table(table, dataIndex = undefined) {
        if (dataIndex) {
            for (let i = 0; i < this.data[dataIndex].length; i++) {
                table.tBodies[0].appendChild(this.create_row(this.format, this.data[dataIndex][i]));
            }
        }
        else {
            for (let i = 0; i < this.data.length; i++) {
                table.tBodies[0].appendChild(this.create_row(this.format, this.data[i]));
            }
        }
    }

    clear_table(table) { 
        table.removeChild(table.tBodies[0]);
        table.appendChild(document.createElement('tbody'));
    }

    create_footer(table, dataIndex = undefined) {
        table.tFoot = document.createElement("tfoot");
        if (dataIndex) {
            table.tFoot.appendChild(this.create_row(this.format, this.data.footer[dataIndex]));
        }
        else {
            table.tFoot.appendChild(this.create_row(this.format, this.data.footer));
        }
        table.tFoot.firstChild.firstChild.style.textAlign = "left";
        table.tFoot.firstChild.lastChild.style.textAlign = "right";
    }

    format_date(date) {
        let dia = date.toLocaleString('pt-br', { day: '2-digit' });
        let mes = date.toLocaleString('pt-br', { month: 'short' }).split('.')[0];

        return `${dia} ${mes[0].toUpperCase() + mes.substring(1)}`;
    }

    format_number(n) {
        return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(n.toFixed(2));
    }

    format_number_pct(n) {
        return (n).toLocaleString('pt-br', { style: 'percent', minimumFractionDigits: 2 });
    }
}

// Classa usada para configurar DataSet da table "Detalhamento"
class table_detalhamento extends table_base {
    constructor(data) {
        super(4)
        this.set_data(data);
        this.set_format();
    }


    set_data(data) {
        let receitas = data.entradas,
            despesas = data.saidas;

        let i;
        for (i = 0; i < receitas.length; i++) {
            let n_data = {};
            n_data.data = receitas[i].data;
            n_data.entrada = Number(receitas[i].valor);
            n_data.saida = -1 * Number(despesas[i].valor);
            n_data.valor = n_data.entrada + n_data.saida;

            this.data.push(n_data);
        }

        this.data.footer = [];
        return this;
    }

    set_format() {

        let format = function () { };

        format.i0 = function (data) {
            let ini, fim;
            ini = this.format_date(new Date(data.data[0]));
            fim = this.format_date(new Date(data.data[1]));

            return { value: `${ini} à ${fim}` };
        };
        format.i1 = function (data) {
            let out = {};
            out.value = this.format_number(data.entrada);

            return out;
        };
        format.i2 = function (data) {
            let out = {};
            out.value = this.format_number(data.saida);
            if (data.saida != 0) {
                out.style = `color:${(data.saida < 0) ? this.color.neg : this.color.pos}`;
            }

            return out;
        };
        format.i3 = function (data) {
            let out = {};
            out.value = this.format_number(data.valor);
            if (data.valor != 0) {
                out.style = `color:${(data.valor < 0) ? this.color.neg : this.color.pos}`;
            }

            return out;
        };
        format.format_date = this.format_date;
        format.format_number = this.format_number;
        format.color = this.style;
        this.format = format;

        return this;
    }
}

// Classa usada para configurar DataSet da table "Receitas" e "Despesas" em "Categorias"
class table_categorias extends table_base {
    constructor(data) {
        super(3)
        this.set_data(data);
        this.set_format();
    }

    set_data(data) {
        let receitas = data.categorias.receitas,
            despesas = data.categorias.despesas;
        let i;

        this.data.receitas = [];
        this.data.despesas = [];

        let total_receitas = (() => { let r = 0; for (i = 0; i < receitas.length; i++) { r += Number(receitas[i].valor) } return r; })(),
            total_despesas = (() => { let r = 0; for (i = 0; i < despesas.length; i++) { r += Number(despesas[i].valor) } return r; })();

        for (i = 0; i < receitas.length; i++) {
            let n_data = {};
            n_data.titulo = receitas[i].titulo;
            n_data.valor = Number(receitas[i].valor);
            n_data.percentual = n_data.valor / total_receitas;

            this.data.receitas.push(n_data);
        }

        for (i = 0; i < despesas.length; i++) {
            let n_data = {};
            n_data.titulo = despesas[i].titulo;
            n_data.valor = -1 * Number(despesas[i].valor);
            n_data.percentual = -1 * n_data.valor / total_despesas;

            this.data.despesas.push(n_data);
        }

        this.data.footer = {
            receitas: {
                titulo: "Total",
                valor: total_receitas,
            },
            despesas: {
                titulo: "Total",
                valor: -1 * total_despesas,
            }
        }
        return this;
    }

    set_format() {

        let format = function () { };

        format.i0 = function (data) {
            return { value: data.titulo };
        };
        format.i1 = function (data) {
            let out = {};
            if (data.percentual) {
                out.value = this.format_number_pct(data.percentual);
            }

            return out;
        };
        format.i2 = function (data) {
            let out = {};
            out.value = this.format_number(data.valor);
            if (data.valor != 0) {
                out.style = `color:${(data.valor < 0) ? this.color.neg : this.color.pos}`;
            }

            return out;
        };
        format.format_number = this.format_number;
        format.format_number_pct = this.format_number_pct;
        format.color = this.style;
        this.format = format;

        return this;
    }
}

// Renderiza a tabela
function table_render(data) {
    let query = document.querySelectorAll("#receitas-table"),
        t_det = new table_detalhamento(data),
        t_cat = new table_categorias(data);

    const table_det = query[0],
        table_cat_receitas = query[1],
        table_cat_despesas = query[2];

    t_det.clear_table(table_det);
    t_det.create_table(table_det);

    [[table_cat_receitas, "receitas"], [table_cat_despesas, "despesas"]].forEach((value) => {
        t_cat.clear_table(value[0])
        t_cat.create_table(value[0], value[1]);
        t_cat.create_footer(value[0], value[1]);
    })


}


function relatorio_response_handler(json) {

    if(json.status == 200) {
        render(json.result);
        table_render(json.result);
    }
    else {
        alert("Ocorreu um erro: " + json.error)
    }

    return false
}