var stages = {
    0:{
      descricao: "Boas vindas",
      obj: require("./stages/0"),
    },
    1:{
      descricao: "opcoes",
      obj: require("./stages/1"),
    },
    2:{
      descricao:"rotas",
      obj: require("./stages/2"),
    },
    3:{
      descricao:"saude",
      obj: "arquivo0.js"
    },
    4:{
      descricao:"higienizaçao",
      obj: "arquivo0.js"
    },
    5:{
      descricao:"agradecimento",
      obj: "arquivo0.js"
    },
    6:{
      descricao:"sid",
      obj: "arquivo0.js"
    },
  
  };

  exports.step = stages;