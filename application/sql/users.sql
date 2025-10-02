CREATE table users(
id int PRIMARY KEY auto_increment,
username varchar(150) not null,
hashed_password varchar(250) not null
);