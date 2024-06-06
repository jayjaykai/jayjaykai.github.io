let currentIndex = 0;
let imageLen = 0;
let attraction;
let imgWrapper = document.getElementById('img-wrapper');

function getQueryParams() {
    const path = window.location.pathname;
    const parts = path.split('attraction/');
    // console.log(parts[1]);
    const attractionIndex = path.indexOf('attraction');
    if (attractionIndex !== -1 && parts.length == 2) {
        return parts[1];
    }
    return null;
}

async function fetchAttractionDetails(id) {
    let response = await fetch(`http://54.79.121.157:8000/api/attraction/${id}`);
    let result = await response.json();
    attraction = result;

    console.log(attraction);
    // let spotPicDiv = document.getElementById('spot-image');
    // spotPicDiv.src = attraction.data.images[currentIndex];
    imageLen = attraction.data.images.length;
    for (let i = 0; i < imageLen; i++) {
        const img = document.createElement('img');
        img.classList.add('spot-picture');
        img.src = attraction.data.images[i];
        imgWrapper.appendChild(img);
    }
    // Profile
    let attractionName = document.getElementById('profile-name');
    let attractionDescription = document.getElementById('profile-category');
    attractionName.textContent = attraction.data.name;
    attractionDescription.textContent = attraction.data.category + " at " + attraction.data.mrt ;

    // Info 
    let infoDiv = document.getElementById('info');
    let infoDescripDiv = document.createElement('div');
    infoDescripDiv.className = 'info-description';
    infoDescripDiv.textContent = attraction.data.description;

    let infoAddDiv = document.createElement('div');
    let infoAddtTtileDiv = document.createElement('div');
    infoAddtTtileDiv.className = 'info-address-title';
    infoAddtTtileDiv.innerHTML = "景點地址：";
    infoAddDiv.appendChild(infoAddtTtileDiv);
    let infoAddContentDiv = document.createElement('div');
    infoAddContentDiv.className = 'info-address';
    infoAddContentDiv.innerHTML = attraction.data.address;

    infoAddDiv.className = 'info-address-block';
    infoAddDiv.appendChild(infoAddContentDiv);

    let infoTrans = document.createElement('div');
    let infoTransTtileDiv = document.createElement('div');
    infoTransTtileDiv.className = 'info-transport-title';
    infoTransTtileDiv.innerHTML = "交通方式：";
    infoTrans.appendChild(infoTransTtileDiv);
    let infoTransContentDiv = document.createElement('div');
    infoTransContentDiv.className = 'info-transport';
    infoTransContentDiv.innerHTML = attraction.data.transport;

    infoTrans.className = 'info-transport-block';
    infoTrans.appendChild(infoTransContentDiv);

    infoDiv.appendChild(infoDescripDiv);
    infoDiv.appendChild(infoAddDiv);
    infoDiv.appendChild(infoTrans);

}

function updatePosition() {
    const offset = -currentIndex * 540;
    imgWrapper.style.transform = `translateX(${offset}px)`;
}

function preImg() {
    if (currentIndex > 0) {
        currentIndex--;
        updatePosition();
    }
}

function nextImg() {
    if (currentIndex < imageLen - 1) {
        currentIndex++;
        updatePosition();
    }
}

// // use another method
// function updateContent() {
//     let spotPicDiv = document.getElementById('spot-image');
//     spotPicDiv.src = attraction.data.images[currentIndex];
// }

// function preImage() {
//     if(currentIndex!=0){
//         let spotPicDiv = document.getElementById('spot-image');
//         spotPicDiv.classList.add('hidden');
//         setTimeout(() => {
//             currentIndex--;
//             updateContent();
//             spotPicDiv.classList.remove('hidden');
//         }, 300);
//     }
// }

// function nextImage() {
//     if(currentIndex>=0 && currentIndex < imageLen-1){
//         let spotPicDiv = document.getElementById('spot-image');
//         spotPicDiv.classList.add('hidden');
//         setTimeout(() => {
//             currentIndex++;
//             updateContent();
//             spotPicDiv.classList.remove('hidden');
//         }, 500);
//     }
// }


const attractionId = getQueryParams();
// console.log(attractionId);

if (attractionId) {
    fetchAttractionDetails(attractionId);
}