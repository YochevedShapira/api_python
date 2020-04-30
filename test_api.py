import json
from ctypes import py_object



from app import app
import pytest
url='/GetMessage?applicationId=321'



@pytest.mark.parametrize(
    "response,expected_status,expected_data",
    [
         (app.test_client().get('/GetMessage?applicationId=321'),200, []),
         (app.test_client().get('/GetMessage?blabla=999'), 404,
          b'Error: No match field provided. Please specify an applicationId/sessionId/messageId.'),
         (app.test_client().get('/GetMessage?messageId=988'), 200, {}),
    ]
)
def test_get_message(response, expected_status, expected_data):

    assert response.status_code == expected_status
    try:
        responseData=json.loads(response.data) #if it isn't json it wiil fall
        assert responseData == expected_data
    except:
           responseData=response.data
           assert responseData == expected_data

@pytest.mark.parametrize(
    "response,expected_status,expected_data",
    [(app.test_client().post('AddMessage',json={
    "application_id": "1",
    "content": "good day!!",
    "message_id": "111",
    "participants": [
        "me",
        "you"
    ],
    "session_id": "9"
}), 500, b'No success insert data(maybe the messageId have used already)'),
     (app.test_client().post('AddMessage',json={"mistake":"error!"}), 402,
      b'Error: the json data does not match the expected pattern'),
     ]
)
def test_add_message(response, expected_status, expected_data):
    assert response.status_code == expected_status
    assert response.data == expected_data

@pytest.mark.parametrize(
        "response,expected_status,expected_data",
        [
            (app.test_client().delete('DeleteMessage?applicationId=987'),200,b'0 messages deleted'),
             (app.test_client().delete('DeleteMessage?blabla=98765'),404, b"Error: No match field provided. Please specify an applicationId/sessionId/messageId."),
        ]
    )
def test_deleteMessage(response, expected_status, expected_data):
    assert response.status_code == expected_status
    assert response.data == expected_data

