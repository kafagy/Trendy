DROP PROCEDURE sp_createUser;

CREATE PROCEDURE sp_createUser(IN p_username VARCHAR(20), IN p_email VARCHAR(20), IN p_password VARCHAR(100))
  BEGIN
    if ( select exists (select 1 from users where username = p_username) ) THEN

        select 'Username Exists !!';

    ELSE

        insert into users
        (
            username,
            email,
            password,
            loadtime
        )
        values
        (
            p_username,
            p_email,
            p_password,
            now()
        );

    END IF;
END;

