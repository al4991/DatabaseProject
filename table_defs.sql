


-- Creating tables

CREATE TABLE Person(
    email VARCHAR(20), 
    password CHAR(64), 
    fname VARCHAR(20),
    lname VARCHAR(20),
    PRIMARY KEY (email)
)     ENGINE = InnoDB;


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
	comment_time Timestamp DEFAULT CURRENT_TIMESTAMP,
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


-- Inserting into AA's family group
INSERT INTO Friendgroup(owner_email, fg_name, description)
VALUES ('AA@nyu.edu', 'family', "Ann's family");

INSERT INTO Belong(email, owner_email, fg_name)
VALUES ('AA@nyu.edu', 'AA@nyu.edu', 'family');

INSERT INTO Belong(email, owner_email, fg_name)
VALUES ('CC@nyu.edu', 'AA@nyu.edu', 'family');

INSERT INTO Belong(email, owner_email, fg_name)
VALUES ('DD@nyu.edu', 'AA@nyu.edu', 'family');

INSERT INTO Belong(email, owner_email, fg_name)
VALUES ('EE@nyu.edu', 'AA@nyu.edu', 'family');


-- Inserting into BB's family group
INSERT INTO Friendgroup(owner_email, fg_name, description)
VALUES ('BB@nyu.edu', 'family', "Bob's family");

INSERT INTO Belong(email, owner_email, fg_name)
VALUES ('BB@nyu.edu', 'BB@nyu.edu', 'family');

INSERT INTO Belong(email, owner_email, fg_name)
VALUES ('FF@nyu.edu', 'BB@nyu.edu', 'family');

INSERT INTO Belong(email, owner_email, fg_name)
VALUES ('EE@nyu.edu', 'BB@nyu.edu', 'family');


-- Inserting into AA's roomies group
INSERT INTO Friendgroup(owner_email, fg_name, description)
VALUES ('AA@nyu.edu', 'roommates', "Ann's Roomies");

INSERT INTO Belong(email, owner_email, fg_name)
VALUES ('AA@nyu.edu', 'AA@nyu.edu', 'roommates');

INSERT INTO Belong(email, owner_email, fg_name)
VALUES ('GG@nyu.edu', 'AA@nyu.edu', 'roommates');

INSERT INTO Belong(email, owner_email, fg_name)
VALUES ('HH@nyu.edu', 'AA@nyu.edu', 'roommates');


-- Inserting into HH's fiesta group
INSERT INTO Friendgroup(owner_email, fg_name, description)
VALUES ('HH@nyu.edu', 'Fiesta', "ITS A FIESTA BOIS");

INSERT INTO Belong(email, owner_email, fg_name)
VALUES ('HH@nyu.edu', 'HH@nyu.edu', 'Fiesta');

INSERT INTO Belong(email, owner_email, fg_name)
VALUES ('DD@nyu.edu', 'HH@nyu.edu', 'Fiesta');

INSERT INTO Belong(email, owner_email, fg_name)
VALUES ('CC@nyu.edu', 'HH@nyu.edu', 'Fiesta');

INSERT INTO Belong(email, owner_email, fg_name)
VALUES ('GG@nyu.edu', 'HH@nyu.edu', 'Fiesta');



-- Ann is posting a lot
INSERT INTO ContentItem(email_post, file_path, item_name, content_type, is_pub)
VALUES('AA@nyu.edu', NULL, 'AA1', 'text', True);
INSERT INTO ContentItem(email_post, file_path, item_name, content_type, is_pub)
VALUES('AA@nyu.edu', NULL, 'AA2', 'text', True);
INSERT INTO ContentItem(email_post, file_path, item_name, content_type, is_pub)
VALUES('AA@nyu.edu', NULL, 'AA3', 'text', True);
INSERT INTO ContentItem(email_post, file_path, item_name, content_type, is_pub)
VALUES('AA@nyu.edu', NULL, 'aa1', 'text', False);
INSERT INTO ContentItem(email_post, file_path, item_name, content_type, is_pub)
VALUES('AA@nyu.edu', NULL, 'aa2', 'text', False);
INSERT INTO ContentItem(email_post, file_path, item_name, content_type, is_pub)
VALUES('AA@nyu.edu', NULL, 'aa3', 'text', False);

-- BB is posting a lot
INSERT INTO ContentItem(email_post, file_path, item_name, content_type, is_pub)
VALUES('BB@nyu.edu', NULL, 'BB1', 'text', True);
INSERT INTO ContentItem(email_post, file_path, item_name, content_type, is_pub)
VALUES('BB@nyu.edu', NULL, 'BB2', 'text', True);
INSERT INTO ContentItem(email_post, file_path, item_name, content_type, is_pub)
VALUES('BB@nyu.edu', NULL, 'BB3', 'text', True);
INSERT INTO ContentItem(email_post, file_path, item_name, content_type, is_pub)
VALUES('BB@nyu.edu', NULL, 'bb1', 'text', False);
INSERT INTO ContentItem(email_post, file_path, item_name, content_type, is_pub)
VALUES('BB@nyu.edu', NULL, 'bb2', 'text', False);
INSERT INTO ContentItem(email_post, file_path, item_name, content_type, is_pub)
VALUES('BB@nyu.edu', NULL, 'bb3', 'text', False);

-- CC is posting a lot
INSERT INTO ContentItem(email_post, file_path, item_name, content_type, is_pub)
VALUES('CC@nyu.edu', NULL, 'CC1', 'text', True);
INSERT INTO ContentItem(email_post, file_path, item_name, content_type, is_pub)
VALUES('CC@nyu.edu', NULL, 'CC2', 'text', True);
INSERT INTO ContentItem(email_post, file_path, item_name, content_type, is_pub)
VALUES('CC@nyu.edu', NULL, 'CC3', 'text', True);
INSERT INTO ContentItem(email_post, file_path, item_name, content_type, is_pub)
VALUES('CC@nyu.edu', NULL, 'cc1', 'text', False);
INSERT INTO ContentItem(email_post, file_path, item_name, content_type, is_pub)
VALUES('CC@nyu.edu', NULL, 'cc2', 'text', False);
INSERT INTO ContentItem(email_post, file_path, item_name, content_type, is_pub)
VALUES('CC@nyu.edu', NULL, 'cc3', 'text', False);

-- DD is posting a lot
INSERT INTO ContentItem(email_post, file_path, item_name, content_type, is_pub)
VALUES('DD@nyu.edu', NULL, 'DD1', 'text', True);
INSERT INTO ContentItem(email_post, file_path, item_name, content_type, is_pub)
VALUES('DD@nyu.edu', NULL, 'DD2', 'text', True);
INSERT INTO ContentItem(email_post, file_path, item_name, content_type, is_pub)
VALUES('DD@nyu.edu', NULL, 'DD3', 'text', True);
INSERT INTO ContentItem(email_post, file_path, item_name, content_type, is_pub)
VALUES('DD@nyu.edu', NULL, 'dd1', 'text', False);
INSERT INTO ContentItem(email_post, file_path, item_name, content_type, is_pub)
VALUES('DD@nyu.edu', NULL, 'dd2', 'text', False);
INSERT INTO ContentItem(email_post, file_path, item_name, content_type, is_pub)
VALUES('DD@nyu.edu', NULL, 'dd3', 'text', False);

-- EE is posting a lot
INSERT INTO ContentItem(email_post, file_path, item_name, content_type, is_pub)
VALUES('EE@nyu.edu', NULL, 'EE1', 'text', True);
INSERT INTO ContentItem(email_post, file_path, item_name, content_type, is_pub)
VALUES('EE@nyu.edu', NULL, 'EE2', 'text', True);
INSERT INTO ContentItem(email_post, file_path, item_name, content_type, is_pub)
VALUES('EE@nyu.edu', NULL, 'EE3', 'text', True);
INSERT INTO ContentItem(email_post, file_path, item_name, content_type, is_pub)
VALUES('EE@nyu.edu', NULL, 'ee1', 'text', False);
INSERT INTO ContentItem(email_post, file_path, item_name, content_type, is_pub)
VALUES('EE@nyu.edu', NULL, 'ee2', 'text', False);
INSERT INTO ContentItem(email_post, file_path, item_name, content_type, is_pub)
VALUES('EE@nyu.edu', NULL, 'ee3', 'text', False);

-- FF is posting a lot
INSERT INTO ContentItem(email_post, file_path, item_name, content_type, is_pub)
VALUES('FF@nyu.edu', NULL, 'FF1', 'text', True);
INSERT INTO ContentItem(email_post, file_path, item_name, content_type, is_pub)
VALUES('FF@nyu.edu', NULL, 'FF2', 'text', True);
INSERT INTO ContentItem(email_post, file_path, item_name, content_type, is_pub)
VALUES('FF@nyu.edu', NULL, 'FF3', 'text', True);
INSERT INTO ContentItem(email_post, file_path, item_name, content_type, is_pub)
VALUES('FF@nyu.edu', NULL, 'ff1', 'text', False);
INSERT INTO ContentItem(email_post, file_path, item_name, content_type, is_pub)
VALUES('FF@nyu.edu', NULL, 'ff2', 'text', False);
INSERT INTO ContentItem(email_post, file_path, item_name, content_type, is_pub)
VALUES('FF@nyu.edu', NULL, 'ff3', 'text', False);

-- GG is posting a lot
INSERT INTO ContentItem(email_post, file_path, item_name, content_type, is_pub)
VALUES('GG@nyu.edu', NULL, 'GG1', 'text', True);
INSERT INTO ContentItem(email_post, file_path, item_name, content_type, is_pub)
VALUES('GG@nyu.edu', NULL, 'GG2', 'text', True);
INSERT INTO ContentItem(email_post, file_path, item_name, content_type, is_pub)
VALUES('GG@nyu.edu', NULL, 'GG3', 'text', True);
INSERT INTO ContentItem(email_post, file_path, item_name, content_type, is_pub)
VALUES('GG@nyu.edu', NULL, 'gg1', 'text', False);
INSERT INTO ContentItem(email_post, file_path, item_name, content_type, is_pub)
VALUES('GG@nyu.edu', NULL, 'gg2', 'text', False);
INSERT INTO ContentItem(email_post, file_path, item_name, content_type, is_pub)
VALUES('GG@nyu.edu', NULL, 'gg3', 'text', False);

-- Testing Tag case :)
INSERT INTO tag (email_tagged, email_tagger, item_id, status)
VALUES ('CC@nyu.edu', 'FF@nyu.edu', 31, 'True');

INSERT INTO tag (email_tagged, email_tagger, item_id, status)
VALUES('AA@nyu.edu', 'CC@nyu.edu', 31, 'True');