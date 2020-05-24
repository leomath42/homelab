function getLogin(){

}

function getPassword(){

}
function getCookie(name){
    const cookie = document.cookie;
    list = document.cookie.split(";") // [1].replace(/\\054/g,",").split("usuario=")[1]
    var aux = "";
    for(i in list){
        var obj = list[i];
        obj = obj.replace(/\ /, "");
        if(obj.startsWith(name+"=")){
            // obj = obj.replace(name+"=", "");
            // obj = obj.replace(/\\054/g,",");
            // obj = obj.replace(/\"/g, "")
            // // obj = obj.replace(/\\/g, "\"");
            // obj = obj.replace(/\\/g, "\"");
            // aux = JSON.parse(obj);
            // break;
            // obj = obj.replace(/\\'/g, "\\'");
            // obj = obj.replace(/\\"/g, '\\"');
            // obj = obj.replace(/\\&/g, "\\&");
            // obj = obj.replace(/\\r/g, "\\r");
            // obj = obj.replace(/\\t/g, "\\t");
            // obj = obj.replace(/\\b/g, "\\b");
            // obj = obj.replace(/\\f/g, "\\f");
            // aux = JSON.parse(obj);
            // break;
            obj = obj.replace(name+"=", "");
            obj = obj.replace(/\\054/g,",");
             obj = obj.replace(/\\""/g, "\"");
            // obj = obj.replace(/\\/g, " ");
            // obj = obj.replace(/\ /g, "\"");
            // obj = obj.replace(/\\/g, "\"");  
            aux = JSON.parse(obj);
            aux = aux.replace(/\\/g, "\\\\");
            aux = JSON.parse(aux);
            break;
        }
    }
    // x.replace(/\\/g, "\"")
    // "{"login":"admin","nome":"admin"}"
    // x = x.replace(/\\/g, "\"")
    // "{"login":"admin","nome":"admin"}"
    // JSON.parse(x)
    return aux;
}

function sair(){
//    var data = $("")
    var data = "sair";
    $.post('/home/commands', {"data": data}, function(data){
//        alert(data);
        window.location = '/';
    });
};

function usuario(){
    var data = "usuario";
    $.post('/home/commands', {"data":data}, function(data){
        $data = $(data);
        $("main").replaceWith($data.filter("main"));
    });
}

function folder(){
    var data = "folder";
    $.post('/home/commands', {"data":data}, function(data){
         $data = $(data);
         $("main").replaceWith($data.filter("main"));
    });
}

function update_usuario(){
    var data = "update_usuario";
    var usuario = getCookie("usuario");
    var login = $("#input-login").val()
    var nome = $("#input-nome").val()
    var email = $("#input-email").val()
    var senha = $("#input-senha").val()
    var info = {data, 'id':usuario.id, login, nome, email, senha}
    $.post('/home/commands', info, function(data){
        //nothing to do for while;
        location.replace("/")
    });
}