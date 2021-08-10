/* *************** AJAX *********************************************** */

$.ajax({
  url: "/Lets_go/country_pop/decroissant",
  success: lectureDuJSON
});



function lectureDuJSON(result) {
  console.log("Résultat de la requête :", result);
  donneesAPI = result["data"];
  colonnes = result["columns"]
  
  let pays = 0;
  /*
  let nom = 0;
  for (colonne in colonnes){
    console.log(colonne[nom]);
  }
  */
  //console.log(colonnes);
  for (pays in donneesAPI){
    //colonnes
    console.log(colonnes[1], colonnes[2], colonnes[3],
      colonnes[4], colonnes[5], colonnes[6]);
    //donnees
    console.log(donneesAPI[pays][1], donneesAPI[pays][2], donneesAPI[pays][3],
        donneesAPI[pays][4],donneesAPI[pays][5],donneesAPI[pays][6]);
    pays++;
  }
}




/* *************** fin AJAX ******************************************* */


/* Navbar fixe */
document.addEventListener("DOMContentLoaded", function(){
    window.addEventListener('scroll', function() {
        if (window.scrollY > 0) {
          document.getElementById('navbar_top').classList.add('fixed-top');
          // add padding top to show content behind navbar
          navbar_height = document.querySelector('.navbar').offsetHeight;
          document.body.style.paddingTop = navbar_height + 'px';
        } else {
          document.getElementById('navbar_top').classList.remove('fixed-top');
           // remove padding top from body
          document.body.style.paddingTop = '0';
        } 
    });
  }); 

/************************  Anime.js J'y vais **************************/

/************  Très grands ecrans  ********************* */
//Avion
let avion = anime({
  targets: '#avionJs',
  translateX: [
    {value: [0, 2500], duration: 3000, delay: 500},
    {value: [2500, 2000], duration: 2000, delay: 200}
  ], 
  translateY: [
    {value: [0], duration: 800, delay: 500},
    {value: [0, -260], duration: 1000, delay: 1500}
  ],
  
  direction: 'normal',
  loop: false,
  easing: 'easeOutSine'/*,
  complete: function() {
    document.querySelector('#avionJs').style.display = 'none';
  },*/
});
  

  //Lettres
  let animation = anime({
  targets: '.letter',
  opacity: 1,
  translateY: 50, 
  rotate: {
    value: 360,
    duration: 1000,
    easing: 'easeInExpo'
  }, 
  scale: anime.stagger([0.7, 1], {from: 'center'}), 
  delay: anime.stagger(100, {start: 1200}), 
  translateX: [-10, 30]
});   

/************  Grands ecrans  ********************* */





/************  Moyens ecrans  ********************* */





/************  Petits ecrans  ********************* */


/************************  fin Anime.js J'y vais **************************/