from flask import Flask,jsonify,request
from Message import  Message
import DB

app = Flask(__name__)


def get_url_parm_and_value():
    if 'applicationId' in request.args:
        Id = str(request.args['applicationId'])
        asked_param='application_id'
    elif 'sessionId' in request.args:
        Id = str(request.args['sessionId'])
        asked_param = 'session_id'
    elif 'messageId' in request.args:
        Id=str(request.args['messageId'])
        asked_param = 'message_id'
    else:
        return None, None  # that means error
    return Id, asked_param


@app.route('/GetMessage', methods=['GET'])
def get_message():
   Id, askedParam = get_url_parm_and_value()
   if Id :
       if askedParam == 'message_id':
           resault = DB.get_message(Id)
       else:
            resault = DB.get_messages(Id, askedParam)
       if resault is not False:
           return jsonify(resault)
       else: return "Eror:Couldn't read data",500
   else:  return "Error: No match field provided. Please specify an applicationId/sessionId/messageId.", 404


@app.route('/AddMessage', methods=['POST'])
def add_message():
    new_msg_data=request.get_json()
    try:
        new_msg=Message(application_id=new_msg_data['application_id'],
                  session_id=new_msg_data['session_id'],message_id=new_msg_data['message_id'],
                   participants=new_msg_data['participants'], content=new_msg_data['content'])
        if type(new_msg.participants) is not list:
            return 'Error: the json data does not match the expected pattern', 402
    except:
        return 'Error: the json data does not match the expected pattern', 402
    success = DB.add_message(new_msg)

    if success:
        return 'created', 201
    return 'No success insert data(maybe the messageId have used already)', 500


@app.route('/DeleteMessage' , methods=['DELETE'])
def delete_message():
    Id, asked_param = get_url_parm_and_value()
    if Id:
        if asked_param == 'message_id':
            count_deleted_messages = DB.delete_message(Id)

        else:
            count_deleted_messages = DB.delete_messages(Id, asked_param)
    else:
        return "Error: No match field provided. Please specify an applicationId/sessionId/messageId.", 404
    if count_deleted_messages >= 0:
        return str(count_deleted_messages)+" messages deleted" , 200

    return "Error: Couldn't delete the data", 500


if __name__ == '__main__':
    app.run(debug=True)
