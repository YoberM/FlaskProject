-- ---
-- Globals
-- ---

-- SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
-- SET FOREIGN_KEY_CHECKS=0;

-- ---
-- Table 'persona'
--
-- ---

DROP TABLE IF EXISTS 'persona';

CREATE TABLE 'persona' (
  'persona_id' INTEGER,
  'nombre' VARCHAR(50) NULL DEFAULT NULL,
  'apellidos' VARCHAR(50) NULL DEFAULT NULL,
  'correo' VARCHAR(50) NULL DEFAULT NULL,
  'contrasenia' VARCHAR(50) NULL DEFAULT NULL,
  'telefono' INTEGER NULL DEFAULT NULL,
  'direccion' VARCHAR(50) NULL DEFAULT NULL,
  PRIMARY KEY ('persona_id')
);

DROP TABLE IF EXISTS 'cliente';

CREATE TABLE 'cliente' (
  'cliente_id' INTEGER ,
  FOREIGN KEY ('cliente_id') REFERENCES persona,
  PRIMARY KEY ('cliente_id')
);

DROP TABLE IF EXISTS 'trabajador';

CREATE TABLE 'trabajador' (
  'trabajador_id' INTEGER NULL DEFAULT NULL,
  'tipo' VARCHAR(50) NULL DEFAULT NULL,
  'sueldo' INTEGER NULL DEFAULT NULL,
  PRIMARY KEY ('trabajador_id'),
  FOREIGN KEY ('trabajador_id') REFERENCES 'persona' ('persona_id')
);
-- ---
-- Table 'pedido'
--
-- ---

DROP TABLE IF EXISTS 'estado';

CREATE TABLE 'estado' (
  'estado_id' INTEGER NULL DEFAULT NULL,
  'nombre' INTEGER NULL DEFAULT NULL,
  PRIMARY KEY ('estado_id')
);

DROP TABLE IF EXISTS 'pedido';

CREATE TABLE 'pedido' (
  'pedido_id' INTEGER NULL DEFAULT NULL,
  'numero_mesa' INTEGER NULL DEFAULT NULL,
  'fecha' VARCHAR NULL DEFAULT NULL,
  'estado_id' INTEGER NULL DEFAULT NULL,
  'cliente_id' INTEGER NULL DEFAULT NULL,
  PRIMARY KEY ('pedido_id'),
  FOREIGN KEY ('estado_id') REFERENCES 'estado' ('estado_id'),
  FOREIGN KEY ('cliente_id') REFERENCES 'cliente' ('cliente_id')
);

-- ---
-- Table 'platillo'
--
-- ---

DROP TABLE IF EXISTS 'platillo';

CREATE TABLE 'platillo' (
  'platillo_id' INTEGER NULL DEFAULT NULL,
  'nombre' VARCHAR(50) NULL DEFAULT NULL,
  'costo_venta' INTEGER NULL DEFAULT NULL,
  'costo_prepa' INTEGER NULL DEFAULT NULL,
  PRIMARY KEY ('platillo_id')
);

-- ---
-- Table 'pedido_platillo'
--
-- ---

DROP TABLE IF EXISTS 'pedido_platillo';

CREATE TABLE 'pedido_platillo' (
  'pedido_id_pedido' INTEGER NULL DEFAULT NULL,
  'platillo_id_platillo' INTEGER NULL DEFAULT NULL,
  'cantidad' INTEGER NULL DEFAULT NULL,
  PRIMARY KEY ('pedido_id_pedido', 'platillo_id_platillo'),
  FOREIGN KEY ('pedido_id_pedido') REFERENCES 'pedido' ('pedido_id'),
  FOREIGN KEY ('platillo_id_platillo') REFERENCES 'platillo' ('platillo_id')
);
