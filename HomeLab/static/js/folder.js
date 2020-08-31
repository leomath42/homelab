function info_file(idFile){
//    alert(idFile);

    $.post("/home/commands", {'data':'info_file', 'id':idFile}, function(data){
        // recupera a tabela.
        table = $("#modal-body").find("p").find("table");

        // trata o button de download e muda href para o local do arquivo.
        var footer = $(".modal-footer")
        // download
        btn_download = $(footer).find("#btn_download");
        link = "/home/"+"download/" + data['path'] + data['nome'] //+ "." + data['tipo'];
        btn_download.attr("href", link);

        // printer file
        var btn_print = $(footer).find("#btn_print");
//        var post_print = ()=> {
//            $.post('/home/print/'+idFile);
//        }
//
//        btn_print.on('click', post_print);
        //btn_print.on('click', ()=>{printer(idFile)});
        // delete
        btn_delete = $(footer).find("#btn_delete");
        link = "delete" + data['path'] + idFile;

        var post_delete = () => {
            $.post(link, '', ()=> {
                folder();
            })
        }
        btn_delete.on('click', post_delete);

        /* eu sei, "this is ugly" */
        str = "";
        for(aux in data){
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
        $.ajax({
            type : "POST",
			data :formData,
			url: "/home/upload",
			processData: false,
            contentType: false,
            success: () =>{
                // recarrega a tela de folder;
                folder();
            }
        })
    });
    document.getElementById('fileUpload').click();
}
function printer(id){
    $.post('/home/commands', {'data':'print', 'id':id}, function(data){
        data = $(data);
        $("main").replaceWith($data.filter("main"));
    });
}

function show_print_content(){
    var print = document.getElementById("printer-content");
    var md = document.getElementById("folder-modal").getElementsByClassName('modal-dialog')[0];
    if(print.style.display == "" || print.style.display == "none"){
        print.style.display = "block";
        md.style.top = "0vh";
    }
    else{
        print.style.display = "none";
        md.style.top = "";
    }
}