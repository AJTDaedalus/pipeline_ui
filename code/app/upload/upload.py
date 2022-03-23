from flask import *
app = Flask(__name__)

@app.route('/upload')
def upload():
    return render_template("fileform.html")

@app.route('/success',methods=['POST'])
def success():
    if request.method == 'POST':
        f=request.files['file']
        f.save(f.filename)
        return render_template("success.html")
    
if __name__ == 'main':
    app.run(debug=True)