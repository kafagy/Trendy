DROP PROCEDURE  sp_validateLogin;

CREATE PROCEDURE sp_validateLogin(IN p_email VARCHAR(20))
  BEGIN
    select * from users where email = p_email;
END;

