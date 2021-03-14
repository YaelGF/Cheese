import web
import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np

urls = ('/upload', 'Upload')

class Upload():
    def GET(self):
        web.header("Content-Type","text/html; charset=utf-8")
        return """
        <html>
            <head></head>
                <body>
                    <form method="POST" enctype="multipart/form-data" action="">
                        <input type="file" name="myfile" />
                        <br/>
                        <input type="submit" />
                    </form>
                </body>
        </html>"""

    def POST(self):
        x = web.input(myfile={})
        filedir = '/workspace/cheese/cheese_api/static/src' # change this to the directory you want to store the file in.
        if 'myfile' in x: # to check if the file-object is created
            filepath=x.myfile.filename.replace('\\','/') # replaces the windows-style slashes with linux ones.
            filename=filepath.split('/')[-1] # splits the and chooses the last part (the filename with extension)
            fout = open(filedir +'/'+ filename,'wb') # creates the file where the uploaded file should be stored
            fout.write(x.myfile.file.read()) # writes the uploaded file to the newly created file.
            fout.close() # closes the file, upload complete.
        np.set_printoptions(suppress=True)
        model = tensorflow.keras.models.load_model('/workspace/cheese/cheese_api/static/model/keras_model.h5')
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        image = Image.open('/workspace/cheese/cheese_api/static/src/'+filename)
        size = (224, 224)
        image = ImageOps.fit(image, size, Image.ANTIALIAS)
        image_array = np.asarray(image)
        image.show()
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
        data[0] = normalized_image_array
        prediction = model.predict(data)
        for i in prediction:
            if i[0] > 0.60:
                analisis = "gouda"
            elif i[1] > 0.60:
                analisis = "mozzarella"
            elif i[2] > 0.60:
                analisis = "parmesano"
            elif i[3] > 0.60:
                analisis = "cheddar"
            elif i[4] > 0.60:
                analisis = "emmental"
            elif i[5] > 0.60:
                analisis = "brie"
            elif i[6] > 0.60:
                analisis = "blue_cheese"
            elif i[7] > 0.60:
                analisis = "roquefort"
            elif i[8] > 0.60:
                analisis = "macarpone"
            elif i[9] > 0.60:
                analisis = "feta"
            else:
                analisis = "not recogniced"
        print(prediction)
        return analisis


if __name__ == "__main__":
   app = web.application(urls, globals()) 
   app.run()