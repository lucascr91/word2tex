class Choice{
    constructor(n_laudas, kind_work, grammar, format_general, style, kind_doc){
        this.n_laudas=n_laudas
        this.kind_work=kind_work
        this.grammar=grammar
        this.format_general=format_general
        this.style=style
        this.kind_doc=kind_doc

    }
    page_value(){
        let doc_array=["monographic", "dissertation", "thesis","paper"]
        let add_array=[0,2,4,6]
        let grammar_value= (this.grammar=="yes") ? 5:0
        let fg_value= (this.format_general=="yes") ? 1:0
        let i;
        for (i=0; i<4;) {
            if (this.kind_work==doc_array[i]){
                    return add_array[i] + grammar_value + fg_value
                } else {
                i++
            }
        }
    }
}
    

document.querySelector('.result').innerHTML = "R$ 0,00"

function round(value, decimals) {
    return Number(Math.round(value+'e'+decimals)+'e-'+decimals);
  }

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
        let grammar_choice=document.getElementById("grammar").value
        let f_all=document.getElementById("fix_all").value
        let style_ref=document.getElementById("style_ref").value
        let doc=document.getElementById("doc").value

        let user_selection= new Choice(n_laudas=pages, 
            kind_work=kind,
            grammar=grammar_choice,
            format_general=f_all,
            style=style_ref, 
            kind_doc=doc)
        let laudas=user_selection.n_laudas
        let cost=user_selection.page_value()
        let L= (doc=="msword" || doc=="nothing")? 0:0.2
        let R= (style_ref=="abnt" || style_ref=="nothing")? 0:0.05
        return document.querySelector('.result').innerHTML = "R$" + " " + round(laudas*cost*(1+L)*(1+R),2) + ",00"
    }
}

