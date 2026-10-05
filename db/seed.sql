INSERT INTO categories (name) VALUES
('Электроника'),('Одежда'),('Книги'),('Бытовая техника');

INSERT INTO products (sku, name, category_id, price, stock) VALUES
('SKU001','Наушники Sony', 1, 15000, 20),
('SKU002','iPhone 15', 1, 90000, 5),
('SKU003','Футболка белая', 2, 1500, 100),
('SKU004','Джинсы синие', 2, 4500, 50),
('SKU005','SQL для профессионалов', 3, 2000, 200),
('SKU006','Python Cookbook', 3, 2500, 150),
('SKU007','Пылесос Dyson', 4, 45000, 10),
('SKU008','Кофемашина', 4, 30000, 15);

INSERT INTO tags (name) VALUES ('хит'),('новинка'),('скидка'),('премиум');
INSERT INTO product_tags (product_id, tag_id) VALUES
(2,1),(2,4),(3,2),(7,4),(7,1);
