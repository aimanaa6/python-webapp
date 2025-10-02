DELIMITER //

CREATE PROCEDURE add_user(IN new_username varchar(150), IN h_password varchar(250))
    BEGIN
        INSERT INTO users(username, hashed_password)
        VALUES (new_username, h_password);
    END //

DELIMITER;
