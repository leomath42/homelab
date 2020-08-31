function select_connect_type(){
    var connect_type = document.getElementById("connect_type");
    var option = connect_type.options[connect_type.selectedIndex];

    var lan_address= document.getElementById("lan-address");
    var lan_port = document.getElementById("lan-port");
    var serial = document.getElementById("serial");

    if (option.value == "lan"){
        lan_address.style.display = "block";
        lan_port.style.display = "block";
        serial.style.display = "none";
    }
    else if(option.value == "serial"){
        lan_address.style.display = "none";
        lan_port.style.display = "none";
        serial.style.display = "block";
    }
    return "";
}