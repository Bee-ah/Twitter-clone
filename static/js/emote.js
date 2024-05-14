const addEmoji = (e , container_name) => {
  
    const emoji = e.native;
  
    const textarea = document.querySelector("."+container_name+" textarea");
    console.log("."+container_name+" textarea");
    textarea.value += emoji;

};
function createEmojiPicker(container , container_name) {

  const pickerOptions = { onEmojiSelect: (e)=>addEmoji(e , container_name), set: "twitter", theme: "light" ,  dynamicWidth: true}; // Customize options here
  const picker = new EmojiMart.Picker(pickerOptions);
  container.innerHTML = "";
  container.appendChild(picker);
}

const formElementArea = document.getElementsByClassName('custom-form');
const formElementNav = document.getElementsByClassName('nav-form');
if(formElementNav){
  document.addEventListener("DOMContentLoaded" , function(){
    parente = document.querySelector(".nav-form p")
    const container = parente.parentElement;
    container_names = container.className;
    parente.style.position = "relative"

    const emojiIconNav = document.createElement("i");
    emojiIconNav.classList.add("fa-regular", "fa-face-smile");
    emojiIconNav.style.position = "absolute";
    emojiIconNav.style.bottom = "5px";
    emojiIconNav.style.right = "10px";
    emojiIconNav.style.zIndex = "9";
    emojiIconNav.style.cursor = "pointer";
    //quando o mouse passa por cima
    emojiIconNav.addEventListener("mouseover", function () {
      emojiIconNav.style.color = "red";
    });
    emojiIconNav.addEventListener("mouseout", function () {
      emojiIconNav.style.color = "";
    });



     // click do mouse do nav
     emojiIconNav.addEventListener("click", function () {      
      const emojiContainer = container.querySelector(".emojiContainer");
      emojiContainer.style.display = emojiContainer.style.display === "none" ? "block" : "none";

      if (emojiContainer.style.display === "block") {
        console.log(container_names);
        createEmojiPicker(emojiContainer , container_names);
      }
    });

    //para fechar tabela de emojis quando se clica fora
    document.addEventListener("click", e => {
      const emojiContainer = document.querySelector(".emojiContainer");
      if (emojiContainer.style.display === "block" && !emojiContainer.contains(e.target) && e.target != emojiIconNav) {
        emojiContainer.style.display = "none";
      }
    })
    document.querySelector(".nav-form p textarea").parentNode.appendChild(emojiIconNav);
  });
}

if (formElementArea) {
  document.addEventListener("DOMContentLoaded", function () {
    parente = document.querySelector(".custom-form p");
    const container = parente.parentElement;
    container_name = container.className;
    parente.style.position = "relative"

    const emojiIcon = document.createElement("i");
    emojiIcon.classList.add("fa-regular", "fa-face-smile");
    emojiIcon.style.position = "absolute";
    emojiIcon.style.bottom = "5px";
    emojiIcon.style.right = "10px";
    emojiIcon.style.zIndex = "99";
    emojiIcon.style.cursor = "pointer";

    //quando o mouse passa por cima
    emojiIcon.addEventListener("mouseover", function () {
      emojiIcon.style.color = "red";
    });
    emojiIcon.addEventListener("mouseout", function () {
      emojiIcon.style.color = "";
    });



    // click do mouse
    emojiIcon.addEventListener("click", function () {      
      const emojiPickerContainer = container.querySelector(".emojiPickerContainer");
      emojiPickerContainer.style.display = emojiPickerContainer.style.display === "none" ? "block" : "none";

      if (emojiPickerContainer.style.display === "block") {
        createEmojiPicker(emojiPickerContainer , container_name);
      }
    });

    //para fechar tabela de emojis quando se clica fora
    document.addEventListener("click", e => {
      const emojiPickerContainer = document.querySelector(".emojiPickerContainer");
      if (emojiPickerContainer.style.display === "block" && !emojiPickerContainer.contains(e.target) && e.target != emojiIcon) {
        emojiPickerContainer.style.display = "none";
      }
    })
    document.querySelector(".custom-form p textarea").parentNode.appendChild(emojiIcon);
    
  });

}

