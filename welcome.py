# Copyright 2015 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from flask import Flask, jsonify, send_file, request
from functions import *
import swiftclient


app = Flask(__name__)


@app.route ('/get_image', methods = ['POST','GET'])
def netatmo_callback():
    face_id = request.args.get('face_id')
    face_key = request.args.get('key')
   # print "Face Id: %s" %face_id
   # print "Key: %s" %face_key
    image_name = get_save_face(face_id, face_key)
   # x=2
    #print image_name
    return send_file(filename_or_fp='images/%s' %image_name)

@app.route('/object_storage', methods=['GET'])
def object_storage():

    auth_url = "https://identity.open.softlayer.com/v3" #add "/v3" at the ending of URL
    password = "oW1tCjUd!/Dy7tnR"
    project_id = "608e9ea7faf2437b9927f3e009864a6b"
    user_id = "230804c517cb469f9da096a1f0082280"
    region_name = "dallas"
    domain = "4e8c062d77dd4f43b356c360c06a9137"

    auth = v3.Password(auth_url=auth_url, username=admin,
                     password="oW1tCjUd", project_name="object_storage_04d321a4_d622_4094_a76a_d60ac0f294c0",
                    user_domain_id="4e8c062d77dd4f43b356c360c06a9137", project_domain_id="608e9ea7faf2437b9927f3e009864a6b")
    
    conn = swiftclient.Connection(key=password, 
    authurl=auth_url,  
    auth_version='3', 
    os_options={"project_id": project_id, 
                "user_id": user_id, 
                "region_name": region_name})

    cont_name = "home_intrusion_face_images"
    conn.put_container(cont_name)

    file_name = "images/morris.jpg"
    with open(file_name, 'r') as upload_file:
        conn.put_object(cont_name, file_name, contents= upload_file.read())


    return 'hello'

@app.route('/morris')
def get_morris():
    return send_file(filename_or_fp='images/morris.jpg')
@app.route('/')
def Welcome():
    return app.send_static_file('index.html')

@app.route('/myapp')
def WelcomeToMyapp():
    return 'Welcome again to my app running on Bluemix!'

@app.route('/api/people')
def GetPeople():
    list = [
        {'name': 'John', 'age': 28},
        {'name': 'Bill', 'val': 26}
    ]
    return jsonify(results=list)

@app.route('/api/people/<name>')
def SayHello(name):
    message = {
        'message': 'Hello ' + name
    }
    return jsonify(results=message)

port = os.getenv('PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port), debug=True)
