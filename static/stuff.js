const fileInput1 = document.getElementById('file-input1');
const imageContainer1 = document.getElementById('image-container1');
const imageContainer3 = document.getElementById('image-container3');

fileInput1.addEventListener('change', function() {
  const file = this.files[0];
  photo1 = file.name;
  const reader = new FileReader();
  reader.onload = function() {
    const imageDataURL = reader.result;
    imageContainer1.style.backgroundImage = `url(${imageDataURL})`;
    imageContainer1.style.backgroundSize = 'cover';
    imageContainer3.style.backgroundImage = `url(${imageDataURL})`;
    imageContainer3.style.backgroundSize = 'cover';
  }
  reader.readAsDataURL(file);
});

const fileInput2 = document.getElementById('file-input2');
const imageContainer2 = document.getElementById('image-container2');

fileInput2.addEventListener('change', function() {
  const file = this.files[0];
  photo2 = file.name;
  const reader = new FileReader();
  reader.onload = function() {
    const imageDataURL = reader.result;
    imageContainer2.style.backgroundImage = `url(${imageDataURL})`;
    imageContainer2.style.backgroundSize = 'cover';
  }
  reader.readAsDataURL(file);
});

let photo1 = '';
let photo2 = '';

const sendButton = document.querySelector('#send-data');

sendButton.addEventListener('click', () => {

  const xhr = new XMLHttpRequest();
  xhr.open('POST', '/call');
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.onload = () => {
    if (xhr.status === 200) {
      console.log(xhr.response);
    } else {
      console.error(xhr.response);
    }
  };
  xhr.send(JSON.stringify({photo1, photo2}));
});

const prevButton = document.querySelector('#prev-data');


const images = [];

for (let i = 0; i < 500; i++) {
  const path = `generated${i}.png`;
  const img = new Image();
  img.src = path;
  images.push(img);
}

prevButton.addEventListener('click', ()=>{
  for (let i = 0; i < 500; i++) {
    setTimeout(function() {
      const path = `generated${i}.png`;
      imageContainer3.style.backgroundImage = `url(${path})`;
      imageContainer3.style.backgroundSize = 'cover';
    }, i * 30);
  }
});
