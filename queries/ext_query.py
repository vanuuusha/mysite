insert_query = """
    INSERT INTO request (headers, method, initiator, url, timestamp, type, document, frame, 
    request) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s); 
"""

check_in_user_agent = """
SELECT USERID FROM user_agent_to_user_id WHERE USER_AGENT = %s;
"""

create_new_ext_user = """
    INSERT INTO user_agent_to_user_id (USER_AGENT, MAX_X, MAX_Y) VALUES (%s, %s, %s);
"""

create_new_note = """
    INSERT INTO Note (X, Y, SEASSION_timestamp, USERID, url) VALUES (%s, %s, %s, %s, %s);
"""

user_have_dataset = """
    SELECT COUNT(*) FROM Note WHERE USERID=%s;
"""

get_all_notes_for_user = """
    SELECT * FROM Note WHERE USERID={0};
"""

check_db_name_by_user = """
    SELECT EXISTS (SELECT 1
FROM information_schema.columns
WHERE table_name = 'user_{0}') 
"""

make_dataset_collected_true = """
    UPDATE user_agent_to_user_id 
    SET DATASET = 1
    WHERE USERID=%s
"""

get_dataset_for_user_collecte = """
    SELECT DATASET FROM user_agent_to_user_id WHERE USERID=%s
"""