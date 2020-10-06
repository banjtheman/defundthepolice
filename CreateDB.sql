CREATE TABLE budget_data (id SERIAL PRIMARY KEY, state char(2),county varchar(50), year int,item varchar(100), budget int, source varchar(150));

COPY budget_data(state, county, year, item, budget, source) FROM '/tmp/allbudgets.csv' DELIMITER ',' CSV HEADER;
