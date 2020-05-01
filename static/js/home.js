function getLogin(){

}

function getPassword(){

}

function sair(){
//    var data = $("")
    var data = "sair";
    $.post('/home/commands', {"data": data}, function(data){
//        alert(data);
        window.location = '/';
    });
};