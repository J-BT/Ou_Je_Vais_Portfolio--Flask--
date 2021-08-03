/* Fait apparaitre ou non formulaire contact*/

const targetDiv = document.querySelector("#formulaireContact");
document.addEventListener("DOMContentLoaded", afficheFormulaire);

function afficheFormulaire () {
  if (targetDiv.style.display == "none"){
    targetDiv.style.display = "block";
  }
  else{
    targetDiv.style.display = "none";
  }

}
