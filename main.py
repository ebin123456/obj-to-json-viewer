from flask import *
from flask.ext.paginate import Pagination
from db.db import *
from db.obj_to_js import * 
 
import time
import glob
import ntpath
app = Flask(__name__) 

@app.route("/")
def hello():
    models = get_models()
    return render_template('index.html',models = models)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['model']
        file_name = f.filename
        new_name = str(time.time())+file_name
        new_dir = str(time.time())
        dir_path = 'static/upload/'+new_dir
        os.makedirs(dir_path)
        path = 'static/upload/'+new_name
        f.save(dir_path+"/model.zip")
        extract_zip(dir_path+"/model.zip",dir_path+"/")
        model_path = 'static/upload/models/'+new_name
       
        files = glob.glob(dir_path+'/*.obj')
        for obj in files:
            
            convert_ascii(obj,"","",obj+".js")
            file_name = new_dir+"/" + ntpath.basename(obj)
            save_to_db(obj,file_name+".js")
    return hello()


@app.route("/model/<model>/<obj>")
def model(model,obj):

    return render_template('model.html',path_dir = model,obj=obj)    

PER_PAGE = 2

@app.route('/kk')
def index():
    search = False
    q = request.args.get('q')
    print q
    if q:
        search = True

    users = (1,2,3,4,5)
    pagination = Pagination(100, search=search, record_name='users')
    return render_template('user.html',
                           users=users,
                           pagination=pagination,
                           )

if __name__ == "__main__":
    app.run(debug=True)