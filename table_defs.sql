


-- Creating tables

CREATE TABLE Person(
    email VARCHAR(20), 
    password CHAR(64), 
    fname VARCHAR(20),
    lname VARCHAR(20),
    PRIMARY KEY (email)
)ENGINE = InnoDB;

CREATE TABLE Friendgroup(
    owner_email VARCHAR(20), 
    fg_name VARCHAR(20), 
    description VARCHAR(1000), 
    PRIMARY KEY (owner_email, fg_name),
    FOREIGN KEY (owner_email) REFERENCES Person(email)
)    ENGINE = InnoDB;



CREATE TABLE Belong (
    email VARCHAR(20), 
    owner_email VARCHAR(20),
    fg_name VARCHAR(20),
    PRIMARY KEY (email, owner_email, fg_name),
    FOREIGN KEY(email) REFERENCES Person(email),
    FOREIGN KEY(owner_email, fg_name) REFERENCES  Friendgroup(owner_email, fg_name)
)    ENGINE = InnoDB;


CREATE TABLE ContentItem(
    item_id int AUTO_INCREMENT, 
    email_post VARCHAR(20),
    post_time Timestamp DEFAULT CURRENT_TIMESTAMP, 
    file_path VARCHAR(100), 
    item_name VARCHAR(1000),
    content_type VARCHAR(20),
    is_pub Boolean, 
    PRIMARY KEY(item_id),
    FOREIGN KEY(email_post) REFERENCES Person(email)
)    ENGINE = InnoDB;



CREATE TABLE Rate (
    email VARCHAR(20), 
    item_id int, 
    rate_time Timestamp DEFAULT CURRENT_TIMESTAMP, 
    emoji VARCHAR(20) CHARACTER SET utf8mb4,
    PRIMARY KEY(email, item_id), 
    FOREIGN KEY(email) REFERENCES Person(email),
        FOREIGN KEY(item_id)REFERENCES ContentItem(item_id)
);        

CREATE TABLE Share ( 
    owner_email VARCHAR(20), 
    fg_name VARCHAR(20), 
    item_id int, 
    PRIMARY KEY(owner_email, fg_name, item_id),
     FOREIGN KEY(owner_email, fg_name) REFERENCES Friendgroup(owner_email, fg_name),                  
    FOREIGN KEY (item_id) REFERENCES ContentItem(item_id)
)    ENGINE = InnoDB;


CREATE TABLE Tag (
    email_tagged VARCHAR(20), 
    email_tagger VARCHAR(20), 
    item_id int,
    status VARCHAR(20),
    tagtime Timestamp DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(email_tagged, email_tagger, item_id),
    FOREIGN KEY(email_tagged) REFERENCES Person(email),
    FOREIGN KEY(email_tagger) REFERENCES Person(email),
    FOREIGN KEY(item_id) REFERENCES ContentItem(item_id)
)    ENGINE = InnoDB;

CREATE TABLE Comments (
	content VARCHAR(1000),
	commentor_email VARCHAR(20),
	item_id int,
	FOREIGN KEY(commentor_email) REFERENCES Person(email),
	FOREIGN KEY(item_id) REFERENCES ContentItem(item_id)
) ENGINE = InnoDB;





-- Creating people
INSERT INTO Person(email, password, fname, lname)
VALUES ('AA@nyu.edu', SHA2('AA', 256), 'Ann', 'Anderson');

INSERT INTO Person(email, password, fname, lname)
VALUES ('BB@nyu.edu', SHA2('BB', 256), 'Bob', 'Baker');

INSERT INTO Person(email, password, fname, lname)
VALUES ('CC@nyu.edu', SHA2('CC', 256), 'Cathy', 'Chang');

INSERT INTO Person(email, password, fname, lname)
VALUES ('DD@nyu.edu', SHA2('DD', 256), 'David', 'Davidson');

INSERT INTO Person(email, password, fname, lname)
VALUES ('EE@nyu.edu', SHA2('EE', 256), 'Ellen', 'Ellenberg');

INSERT INTO Person(email, password, fname, lname)
VALUES ('FF@nyu.edu', SHA2('FF', 256), 'Fred', 'Fox');

INSERT INTO Person(email, password, fname, lname)
VALUES ('GG@nyu.edu', SHA2('GG', 256), 'Gina', 'Gupta');

INSERT INTO Person(email, password, fname, lname)
VALUES ('HH@nyu.edu', SHA2('HH', 256), 'Helen', 'Harper');

-- Creating friend groups 
INSERT INTO Friendgroup(owner_email, fg_name, description)
VALUES ('AA@nyu.edu', 'family', "Ann's family");

INSERT INTO Friendgroup(owner_email, fg_name, description)
VALUES ('BB@nyu.edu', 'family', "Bob's family");

INSERT INTO Friendgroup(owner_email, fg_name, description)
VALUES ('AA@nyu.edu', 'roommates', "Ann's Roomies");

-- Inserting into AA's family group
INSERT INTO Belong(email, owner_email, fg_name)
VALUES ('AA@nyu.edu', 'AA@nyu.edu', 'family');

INSERT INTO Belong(email, owner_email, fg_name)
VALUES ('CC@nyu.edu', 'AA@nyu.edu', 'family');


INSERT INTO Belong(email, owner_email, fg_name)
VALUES ('DD@nyu.edu', 'AA@nyu.edu', 'family');

INSERT INTO Belong(email, owner_email, fg_name)
VALUES ('EE@nyu.edu', 'AA@nyu.edu', 'family');

-- Inserting into BB's family group
INSERT INTO Belong(email, owner_email, fg_name)
VALUES ('BB@nyu.edu', 'BB@nyu.edu', 'family');

INSERT INTO Belong(email, owner_email, fg_name)
VALUES ('FF@nyu.edu', 'BB@nyu.edu', 'family');

INSERT INTO Belong(email, owner_email, fg_name)
VALUES ('EE@nyu.edu', 'BB@nyu.edu', 'family');

-- Inserting into AA's roomies group
INSERT INTO Belong(email, owner_email, fg_name)
VALUES ('AA@nyu.edu', 'AA@nyu.edu', 'roommates');

INSERT INTO Belong(email, owner_email, fg_name)
VALUES ('GG@nyu.edu', 'AA@nyu.edu', 'roommates');

INSERT INTO Belong(email, owner_email, fg_name)
VALUES ('HH@nyu.edu', 'AA@nyu.edu', 'roommates');


-- Ann is posting 
INSERT INTO ContentItem(email_post, file_path, item_name,content_type, is_pub)
VALUES('AA@nyu.edu', NULL , 'Whiskers','text', False);

INSERT INTO Share(owner_email, fg_name, item_id) 
VALUES( 'AA@nyu.edu', 'family',  1);


-- She doing it again 
INSERT INTO ContentItem(email_post, file_path, item_name, content_type, is_pub)
VALUES('AA@nyu.edu', NULL, 'leftovers in fridge', 'text', False);

INSERT INTO Share(owner_email, fg_name, item_id) 
VALUES( 'AA@nyu.edu', 'roommates', 2);


-- Now Bobert is posting 
INSERT INTO ContentItem(email_post, file_path, item_name, content_type, is_pub)
VALUES('BB@nyu.edu', NULL, 'Rover', 'text', False);

INSERT INTO Share(fg_name, owner_email, item_id) 
VALUES('family', 'BB@nyu.edu', 3);

-- Just a public post. Nothing to see here 
INSERT INTO ContentItem(email_post, file_path, item_name,content_type, is_pub)
VALUES('CC@nyu.edu', NULL , 'YAH YEET','text', True);



