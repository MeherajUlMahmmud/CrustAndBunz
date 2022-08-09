var updateBtns = document.getElementsByClassName('update-cart')

    for (let i = 0; i < updateBtns.length; i++) {
        updateBtns[i].addEventListener('click', function () {
            var foodID = this.dataset.food;
            var action = this.dataset.action;
            console.log('foodID: ', foodID, 'action: ', action);

            updateCart(foodID, action);
        })
    }

    function updateCart(foodID, action) {
        console.log('User logged in')

        var url = '/update-item/'

        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({'foodID': foodID, 'action': action})
        }).then((response) => {
            return response.json()
        }).then((data) => {
            console.log('data:', data)
            location.reload()
        })
    }