USE test;

CREATE TABLE accounts (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	firstname VARCHAR(255) NOT NULL,
	lastname_middlenames VARCHAR(255) NOT NULL,
	username  VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE ,
    password VARCHAR(255) NOT NULL
);

INSERT INTO accounts VALUES(
"Bishnu","Poudel","vsnupoudel","replytobishnu@gmail.com","bpoudel");

# Table to user and the mongodb Object ID for 24 hours
create table if not exists file_list_24hr
(
id int not null auto_increment primary key,
user_email VARCHAR(255) NOT NULL, 
    INDEX user_email_index (user_email),
    FOREIGN KEY (user_email)
        REFERENCES accounts(email)
        ON DELETE CASCADE,
start_date timestamp default current_timestamp not null,
end_date timestamp NULL ,
file_object_id VARCHAR(255) NULL,
predicted INT NULL
);

ALTER TABLE file_list_24hr ADD COLUMN file_object_id VARCHAR(255) NULL;
ALTER TABLE file_list_24hr ADD COLUMN predicted INT NULL;

ALTER TABLE file_list_24hr ADD CONSTRAINT file_object_id_unique UNIQUE file_object_id;


CREATE TRIGGER add_24_hours BEFORE INSERT ON file_list_24hr
FOR EACH ROW
  SET NEW.end_date =  COALESCE ( NEW.start_date, NOW() ) + INTERVAL 24 HOUR;
  
-- Insert 2 object IDs to test the trigger
INSERT INTO file_list_24hr ( id, user_email, start_date, end_date,  file_object_id, predicted )
VALUES (NULL, 'replytobishnu@gmail.com', NOW(), NOW() + INTERVAL 24 HOUR, '63dcfc67cf98d95aac03a2a4', NULL )

INSERT INTO file_list_24hr ( id, user_email, start_date, end_date,  file_object_id, predicted )
VALUES (NULL, 'replytobishnu@gmail.com', NOW(), NOW() + INTERVAL 24 HOUR, '63dcfc67cf98d95aac03a2aa', NULL )
