document.addEventListener('DOMContentLoaded', () => {

    var mnistData = null;
    var imageData = null;

    const canvas = document.getElementById("main-canvas");
    const context = canvas.getContext("2d");

    const mnistCan = document.getElementById("mnist-canvas");
    const mnistCtx = mnistCan.getContext("2d");

    const ansCan = document.getElementById("ans-canvas");
    const ansCtx = ansCan.getContext("2d");

    fillWhite(context, canvas);
    fillWhite(mnistCtx, mnistCan);
    fillWhite(ansCtx, ansCan);
    
    // draw section and update mnist-canvas, imageData
    let isDrawing = false;
    let x = 0;
    let y = 0;

    canvas.onmousedown = e => {
        isDrawing = true;
        x = e.offsetX;
        y = e.offsetY;
    };

    canvas.onmousemove = e => {
        if (isDrawing) {
            draw(context, x, y);
            x = e.offsetX;
            y = e.offsetY;
        }
    };

    document.onmouseup = () => {
        isDrawing = false;

        let img = new Image();
        img.src = canvas.toDataURL("image/png");

        img.onload = () => {
            mnistCtx.drawImage(img, 0, 0, canvas.width, canvas.height, 0, 0, mnistCan.width, mnistCan.height);
            imageData = mnistCtx.getImageData(0, 0, mnistCan.width, mnistCan.height);
            mnistData = toMnist(imageData.data);
            console.log(mnistData);
            //console.log("debug", imageData.data);
        };
    };
    
    // clear everthing to defaults
    document.getElementById("clear").onclick = () => {
        fillWhite(context, canvas);
        fillWhite(mnistCtx, mnistCan);
        fillWhite(ansCtx, ansCan);
        document.getElementById("test").innerHTML = "";
    };

    // onprocess
    // request section
    document.getElementById("submit").onclick = () => {
        let req = new XMLHttpRequest();
        req.open("POST", "/");
        
        let data = new FormData();
        data.append("mnist", mnistData);
        req.send(data)

        req.onreadystatechange = () => {
            if(req.readyState == 4 && req.status == 200) {
                res = JSON.parse(req.responseText)
                
                let pic = new Image()
                pic.src = `static/numbers/${res.result}.png`
                
                pic.onload = () => {
                    ansCtx.drawImage(pic, 0, 0, pic.width, pic.height, 0, 0, ansCan.width, ansCan.height);
                };

                document.getElementById("test").innerHTML = "";
                
                var i;
                for(i=0; i<10; i++){
                    var resultLog = document.createElement("div");
                    resultLog.id = i;
                    resultLog.innerHTML = `"${i}": ${res.resultArray[i]}`;
                    document.getElementById("test").appendChild(resultLog);
                }

                // document.getElementById("test").innerHTML = res.resultArray[0];
            }
            else {
                document.getElementById("test").innerHTML = "what?"
            }
        };
    };

});

function fillWhite(ctx, can) {
    ctx.fillStyle = "white";
    ctx.fillRect(0, 0, can.width, can.height);
};

function draw(ctx, x, y) {
    ctx.fillStyle = "black";
    ctx.beginPath();
    ctx.ellipse(x, y, 15, 15, 0, 0, 2 * Math.PI);
    ctx.fill();
    ctx.closePath();
};

function toMnist(imageData) {
    let arr = [];
    let r;
    for(var i=0; i<imageData.length; i+=4){
        r = (imageData[i] + imageData[i+1] + imageData[i+2])/(3*255);
        arr.push(1-r)
    }
    return arr;
}