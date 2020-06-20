# simple-handwritten-digit-recognizer
simple web for handwritten digit recognition with python
## info
- flask web app
- canvas input
## required python lib
flask, numpy, random, cPickle, gzip, 
### ML files
- mnist.pkl.gz => mnist data for training and testing
- mnist_loader.py	=> mnist data loader
- network.py => ML obj and some useful function
- trained.npy	=> trained network data store here
- training.py => for network training

# note
### convert ImageData(rgba) to mnist(grayscale)
```javascript
function toMnist(imageData) {
    let arr = [];
    let r;
    for(var i=0; i<imageData.length; i+=4){
        r = (imageData[i] + imageData[i+1] + imageData[i+2])/(3*255);
        arr.push(1-r)
    }
    return arr;
}
```

### prepare string(mnist) -> numpy.array(784, 1) for calculation
```python
# string -> array
temp = request.form.get("mnist")
temp = temp.split(',')

# array -> numpy.arry(784, 1)
mnist = []
for i in temp:
mnist.append(float(i))
            
mnist = np.array(mnist)
mnist = mnist.reshape((784, 1))
```

### XMLHttpRequest
client request -> server respond -> client output
```python
@app.route("/", methods=["GET", "POST"])
def index():
    
    if request.method == "POST":

        # do something
        data = request.form.get("mnist")

        return "something"
    return render_template("index.html")
```
```javascript
document.getElementById("submit").onclick = () => {
        let req = new XMLHttpRequest();
        req.open("POST", "/");
        
        let data = new FormData();
        data.append("mnist", mnistData);
        req.send(data)

        req.onreadystatechange = () => {
            if(req.readyState == 4 && req.status == 200) {
                // do something
            }
            else {
                // do something
            }
        };
    };
```
