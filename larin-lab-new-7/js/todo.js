class Task {
    constructor(text, state) {
        this.text = text;
        this.state = state;
    }
}

var tasks = [];

setInterval(() => {
    document.querySelector("body").removeAttribute("style");
}, 1);


window.addEventListener('load', function () {
    tasks = JSON.parse(localStorage.getItem('tasks'));
    if (tasks) {
        tasks.forEach(task => {
            createTask(task.text, task.state);
        })
        countItems();
    } else {
        localStorage.setItem("tasks", JSON.stringify([]));
        tasks = [];
    }
})

function countItems() {
    let counter = 0;
    tasks.forEach(task => {
        if (!task.state) {
            counter++;
        }
    })
    document.querySelector(".states p").textContent = counter.toString() + " item left";
}

function createTask(text, state) {
    let tmp = document.querySelector('template');
    let template = tmp.content.cloneNode(true);
    let count = document.querySelector(".todo").childElementCount * 70
    template.querySelector("div").setAttribute(`data-${count - 810}`, template.querySelector("div").getAttribute('data-0'));
    template.querySelector("div").removeAttribute("data-0")
    template.querySelector("div").setAttribute(`data-${count - 110}`, template.querySelector("div").getAttribute('data-500'));
    template.querySelector("div").removeAttribute("data-500")
    template.querySelector("p").textContent = text;
    if (state) {
        template.querySelector("input").setAttribute('checked', '');
        template.querySelector("p").classList.add('line-through');
    }
    document.querySelector(".todo").appendChild(template);
}

function addTask() {
    state(0);
    let text = document.querySelector("input").value;
    if (text.trim()) {
        let is_new = true;
        tasks.forEach(task => {
            if (task.text === text){
                is_new = false;
            }
        })
        if (is_new) {
            let task = new Task(text, false);
            tasks.push(task);
            localStorage.setItem("tasks", JSON.stringify(tasks));
            createTask(text, false);
            countItems();
        } else {
            alert("Данно задание уже есть");
        }
    }
    document.querySelector("input").value = "";
    s.refresh();//перезапуск
}

function deleteTask(el) {
    tasks.forEach(task => {
        if (task.text === el.parentNode.childNodes[3].textContent){
            tasks.splice(tasks.indexOf(task), 1);
        }
    })
    countItems();
    localStorage.setItem("tasks", JSON.stringify(tasks))
    document.querySelector(".todo").removeChild(el.parentNode);
}

function changeState(el) {
    tasks.forEach(task => {
        if (task.text === el.parentNode.parentNode.childNodes[3].textContent){
            task.state = !task.state;
            if (task.state){
                el.parentNode.parentNode.childNodes[3].classList.add('line-through');
            } else {
                el.parentNode.parentNode.childNodes[3].classList.remove('line-through');
            }
        }
    })
    countItems();
    localStorage.setItem("tasks", JSON.stringify(tasks));
}

function state(state) {
    for (let i = 0; i < 3; i++) {
        if (i === state){
            document.querySelectorAll(".state p")[i].classList.add("active");
        } else {
            document.querySelectorAll(".state p")[i].classList.remove("active");
        }
    }
    document.querySelectorAll(".task").forEach(task => {
        task.remove();
    });
    function check (el) {
        return true
    }
    switch (state) {
        case 1:
            check = function (el) {
                return !el
            }
            break;
        case 2:
            check = function (el) {
                return el
            }
            break;
    }
    tasks.forEach(task => {
        if (check(task.state)) {
            createTask(task.text, task.state);
        }
    })
}