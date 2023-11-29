const formElement = document.getElementById('edit-user');

if(formElement){
document.addEventListener('DOMContentLoaded', function () {
    var maxlength = 160;
    const profileBioTextarea = document.getElementById('id_profile_bio');
    const charCountDisplay = document.createElement('div');

    charCountDisplay.style.position = 'absolute';
    charCountDisplay.style.bottom = '0';
    charCountDisplay.style.right = '10px';
    charCountDisplay.style.color = '#666';
    charCountDisplay.style.fontSize = '12px';

    profileBioTextarea.addEventListener('input', function () {
        const charCount = this.value.length;
        charCountDisplay.textContent = charCount + ' / 160';
        if(charCount > maxlength){
            profileBioTextarea.style.border = "5px solid #ff2851";
            charCountDisplay.style.color = '#ff2851';
        }
        else{
            profileBioTextarea.style.border = "1px solid #ced4da";
            charCountDisplay.style.color = '#666';
        }
    });

    profileBioTextarea.parentNode.appendChild(charCountDisplay);
});}