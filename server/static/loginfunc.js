function onSuccess(googleUser) {
    var id_token = googleUser.getAuthResponse().id_token;
    sendIdToken(id_token);
}
function sendIdToken(id_token) {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/logincheck');
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onload = function () {
        if (xhr.readyState == 4) {
            afterSignin();
            if (xhr.status == 200) {
                window.location.href = xhr.responseURL
            }
        }
    }
    xhr.send('idtoken=' + id_token);
}
function afterSignin() {
    document.getElementById('g-signin').style.display = "none";
}
function onFailure(error) {
    window.alert(error);
}
function renderButton() {
    gapi.signin2.render('g-signin', {
        'scope': 'profile email',
        'width': 240,
        'height': 50,
        'longtitle': true,
        'theme': 'light',
        'onsuccess': onSuccess,
        'onfailure': onFailure
    });
}