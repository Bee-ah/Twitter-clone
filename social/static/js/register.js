function validaEmail(elemento){

    elemento.addEventListener('focusout', function(event) {

        event.preventDefault();
        
        const emailValido = /^[a-z0-9.]+@[a-z0-9]+\.[a-z]+(\.[a-z]+)?/i;
        //notação com construtor: ideal quando o padrão é mudado, ou quando não se sabe o padrão
        
        if(this.value.match(emailValido)) { 
            document.querySelector('.mensagem').innerHTML = "";
            this.classList.remove('erro');
            this.parentNode.classList.remove('erro');
        } else { 
            document.querySelector('.mensagem').innerHTML = "verifique o preenchimento dos campos em destaque";
            this.classList.add('erro');
            this.parentNode.classList.add('erro');
            return false;
        }

    });

}

let camposEmail = document.querySelectorAll('input.email');

for( let emFoco of camposEmail) {
    validaEmail(emFoco);
}