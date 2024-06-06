document.getElementById('loginButton').addEventListener('click', function() {
    // 檢查dialog是否存在，不存在使用fetch寫到body最後面
    if (!document.getElementById('loginModal')) {
        fetch('/static/dialog.html')
            .then(response => response.text())
            .then(html => {
                document.body.insertAdjacentHTML('beforeend', html);

                let modal = document.getElementById('loginModal');
                modal.showModal();
                document.getElementById('closeModal').addEventListener('click', function() {
                    modal.close();
                });

                // 點擊視窗外部關閉視窗
                window.addEventListener('click', function(event) {
                    if (event.target == modal) {
                        modal.close();
                    }
                });
            });
    } else {
        document.getElementById('loginModal').showModal();
    }
});