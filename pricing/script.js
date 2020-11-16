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
        let i;
        for (i=0; i<4;) {
            if (this.kind_work==doc_array[i]){
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



function reset() {
    document.querySelector('.result').innerHTML = "R$ 0,00"
    pages=document.getElementById("pages").value="---"
    kind=document.getElementById("work").value="---"
}

function  budget() {
    let pages=document.getElementById("pages").value
    let kind=document.getElementById("work").value
    if (isNaN(parseInt(pages)) || kind=='') {
        alert("Ao menos 3 campos devem ser preenchidos. Sendo \"Número de laudas\" e \"Tipo de Trabalho\" sempre obrigatórios.")

    } else {
        let grammar=document.getElementById("grammar").value
        let f_ref=document.getElementById("fix_ref").value
        let style_ref=document.getElementById("style_ref").value

        let user_selection= new Choice(n_laudas=pages, 
            kind_work=kind,grammar=false,format_general=false,
            format_ref=f_ref, style=false)
        let laudas=user_selection.n_laudas
        let cost=user_selection.page_value()
        return document.querySelector('.result').innerHTML = "R$" + " " + laudas*cost + ",00"
    }
}

