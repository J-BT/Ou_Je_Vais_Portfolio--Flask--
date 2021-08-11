/* *************** AJAX ************************************************* */
/* ******** SELECTEUR ***** */

$(document).ready(function () {
 

    // SHOW SELECTED VALUE.
    $('#sel').change(function () {
      $('#msg').text('Selected Item: ' + this.options[this.selectedIndex].text);
      console.log(this.options[this.selectedIndex].text);
    }); 


  
});





/* ******* POST ******** */
$(function(){
	$('#buttonTest').click(function(){
		var user = $('#inputUsername').val();
		var pass = $('#inputPassword').val();
		$.ajax({
			url: '/Jy_vais_DATA',
			data: $('#form_jy_vais').serialize(),
			type: 'POST',
			success: function(response){
				console.log(response);
			},
			error: function(error){
				console.log(error);
			}
		});
	});
});


/* ******* GET ******** */
$(document).ready(function(){
  $(".testBouton").click(function(){
    if(document.getElementById("myTable").rows.length == 1){
      $.ajax({
        url: "/Lets_go",
        success: lectureDuJSON
      });
    }//fin du if
    else{
      $("#myTable > tbody ").empty();
      document.getElementById("myTable").rows.length = 1;
    }
  });

});



// Affiche les données pays dans un tableau
function lectureDuJSON(result) {
  console.log("Résultat de la requête :", result);
  donneesAPI = result["data"];
  colonnes = result["columns"]
  
  let pays = 0;
 
  for (pays in donneesAPI) {
    let row = $(
      '<tr><td>' + donneesAPI[pays][1] + '</td><td>'
                 + donneesAPI[pays][2] + '</td><td>' 
                 + donneesAPI[pays][3] + '</td><td>' 
                 + donneesAPI[pays][4] + '</td><td>' 
                 + donneesAPI[pays][5] + '</td><td>'
                 + donneesAPI[pays][6] + '</td><td>' 
                 + donneesAPI[pays][7] + '</td></tr>');
    $('#myTable').append(row);
  }
}


/* *************** fin AJAX ********************************************* */


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