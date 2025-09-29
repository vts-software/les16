create table if not exists authors(
id serial primary key,
name varchar(255) not null
);

create table if not exists genres(
id serial primary key,
name varchar(50) not null
);

create table if not exists books(
id serial primary key,
name varchar(255) not null,
year int not null,
description varchar
);

create table if not exists books_authors(
book_id int not null,
author_id int not null,
primary key (book_id, author_id),
constraint fk_book foreign key (book_id) references book(id) on delete cascade,
constraint fk_authors foreign key (author_id) references authors(id) on delete cascade
);

create table if not exists book_genres(
book_id int not null,
genres_id int not null,
primary key (book_id, genres_id),
constraint fk_book foreign key (book_id) references book(id) on delete cascade,
constraint fk_genres foreign key (genres_id) references genres(id) on delete cascade
);