
const opcoes = require("../opcoes");
const banco = require("../banco");

function execute(user,msg) {
    let menu = "BINO CHAT \n \n ";

Object.keys(opcoes.menu).forEach((value) => {
    let element = opcoes.menu[value];
    menu += `*${value}* - ${element.descricao} \n `; 
});

    banco.db[user].stage = 1;

    return ["Olá, Bem vindo ao Bino Chatbot, Sou o Bino, seu assistente Virtual! Escolhar uma de nossas opções.", menu];
}

exports.execute = execute;