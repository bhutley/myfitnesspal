
create table food (
       food_id integer primary key,
       dt date not null,
       meal varchar(60) not null,
       food varchar(300) not null,
       calories float,
       carbs float,
       fat float,
       protein float,
       sodium float,
       sugar float
       );

create index x_f_dt on food(dt);
create index x_f_dt_meal on food(dt, meal);
create index x_f_food on food(food);
