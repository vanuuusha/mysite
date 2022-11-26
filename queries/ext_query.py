insert_query = """
    INSERT INTO request (headers, method, initiator, url, timestamp, type, document, frame, 
    request) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s); 
"""

check_in_user_agent = """
SELECT USERID FROM user_agent_to_user_id WHERE USER_AGENT = %s;
"""

create_new_ext_user = """
INSERT INTO user_agent_to_user_id (USER_AGENT) VALUES (%s);
"""

create_new_note = """
    INSERT INTO Note (X, Y, SEASSION_timestamp, USERID, hostname) VALUES (%s, %s, %s, %s, %s);
"""

user_have_dataset = """
    SELECT COUNT(*) FROM Note WHERE USERID=%s;
"""