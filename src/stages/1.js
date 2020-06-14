const opcoes = require("../opcoes");
const banco = require("../banco");

function execute(user,msg){

    // if(!opcoes.menu[msg]){

    //     return["Opção invalida, escolha uma opção valida."];
    // }
    banco.db[user].stage = 2;
    // banco.db[user].itens.push(opcoes.menu[msg]);

    return ["Voce escolheu a opção Rotas. \n Informe a rota que voce deseja. \n Ex: *De Cravinhos a Barrinha.*"];
    
}

exports.execute = execute;