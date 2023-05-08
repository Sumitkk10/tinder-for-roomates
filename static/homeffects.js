const text = "Find your perfect roommate."; 
const delay = 100; 

let i = 0;
function type() {
  if (i < text.length) {
    document.getElementById("text").innerHTML += text.charAt(i);
    i++;
    setTimeout(type, delay);
  }
}
type();

const images = [
  "../static/img/roomies.jpg",
  "../static/img/roomies2.jpg",
  "../static/img/roomies3.jpg",
  "../static/img/roomies4.jpg",
  "../static/img/roomies5.jpg",
  "../static/img/roomies6.jpg",
];
const intervalTime = 5000;
const img = document.querySelector('#bg-image');
img.style.backgroundImage = `url(${images[0]})`;
let index = 1;
function changeImage() {
  img.style.backgroundImage = `url(${images[index]})`;
  index = (index + 1) % images.length;
}
setInterval(changeImage, intervalTime);
