class Choice{
    constructor(n_laudas, kind_work, grammar, format_general, format_ref, style, kind_doc){
        this.n_laudas=n_laudas
        this.kind_work=kind_work
        this.grammar=grammar
        this.format_general=format_general
        this.format_ref=format_ref
        this.style=style
        this.kind_doc=kind_doc

    }
    page_value(){
        let doc_array=["monographic", "dissertation", "thesis","paper"]
        let add_array=[0,2,4,6]
        for (i=0; i<4;) {
            if (this.kind_work==doc_array){
                if (this.style==false) {
                    return 6+add_array[i]
                }
                else if (this.style=="abnt") {
                    return 7+add_array[i]
                }
                else if (this.style=="chicago_notes" || this.style=="chicago_author") {
                    return 9+add_array[i]
                }
            } else {
                i++
            }
        }
    }
}

document.querySelector('.result').innerHTML = "R$ 0,00"

let pages=document.getElementById("pages").value
let kind=document.getElementById("work").value
let grammar=document.getElementById("grammar").value
let f_ref=document.getElementById("fix_ref").value
let style_ref=document.getElementById("style_ref").value

function reset() {
    document.querySelector('.result').innerHTML = "R$ 0,00"
    pages=document.getElementById("pages").value="---"
    kind=document.getElementById("arbeit").value="---"
}

function  budget() {
    if (isNaN(parseInt(pages)) || kind=='') {
        alert("Ao menos 3 campos devem ser preenchidos. Sendo \"Número de laudas\" e \"Tipo de Trabalho\" sempre obrigatórios.")

    } else {
        let user_selection= new Choice(n_laudas=pages, 
            kind_work=kind,grammar=false,format_general=false,
            format_ref=f_ref, style=style_ref)

        return user_selection.n_laudas*user_selection.page_value()
    }
}

