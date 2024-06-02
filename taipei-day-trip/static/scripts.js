let currentPage = 0;
let isLoading = false;
let currentIndex = 0;

async function getData(page) {
    console.log(page);
    isLoading = true;
    let response = await fetch(`http://3.27.243.249:8000/api/attractions?page=${page}`, {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        }
    });
    if (!response.ok) {
        console.error('HTTP error', response.status);
        isLoading = false;
        return;
    }
    let result = await response.json();
    let spots = result.data;
    addContent(spots);
    isLoading = false;
}

function addContent(results) {
    let container = document.getElementById('spot_images');
    for (let i = 0; i < results.length; i++) {
        let itemContainer = document.createElement('div');
        itemContainer.className = 'List_spot';

        let imageContainer = document.createElement('div');
        imageContainer.className = 'image-container';

        let img = document.createElement('img');
        img.className = 'content_image';
        img.src = results[i].images[0];
        img.alt = results[i].name;

        let textDiv = document.createElement('div');
        textDiv.className = 'image-text';
        textDiv.textContent = results[i].name;

        imageContainer.appendChild(img);
        imageContainer.appendChild(textDiv);

        let infotextDiv = document.createElement('div');
        infotextDiv.className = 'image-info';

        let mrt = document.createElement('div');
        mrt.className = 'mrt-name';
        mrt.textContent = results[i].mrt;

        let cat = document.createElement('div');
        cat.className = 'category';
        cat.textContent = results[i].category;

        infotextDiv.appendChild(mrt);
        infotextDiv.appendChild(cat);

        itemContainer.appendChild(imageContainer);
        itemContainer.appendChild(infotextDiv);

        container.appendChild(itemContainer);
    }
}

async function addMrtsList() {
    let response = await fetch("http://3.27.243.249:8000/api/mrts", {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        }
    });
    let mrts = await response.json();
    let mrtList = new Set();
    for (let i = 0; i < mrts.length; i++) {
        if (mrts[i]) {
            mrtList.add(mrts[i]);
        }
    }

    let listMrtsDiv = document.getElementById('list-mrts');
    listMrtsDiv.innerHTML = '';

    let mrtArray = Array.from(mrtList);
    for (let i = 0; i < mrtArray.length; i++) {
        let mrt = mrtArray[i];
        let mrtLink = document.createElement('a');
        mrtLink.textContent = mrt;
        mrtLink.className = 'mrt-info';
        mrtLink.addEventListener('click', function (event) {
            event.preventDefault();
            document.getElementById('mrtInput').value = mrt;
            fetchAttractionsByKeyword(mrt);
        });
        listMrtsDiv.appendChild(mrtLink);
    }
}

async function fetchAttractionsByKeyword(keyword) {
    let response = await fetch(`http://3.27.243.249:8000/api/attractions?page=0&keyword=${encodeURIComponent(keyword)}`, {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        }
    });
    let result = await response.json();
    let spots = result.data;
    console.log(spots);
    let container = document.getElementById('spot_images');
    container.innerHTML = "";
    addContent(spots);
}

function searchByMRT() {
    let mrtInput = document.getElementById('mrtInput').value.trim();
    if (mrtInput) {
        fetchAttractionsByKeyword(mrtInput);
    } else {
        alert('請輸入捷運站名稱');
    }
}

// function shiftLeft() {
//     const items = document.getElementById('list-mrts');
//     const itemCount = items.children.length;
//     if (currentIndex > 0) {
//         currentIndex--;
//         updateScroll(items);
//     }
// }

// function shiftRight() {
//     const items = document.getElementById('list-mrts');
//     const itemCount = items.children.length;
//     const visibleItemsCount = Math.floor(items.parentElement.offsetWidth / items.children[0].offsetWidth);
//     console.log("visibleItemsCount: "+ visibleItemsCount);
//     console.log("CurrentIndex: " +currentIndex);
//     console.log("ItemCount: " +itemCount);

//     if (currentIndex < itemCount - visibleItemsCount) {
//         currentIndex++;
//         updateScroll(items);
//     }
// }

// function updateScroll(items) {
//     const itemCount = items.children.length;
//     const visibleItemsCount = Math.floor(items.parentElement.offsetWidth / items.children[0].offsetWidth);
//     const itemWidth = items.children[0].offsetWidth;
//     items.style.transform = `translateX(${-currentIndex * itemWidth}px)`;
//     console.log(itemCount - visibleItemsCount + currentIndex);
//     items.children[itemCount - visibleItemsCount].style.visibility = 'visible';
//     items.children[itemCount - visibleItemsCount].style.display = 'inline-block';
// }

function shiftLeft() {
    const items = document.getElementById('list-mrts');
    const itemWidth = items.children[0].offsetWidth;
    if (currentIndex > 0) {
        currentIndex--;
        items.scrollBy({
            left: -itemWidth,
            behavior: 'smooth'
        });
    }
}

function shiftRight() {
    const items = document.getElementById('list-mrts');
    const itemCount = items.children.length;
    const itemWidth = items.children[0].offsetWidth;
    const visibleWidth = items.parentElement.offsetWidth;
    const visibleItemsCount = Math.floor(visibleWidth / itemWidth)-5;

    // console.log("visibleWidth: "+ visibleWidth);
    // console.log("itemWidth: "+ itemWidth);
    // console.log("visibleItemsCount: "+ visibleItemsCount);
    // console.log("ItemCount: " +itemCount);
    // console.log("CurrentIndex: " +currentIndex);
    if (currentIndex < itemCount - visibleItemsCount) {
        currentIndex++;
        items.scrollBy({
            left: itemWidth,
            behavior: 'smooth'
        });
    }
}

// document.addEventListener('DOMContentLoaded', () => {
    getData(currentPage);
    addMrtsList();

    window.addEventListener('scroll', () => {
        console.log('scrolling...');
        console.log('window.innerHeight:', window.innerHeight);
        console.log('window.scrollY:', Math.ceil(window.scrollY));
        console.log('document.body.offsetHeight:', document.body.offsetHeight);

        if ((window.innerHeight + Math.ceil(window.scrollY)) >= document.body.offsetHeight && !isLoading) {
            console.log('bottom reached');
            currentPage++;
            getData(currentPage);
        }
    });
// });
