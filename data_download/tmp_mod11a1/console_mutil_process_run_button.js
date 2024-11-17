function run(count){
    try{
        for (var idx = 1; idx <= count; idx++){
            var button = document.querySelector("#task-pane").shadowRoot.querySelector("div.client-task-pane > div > div:nth-child(" + idx + ") > ee-button")
            if (button !== undefined){
                button.click()
            }
        }
    }
    catch{}
}

function ok(){
    try{
        // var button = document.querySelector("body > ee-image-config-dialog").shadowRoot.querySelector("ee-dialog").shadowRoot.querySelector("paper-dialog > div.buttons > ee-button.ok-button")
        var button = document.querySelector("body > ee-table-config-dialog").shadowRoot.querySelector("ee-dialog").shadowRoot.querySelector("paper-dialog > div.buttons > ee-button.ok-button")
        if (button !== undefined){
            button.click()
        }
    }
    catch{}
}

function runonce(){
    try{
        var length = document.querySelector("#task-pane").shadowRoot.querySelector("div.client-task-pane > div").childElementCount
        if (length == 2){
            run(length)
        }
        else{
            run(1)
        }
    }
    catch{}
}

setInterval(ok, 500)
setInterval(runonce, 500)