(function() {
    let startTime = (new Date).getTime();
    window.addEventListener('load', function() {
        let endTime = (new Date).getTime();
        document.querySelector("#load_time").textContent = "Page load time is " + (endTime - startTime) / 1000 + " Seconds";
    });
})();