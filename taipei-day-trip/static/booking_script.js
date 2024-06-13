// JavaScript 檢查區域是否為空
document.addEventListener("DOMContentLoaded", function() {
    // 檢查 token 並調用 getUserData
    let token = localStorage.getItem('token');
    if (token) {
        getUserData();
        getUserBookingData();
    } else {
        alert('請先登入會員帳戶');
        window.location.href = `/`;
    }

    let img = document.getElementById("image");
    console.log
    if (!img.src || img.src.trim() === "") {
        document.querySelector(".footer").classList.add("full-height-footer");
        document.querySelector(".travel-dedails").style.display = 'none';
        document.querySelector(".personInfo").style.display = 'none';
        document.querySelector(".creditCardInfo").style.display = 'none';
        document.querySelector(".confirm").style.display = 'none';
        document.querySelector(".delete-btn").style.display = 'none';
        document.querySelector(".hr1").style.display = 'none';
        document.querySelector(".hr2").style.display = 'none';
        document.querySelector(".hr3").style.display = 'none';
        document.querySelector(".noReservation").style.display = 'block';
    }
    // var personInfo = document.querySelector(".personInfo").innerHTML.trim();
    // var creditCardInfo = document.querySelector(".creditCardInfo").innerHTML.trim();
    // var confirm = document.querySelector(".confirm").innerHTML.trim();

    // if (!personInfo && !creditCardInfo && !confirm) {
    //     document.querySelector(".footer").classList.add("full-height-footer");
    //     document.querySelector(".hr1").style.display = 'none';
    //     document.querySelector(".hr2").style.display = 'none';
    //     document.querySelector(".hr3").style.display = 'none';
    // }
});

async function getUserData() { 
    try {
        let token = localStorage.getItem('token');
        let response = await fetch('http://127.0.0.1:8000/api/user/auth', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            }
        });
        
        // if (response.status === 403) {
        //     alert('無效的憑證，請重新登入');
        //     window.location.href = `/`;
        //     return;
        // }

        let result = await response.json();
        if (!response.ok) {
            console.error('HTTP error', response.status);
            alert(result.message);
            window.location.href = `/`;
        }

        // console.log(result.data);
        let username = document.getElementById('username');
        username.textContent = result.data.name;
    } 
    catch (error) {
        console.error('Error:', error);
    }
}

async function getUserBookingData() { 
    let token = localStorage.getItem('token');
    let response = await fetch('http://127.0.0.1:8000/api/booking', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        }
    });

    let result = await response.json();
    if (!response.ok) {
        console.error('HTTP error', response.status);
        alert(result.message);
        return;
    }
    console.log(result.data);
}
