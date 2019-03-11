CREATE TABLE users(
    sender_id VARCHAR(8) PRIMARY KEY,
    username VARCHAR(50) NOT NULL
);

CREATE TABLE messages(
    message_id VARCHAR(25) PRIMARY KEY,
    sender_id VARCHAR(8) NOT NULL,
    text_contents VARCHAR(1000),
    num_likes INTEGER NOT NULL,
    attachment_url VARCHAR(100) DEFAULT NULL,
    FOREIGN KEY (sender_id) REFERENCES users(sender_id)
);