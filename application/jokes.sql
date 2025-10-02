CREATE TABLE joke (
id int PRIMARY KEY auto_increment,
question varchar(250) not null,
punchline varchar (250) default null
);

INSERT into joke (question,punchline)
values
("Why do programmers prefer dark mode?","Because light attracts bugs."),
("Why do Java developers wear glasses?", "Because they don't C#."),
("What’s a programmer’s favorite hangout place?","The Foo Bar."),
("Why don't programmers go out?","Because they're stuck in a virtual environment.");

CREATE table users(
id int PRIMARY KEY auto_increment,
username varchar(150) not null,
hashed_password varchar(250) not null
);

INSERT into users(username) values ('aiman');