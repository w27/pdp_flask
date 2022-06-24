let access_token = ""

function courses() {
    var url = "/courses";

    var xhr = new XMLHttpRequest();
    xhr.open("GET", url);

    xhr.setRequestHeader("Accept", "application/json");
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.setRequestHeader("Authorization", `Bearer ${access_token}`);

    xhr.onreadystatechange = function () {
    if (xhr.readyState === 4) {
        let res = xhr.responseText

        main = document.getElementById("body");
        var p =  JSON.parse(res)["course list"]
        var buf = "<ul>"
        for(var k in p) {
            buf += "<li>" + p[k]["name"] + "</li>"
        }
        buf += "</ul>"
        main.innerHTML = `
        <h1>
            ${buf}
        </h1>`

    }};
     
    xhr.send();
}

function menu() {
    main = document.getElementById("main");
    main.innerHTML = `
    <ul>
        <li><a href="#" onclick="courses();">Список курсов</a></li>
        <li>Список студентов</li>
    </ul>`

}


function login() {

    var url = "/auth";

    var xhr = new XMLHttpRequest();
    xhr.open("POST", url);

    xhr.setRequestHeader("Accept", "application/json");
    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.onreadystatechange = function () {
    if (xhr.readyState === 4) {
        let res = xhr.responseText
        if (JSON.stringify(res).indexOf("access_token") != -1) {
            access_token = JSON.parse(res)['access_token'];
            menu();
        } else {
            console.log("Error accept");
            main = document.getElementById("body");
            main.innerHTML = `
            <h1>
                Login Error
            </h1>`
        }
    }};

    var data = `{
                    "username": "${document.getElementById("login").value}",
                    "password": "${document.getElementById("password").value}"
                }`;
      
    xhr.send(data);
}

