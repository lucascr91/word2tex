class Budget {
    constructor(pages, kind, grammar, f_ref, f_all, style) {
        this.pages=pages
        this.kind=kind
        this.grammar=grammar
        this.f_ref=f_ref
        this.f_all=f_all
        this.style=style
        this.clear()
    }

    clear() {
        this.result = ''
    }

    compute () {

    }
}

var user_pages=document.getElementById("pages").value
var user_kind=document.getElementById("pages").value
var user_grammar=document.getElementById("pages").value
var user_fref=document.getElementById("pages").value
var user_fall=document.getElementById("pages").value
var user_style=document.getElementById("pages").value


