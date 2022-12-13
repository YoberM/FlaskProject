INSERT INTO 'persona' ('persona_id','nombre','apellidos','correo','contrasenia','telefono','direccion') VALUES
('1','Jaime','Zuniga','Jaime@gmail.com','jaime123','987654321','Av Estados Unidos'),
('2','Tommy','Garcia','Tommy@gmail.com','tommy123','987321654','Av Dolores'),
('3','Juan','Rodriguez','Juan@gmail.com','juan123','978563412','Av Goyoneche');
INSERT INTO 'trabajador' ('trabajador_id','tipo','sueldo') VALUES
('3','Mesero','1030');
INSERT INTO 'cliente' ('cliente_id') VALUES
('1'),
('2');
INSERT INTO 'platillo' ('platillo_id','nombre','costo_venta','costo_prepa') VALUES
('1000','Lomo Saltado','8','5'),
('1001','Lomo Saltado a lo pobre','10','7'),
('1002','Saltado de Pollo','7','4');
INSERT INTO 'estado' ('estado_id','nombre') VALUES
('10','En preparacion'),
('11','En espera'),
('12','Esperando orden'),
('13','Terminado');
INSERT INTO 'pedido' ('pedido_id','numero_mesa','fecha','estado_id','cliente_id') VALUES
('1','3','22 Nov','13','1'),
('2','5','21 Nov','13','2');
INSERT INTO 'pedido_platillo' ('pedido_id_pedido','platillo_id_platillo','cantidad') VALUES
('1','1000','1'),
('1','1002','1'),
('2','1001','2'),
('2','1002','1');