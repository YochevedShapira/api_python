from Message import Message
import sqlite3

sql_select_query_GetMessagesByApplicationId = """select * from Messages where applicationId = ?"""
sql_select_query_GetMessagesBySessionId = """select *  from Messages where sessionId = ?"""
sql_select_query_GetMessageByID = """select *  from Messages  where messageId = ?"""
sql_select_query_participants = """select participantName from participants where messageId = ?"""
sql_delete_query_MessagesByApplicationId = """DELETE from Messages where applicationId = ?"""
sql_delete_query_MessagesBySessionId = """DELETE from Messages where sessionId= ?"""
sql_delete_query_MessageByMessageId = """DELETE from Messages where messageId= ?"""
sql_delete_query_participantsByApplicationId = """ DELETE from participants  
where messageId in(select messageId from Messages where applicationId=?)"""
sql_delete_query_participantsBySessionId = """ DELETE from participants  
where messageId in(select messageId from  Messages where sessionId=?)"""
sql_delete_query_participantsByMessageId = """ DELETE from participants  where messageId =?"""
sqlite_insert_query_Message = """INSERT INTO Messages (messageId, applicationId, sessionId, content)
  VALUES (?, ?, ?, ?);"""
sqlite_insert_query_participant = """INSERT INTO participants (participantName,messageId)   VALUES (?, ?);"""


def get_messages_from_db(id, param):
    try:
        sqlite_connection = sqlite3.connect('MessagesDB.db')
        cursor = sqlite_connection.cursor()
        print("Connected to SQLite")
        if param == 'application_id':
            cursor.execute(sql_select_query_GetMessagesByApplicationId, (id,))
        elif param == "session_id":
            cursor.execute(sql_select_query_GetMessagesBySessionId, (id,))
        else:
            return False
        records = cursor.fetchall()
        result = []
        for row in records:
            msg = Message(message_id=row[0], application_id=row[1],
                          session_id=row[2], content=row[3])
            cursor.execute(sql_select_query_participants, (msg.message_id,))
            participants_record = cursor.fetchall()
            par_list = [p[0] for p in participants_record]
            msg.participants = par_list
            result.append(msg)
        cursor.close()
        return result
    except sqlite3.Error as error :
        print("Failed to read data from sqlite table", error)
        return False
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("The SQLite connection is closed")


def get_signal_message_from_db(id):
    try:
        sqlite_connection = sqlite3.connect('MessagesDB.db')
        cursor = sqlite_connection.cursor()
        print("Connected to SQLite")
        cursor.execute(sql_select_query_GetMessageByID, (id,))
        records = cursor.fetchall()
        if cursor.rowcount == -1:  # that means the message with the asked id was'nt found
            return None
        row = records[0]
        msg = Message(message_id=row[0], application_id=row[1],
                      session_id=row[2], content=row[3])
        cursor.execute(sql_select_query_participants, (msg.message_id,))
        participants_record = cursor.fetchall()
        cursor.close()
        par_list = [p[0] for p in participants_record]
        msg.participants = par_list
        return msg
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
        return False
    finally :
        if sqlite_connection:
            sqlite_connection.close()
            print("The SQLite connection is closed")


def delete_messages_from_db(id, param) :
    try:
        sqlite_connection = sqlite3.connect('MessagesDB.db')
        cursor = sqlite_connection.cursor()
        print("Connected to SQLite")
        if param == 'application_id':
            cursor.execute(sql_delete_query_participantsByApplicationId, (id,))
            cursor.execute(sql_delete_query_MessagesByApplicationId, (id,))
            count_deleted_messages = cursor.rowcount
        elif param == "session_id":
            cursor.execute(sql_delete_query_participantsBySessionId, (id,))
            cursor.execute(sql_delete_query_MessagesBySessionId, (id,))
            count_deleted_messages = cursor.rowcount
        else:
            return -1
        sqlite_connection.commit()
        cursor.close()
        return count_deleted_messages
    except sqlite3.Error as error:
        print("Failed to delete record from sqlite table", error)
        return -1
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("the sqlite connection is closed")


def delete_signal_message_from_db(id) :
    try:
        sqlite_connection = sqlite3.connect('MessagesDB.db')
        cursor = sqlite_connection.cursor()
        print("Connected to SQLite")
        cursor.execute(sql_delete_query_MessageByMessageId, (id,))
        count_deleted_messages = cursor.rowcount
        cursor.execute(sql_delete_query_participantsByMessageId, (id,))
        cursor.close()
        return count_deleted_messages
    except sqlite3.Error as error:
        print("Failed to delete record from sqlite table", error)
        return -1
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("the sqlite connection is closed")


def insert_msg_to_db(data_to_msg_table: tuple, data_to_participants_table: list):
    try:
        sqlite_connection = sqlite3.connect('MessagesDB.db')
        cursor = sqlite_connection.cursor()
        print("Connected to SQLite")
        cursor.executemany(sqlite_insert_query_participant, data_to_participants_table)
        cursor.execute(sqlite_insert_query_Message, data_to_msg_table)
        sqlite_connection.commit()
        print("Total", cursor.rowcount, "inserted successfully ")
        sqlite_connection.commit()
        cursor.close()
        return True
    except sqlite3.Error as error:
        print("Failed to insert ", error)
        return False
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("The SQLite connection is closed")


def add_message(message: Message):
    data_msg = (message.message_id, message.application_id, message.session_id, message.content)
    data_participants = [(par, message.message_id) for par in message.participants]
    success = insert_msg_to_db(data_msg, data_participants)
    if success:
        return True
    return False


def get_message(id):
    msg = get_signal_message_from_db(id)
    if msg is not False:
        if msg is None:
            return {}
        return msg.ParseToDicionary()
    return False


def get_messages(id, by_param):
    messages_list = get_messages_from_db(id, by_param)
    if messages_list is not False:
        dict_msg_list = [msg.ParseToDicionary() for msg in messages_list]
        return dict_msg_list
    return False


def delete_message(id):
    return delete_signal_message_from_db(id)


def delete_messages(id, by_param):
    return delete_messages_from_db(id, by_param)  # it returns the count of the deleted messages
