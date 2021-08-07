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

  /************************  Anine.js J'y vais **************************/
    
//Avion
let avion = anime({
  targets: '#avionJs',
  translateX: [
    {value: [0, 1900], duration: 3000, delay: 1000},
    {value: [1900, 1750], duration: 2000, delay: 200}
  ], 
  translateY: [
    {value: [0], duration: 800, delay: 1500},
    {value: [0, -330], duration: 1000, delay: 1500}
  ],
  /*translateY: [0, -200],*/
  /*delay: 2500,*/
  direction: 'normal',
  loop: false,
  easing: 'easeOutSine'
});
  

  //Lettres
  let animation = anime({
  targets: '.letter',
  opacity: 1,
  translateY: 50, 
  rotate: {
    value: 360,
    duration: 1500,
    easing: 'easeInExpo'
  }, 
  scale: anime.stagger([0.7, 1], {from: 'center'}), 
  delay: anime.stagger(100, {start: 1000}), 
  translateX: [-10, 30]
});   
