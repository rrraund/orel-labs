window.addEventListener('load', function() {
    let nav = document.querySelector("nav");
    let a = nav.querySelectorAll("a");
    for (let i = 0; i < a.length; i++) {
        if (a[i].href === window.location.href) {
            a[i].classList.add("active");
        }
    }
});