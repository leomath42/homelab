function info_file(idFile){
//    alert(idFile);

    $.post("/home/commands", {'data':'info_file', 'id':idFile}, function(data){
        // recupera a tabela.
        table = $("#modal-body").find("p").find("table");

        // trata o button de download e muda href para o local do arquivo.
        btn_download = $(".modal-footer").find("#btn_download");
        link = "download/" + data['path'] + data['nome'] //+ "." + data['tipo'];
        btn_download.attr("href", link);

        /* eu sei, "this is ugly" */
        str = "";
        for(aux in data){
//            if(aux == "nome"){
//                str+=format_table(aux, data[aux]+"."+data['tipo']);
//            }
//            else if (aux == "path" && data['path'] === ""){
//                str+=format_table(aux, "/");
//            }
            if(aux != "id"){
                str+=format_table(aux, data[aux]);
            }
        }

        // muda o html da tabela.
        table.html(str);

    });

    var modal = $(".modal");
    modal.css("display", "block");

    function close(){
        modal.css("display", "none");
        window.onclick = null;
    }
    window.onclick = function(event) {
        if (event.target == modal[0]) {
            close();
        }
    }
    var close_button_1 = modal.find("#close_1")[0];
    var close_button_2 = modal.find("#close_2")[0];
    close_button_1.onclick = function(e){close()};
    close_button_2.onclick = function(e){close()};
}
function format_table(str1, str2){
    str = "<tr><th class='w-50'>" + str1 + "</th><td class='w-50'>" + str2 + "</td></tr>";
    return str;
}

function file_upload(file){
    file = document.getElementById(file);
    file.addEventListener('change', function(){
        var formData = new FormData($("form").get(0));
//        $.post("/home/commands", formData, processData:false, contentType:false, function(e){
//            alert("teste");
//        });
//        alert("teste")
        $.ajax({
            type : "POST",
			data :formData,
			url: "/home/upload",
			processData: false,
            contentType: false
        })
    });
    document.getElementById('fileUpload').click();
}