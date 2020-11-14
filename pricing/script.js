function reset() {
    document.querySelector('.result').innerHTML = "0,00"
}

for (k in fields) {
    console.log(k)
}


function  budget() {
    var kind=document.getElementById("arbeit").value
    var pages=document.getElementById("pages").value
    var grammar=document.getElementById("grammar").value
    var f_ref=document.getElementById("fix_ref").value
    var f_all=document.getElementById("fix_all").value
    var style=document.getElementById("style_ref").value
    var doc=document.getElementById("kind_doc").value

    var fields=[kind,pages, grammar, f_ref, f_all, style, doc]

    if (pages=='' || kind=='') {
        alert("Ao menos 3 campos devem ser preenchidos. Sendo \"Número de laudas\" e \"Tipo de Trabalho\" sempre obrigatórios.")

    } else {
        if (kind=="monographics") {
            document.querySelector('.result').innerHTML = 2*pages
        }
        else if (kind=="dissertation") {
            document.querySelector('.result').innerHTML = 3*pages
        }
        else if (kind=="thesis") {
            document.querySelector('.result').innerHTML = 4*pages
        }
        else if (kind=="article") {
            document.querySelector('.result').innerHTML = 5*pages
        }
        else {
            document.querySelector('.result').innerHTML = "Something goes wrong"
        }
    }
}

