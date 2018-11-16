from flask import Flask,render_template, request
from flask import jsonify
import random,base64
from mnist_base_test import construct_captcha_game

def generate_randint():
    randint = random.randint(2,3)
    
    return randint


app = Flask(__name__, template_folder='templates')

@app.route('/hello_world/<n>', methods=['POST','GET'])
def index(n):
    # I tried multi-process within a flask func but didnt work
    # just render a simple web page and use javascript to call
    # REST api from python server shell
    user_id = request.args.get('numofpeople','')
    s = generate_randint()
    print(s)
    #return numofpeople
    return render_template('captcha_hci.html', user_id=n)#numofpeople)
'''
@app.route('/<order>')
def order(order):
    if order=='forward':
        return 'forward'
    elif order=='left':
        return 'left'
    elif order=='right':
        return 'right'
    elif order=='back':
        return 'back'
    else:
        return order
'''
@app.route('/tmp')
def display():
    num = request.args.get('numofpeople','')
    return num

@app.route('/hci/<gametype>', methods=['POST','GET'])
def give_a_game(gametype):
    game_type = 'mnist'
    classes = ['airplane',
               'automobile',
               'bird',
               'cat',
               'deer',
               'dog',
               'frog',
               'horse',
               'ship',
               'truck']
    
    
    captcha_game = construct_captcha_game(game_type)
    captcha_image_list = captcha_game.get_captcha_images()
    captcha_game_groundtruth = captcha_game.get_captcha_groundtruth()
    captcha_game_content = {}
    for i,image in enumerate(captcha_image_list):
        captcha_game_content[i]=base64.b64encode(image)

    groundtruth_dic = {}
    for i,truth in enumerate(captcha_game_groundtruth):
        if truth in groundtruth_dic:
            groundtruth_dic[truth].append(i)
        else:
            groundtruth_dic[truth]=[i]
    
    question, waited_answer = random.choice(list(groundtruth_dic.items()))
    print(question, waited_answer)
    
    captcha_game_content["question"] = classes[question]
    
    return jsonify(captcha_game_content)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
