from flask import Flask, request, render_template, jsonify
import ML.network as network
import ML.mnist_loader as mnist_loader
import numpy as np

app = Flask(__name__)

# load trained network data
bias, weight, accuracy = network.load_network("ML/trained.npy")

@app.route("/", methods=["GET", "POST"])
def index():
    
    if request.method == "POST":

        # string -> array
        temp = request.form.get("mnist")
        temp = temp.split(',')

        # array -> numpy.arry(784, 1)
        mnist = []
        for i in temp:
            mnist.append(float(i))
        # print(mnist)

        mnist = np.array(mnist)
        mnist = mnist.reshape((784, 1))
        # print(mnist.shape)
        # print(mnist)
        
        try:
            resultArray, result = network.recognition(mnist, bias, weight)
        except:
            return "something wrong!!"
        
        # print(result)
        return jsonify({"result": int(result), "resultArray": "{}".format(resultArray)})
    
    return render_template("index.html", accuracy=accuracy)