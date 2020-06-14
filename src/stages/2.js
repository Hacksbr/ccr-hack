const opcoes = require("../opcoes");
const banco = require("../banco");

function execute(user,msg){

    // if(!opcoes.menu[msg]){

    //     return["Opção invalida, escolha uma opção valida."];
    // }

    // banco.db[user].itens.push(opcoes.menu[msg]);
    banco.db[user].stage = 2;

    return ["Rota de *Ribeirão Preto a São Carlos* esta neste link: \n  https://bityli.com/6p9Ey"];
    
}

exports.execute = execute;