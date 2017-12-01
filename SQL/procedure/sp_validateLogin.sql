DROP PROCEDURE IF EXISTS sp_validateLogin;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_validateLogin`
(
  IN p_email VARCHAR(20)
)
BEGIN
    select * from users where email = p_email;
END$$
DELIMITER ;