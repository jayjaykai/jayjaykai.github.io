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

    // console.log(attraction);
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

    let infoAddtDiv = document.createElement('div');
    infoAddtDiv.className = 'info-address';
    infoAddtDiv.innerHTML = "景點地址：<br>" + attraction.data.address;

    let infoTrans = document.createElement('div');
    infoTrans.className = 'info-transport';
    infoTrans.innerHTML = "交通方式：<br>" + attraction.data.transport;

    infoDiv.appendChild(infoDescripDiv);
    infoDiv.appendChild(infoAddtDiv);
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