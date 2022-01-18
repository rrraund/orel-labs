async function requestTask(randint) {
    let url = `https://jsonplaceholder.typicode.com/todos/${randint}`;
    await fetch(url)
        .then(function (response) {
            if (response.status !== 200) {
                return Promise.reject(new Error(response.statusText))
            }
            return Promise.resolve(response)
        })
        .then(function (response) {
            return response.json()
        })
        .then(function (data) {
            let text = data.id.toString() + ": " + data.title;
            createTask(text, data.completed);
            let task = new Task(text, data.completed);
            tasks.push(task);
            localStorage.setItem("tasks", JSON.stringify(tasks));
            countItems();
            s.refresh();//перезапуск
            if (i === 5) {
                document.querySelector("#preloader").classList.add("none");
            }
        }).catch(function (error) {
            document.querySelector("#error").classList.remove("none");
            document.querySelector("#preloader").classList.add("none");
            clearInterval(interval);
        });
}

var interval;
var i = 0;


window.addEventListener('load', function () {
    document.querySelector("#preloader").classList.remove("none");
    let randint = Math.floor(Math.random() * 195) + 1;
    interval = setInterval(() => {
        requestTask(randint + i)
        i++;
        if (i === 5) {
            clearInterval(interval);
        }
    }, 1000)
});