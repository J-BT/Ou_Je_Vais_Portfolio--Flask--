/* *************** AJAX ************************************************* */
//Obligé de créer variables globale, sinon .destroy() ne fonctionne pas
let myChart = "";
let myChart2 = "";
let myChart3 = "";
let myChart4 = "";

/**********  Remplissage tableau via /Classement_pays en  GET ***********/

/***************************************************************** */
// Affiche tableau classsment pays en AJAX selon les critres choisis
/***************************************************************** */
$(document).ready(function () {
  $('#critere_classement').change(function () {
    let critere = this.options[this.selectedIndex].value;

    if (this.options[this.selectedIndex].text.includes("elevé") || 
    this.options[this.selectedIndex].text.includes("déprimante")){
      $.ajax({
        url: "/Classement_pays/"+critere+"/decroissant/",
        success: lectureDuJSON
      });
    }//fin if
    else if (this.options[this.selectedIndex].text.includes("faible") || 
    this.options[this.selectedIndex].text.includes("favorable")){
      $.ajax({
        url: "/Classement_pays/"+critere+"/croissant/",
        success: lectureDuJSON
      });
    }//fin else if
  }); //fin $('#critere_classement').change()
});//fin $(document).ready()


// Affiche les données pays dans un tableau
function lectureDuJSON(result) {
  // Si la table n'est pas vide --> on la vide puis reinitialise nb de lignes
  if(document.getElementById("myTable").rows.length > 1){
    $("#myTable > tbody ").empty();
    document.getElementById("myTable").rows.length = 1;
  }
  const blockCharts = document.querySelector("#blockCharts");
  if (blockCharts.style.display != "block"){
    blockCharts.style.display = "block";
  }


  console.log("Résultat de la requête :", result);
  console.log(document.getElementById("myTable").rows.length);
  donneesAPI = result["data"];
  colonnes = result["columns"]
  
  let pays = 0;
  let premiereDestination = "";
  let paysNumero = 1;

  for (pays in donneesAPI) {
    if (paysNumero == 1){
      premiereDestination = donneesAPI[pays][1];
    }
    paysNumero++;
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
  // Puis on change titre du tableau 
  $('.questionPreferencesAJAX').empty();
  $('.questionPreferencesAJAX').text('Les données vous conseillent : ' 
  + premiereDestination);

  displayCountryCharts(premiereDestination);
}//fin lectureDuJSON


/******* (fin)  Remplissage tableau via /Classement_pays en  GET ********/


////////////////////
// Pour plus tard //
////////////////////
/* ******* POST ******** */
/*
(Dans .js)

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

(Dans .html)

<div class="container">
  <form class=""  role="form" id="form_jy_vais">
      <h2 class="form-signin-heading">Please Sign Up</h2>
      
      <input type="email" id="inputUsername" name="username" class="form-control"
      placeholder="Email address" required autofocus>
      
      <input type="password" id="inputPassword" name="password" 
      class="form-control" placeholder="Password" required>       
      
      <button class="btn btn-lg btn-primary btn-block" 
      type="button" id="buttonTest">Register</button>
</form>   
</div>  
*/








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

/************************  fin Anime.js J'y vais **************************/

/************************************************************************* */
/**************************** Display charts ***************************** */
/************************************************************************* */
// ToDo Put it in a separated module 

function displayCountryCharts(premiereDestination){
  $.ajax({
    url: "/Analyse_par_pays/population/"+premiereDestination+"/",
    success: forGraphDisplay
  });

  function forGraphDisplay(result) {
    // On change titre du tableau 
    $('#graphCountry').empty();
    $('#graphCountry').text(premiereDestination);
    
    donneesAPI = result["data"];
    colonnes = result["columns"];

    let countryName = "";
    let dataForGraph = new Array();
    let labelForGraph = new Array();
    let nYear = 1;

    for (year in donneesAPI) {
      if(nYear == 1){
        countryName = donneesAPI[year][1];
      } 
      dataForGraph.push(parseInt(donneesAPI[year][3])); //value
      labelForGraph.push(donneesAPI[year][2].toString()); //year (as label)
      nYear++;
    }
    
    console.log(donneesAPI);
    console.log(countryName);
    /*
    console.log(dataForGraph[0] + "   " + labelForGraph[0]);
    console.log(typeof dataForGraph[0] + "   " + typeof labelForGraph[0]);
    */
    
    let ctx = document.getElementById('myChart').getContext('2d');
    if (myChart != ""){
      myChart.destroy();
    }
    myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labelForGraph,
            datasets: [{
                label: 'Population of '+premiereDestination+'',
                data: dataForGraph,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            legend: {
              position: top,
            },
            title:{
              display: true,
              text: 'Population of '+premiereDestination+''
            },
            scales: {
                y: {
                    beginAtZero: true/*,
                    max: 140000000,
                    min: 100000000*/
                }
            }
        }
    });
    
    $.ajax({
      url: "/Analyse_par_pays/life_expectancy/"+premiereDestination+"/",
      success: forGraphDisplay2
    });

  }//end function forGraphDisplay

  function forGraphDisplay2(result) {
    
    donneesAPI = result["data"];
    colonnes = result["columns"];

    let countryName = "";
    let dataForGraph = new Array();
    let labelForGraph = new Array();
    let nYear = 1;

    for (year in donneesAPI) {
      if(nYear == 1){
        countryName = donneesAPI[year][1];
      } 
      dataForGraph.push(parseInt(donneesAPI[year][3])); //value
      labelForGraph.push(donneesAPI[year][2].toString()); //year (as label)
      nYear++;
    }
    
    console.log(donneesAPI);
    console.log(countryName);
    /*
    console.log(dataForGraph[0] + "   " + labelForGraph[0]);
    console.log(typeof dataForGraph[0] + "   " + typeof labelForGraph[0]);
    */
    
    
    let ctx2 = document.getElementById('myChart2').getContext('2d');
    if (myChart2 != ""){
      myChart2.destroy();
    }
    myChart2 = new Chart(ctx2, {
        type: 'line',
        data: {
            labels: labelForGraph,
            datasets: [{
                label: 'Life Expectancy of '+premiereDestination+'',
                data: dataForGraph,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            legend: {
              position: top,
            },
            title:{
              display: true,
              text: 'Life Expectancy of '+premiereDestination+''
            },
            scales: {
                y: {
                    beginAtZero: true/*,
                    max: 90,
                    min: 60*/
                    
                }
            }
        }
    });
   
    $.ajax({
      url: "/Analyse_par_pays/unemployment_rate/"+premiereDestination+"/",
      success: forGraphDisplay3
    });

  }//end function forGraphDisplay2

  function forGraphDisplay3(result) {
    
    donneesAPI = result["data"];
    colonnes = result["columns"];

    let countryName = "";
    let dataForGraph = new Array();
    let labelForGraph = new Array();
    let nYear = 1;

    for (year in donneesAPI) {
      if(nYear == 1){
        countryName = donneesAPI[year][1];
      } 
      dataForGraph.push(parseInt(donneesAPI[year][3])); //value
      labelForGraph.push(donneesAPI[year][2].toString()); //year (as label)
      nYear++;
    }
    
    console.log(donneesAPI);
    console.log(countryName);
    /*
    console.log(dataForGraph[0] + "   " + labelForGraph[0]);
    console.log(typeof dataForGraph[0] + "   " + typeof labelForGraph[0]);
    */
    
    let ctx3 = document.getElementById('myChart3').getContext('2d');
    if (myChart3 != ""){
      myChart3.destroy();
    }
    myChart3 = new Chart(ctx3, {
        type: 'line',
        data: {
            labels: labelForGraph,
            datasets: [{
                label: 'Unemployment rate of '+premiereDestination+'',
                data: dataForGraph,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            legend: {
              position: top,
            },
            title:{
              display: true,
              text: 'Unemployment rate of '+premiereDestination+''
            },
            scales: {
                y: {
                    beginAtZero: true
                    
                }
            }
        }
    });
   
    $.ajax({
      url: "/Analyse_par_pays/unemployment_rate/BRAZIL/",
      success: forGraphDisplay4
    });
    
  }//end function forGraphDisplay3


  function forGraphDisplay4(result) {
    
    donneesAPI = result["data"];
    colonnes = result["columns"];

    let countryName = "";
    let dataForGraph = new Array();
    let labelForGraph = new Array();
    let nYear = 1;

    for (year in donneesAPI) {
      if(nYear == 1){
        countryName = donneesAPI[year][1];
      } 
      dataForGraph.push(parseInt(donneesAPI[year][3])); //value
      labelForGraph.push(donneesAPI[year][2].toString()); //year (as label)
      nYear++;
    }
    
    console.log(donneesAPI);
    console.log(countryName);
    /*
    console.log(dataForGraph[0] + "   " + labelForGraph[0]);
    console.log(typeof dataForGraph[0] + "   " + typeof labelForGraph[0]);
    */
    
    let ctx4 = document.getElementById('myChart4').getContext('2d');
    if (myChart4 != ""){
      myChart4.destroy();
    }
    myChart4 = new Chart(ctx4, {
        type: 'line',
        data: {
            labels: labelForGraph,
            datasets: [{
                label: 'Unemployment rate of BRAZIL',
                data: dataForGraph,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            legend: {
              position: top,
            },
            title:{
              display: true,
              text: 'Unemployment rate of BRAZIL'
            },
            scales: {
                y: {
                    beginAtZero: true
                    
                }
            }
        }
    });
  }//end function forGraphDisplay4

}//end displayCountryCharts

/************************************************************************* */
/************************* fin  Display charts *************************** */
/************************************************************************* */