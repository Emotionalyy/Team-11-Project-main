USE agri_proj;

-- -------------------------------------------------------- --

-- 统一删除表
-- USE agri_proj;
-- DROP TABLE IF EXISTS Sensor_Maintenance;
-- DROP TABLE IF EXISTS Sensors;
-- DROP TABLE IF EXISTS Fertilization;
-- DROP TABLE IF EXISTS Agri_Mach_Use;
-- DROP TABLE IF EXISTS Agri_Mach;
-- DROP TABLE IF EXISTS Weather;
-- DROP TABLE IF EXISTS Headwaters_Status;
-- DROP TABLE IF EXISTS Air_Status;
-- DROP TABLE IF EXISTS Soil_Status;
-- DROP TABLE IF EXISTS Fields;
-- DROP TABLE IF EXISTS Users;

-- -------------------------------------------------------- --

-- 用户数据
-- 包括【用户信息】

-- 用户信息表 Users
DROP TABLE IF EXISTS Users;
CREATE TABLE Users
(
    `user_id`   INT         NOT NULL UNIQUE AUTO_INCREMENT COMMENT "用户自增ID",
    `is_admin`  BOOLEAN     NOT NULL COMMENT "是否为管理员",
    `user_name` VARCHAR(10) NOT NULL UNIQUE COMMENT "用户名，应只有英文与数字",
    `password`  CHAR(32)    NOT NULL COMMENT "用户密码，用32位MD5加密",
    `name`      VARCHAR(20) COMMENT "用户昵称",
    `note`      VARCHAR(100) COMMENT "备注信息",
    `available` BOOLEAN NOT NULL DEFAULT 1 COMMENT "用户是否可用",
    PRIMARY KEY (`user_id`)
);

INSERT INTO Users (`is_admin`, `user_name`, `password`, `name`, `note`)
VALUES (TRUE, 'niugiegie', MD5('123456'), 'NiuDie', '最屌的那个'),
       (FALSE, 'jiafw', MD5('666666'), 'XiaoxiJia', '小弟'),
       (FALSE, 'jiangbao', MD5('888888'), 'XinyuanJiang', '徒弟');


-- -------------------------------------------------------- --

-- 农田与检测数据
-- 包括【农田信息】、【土壤湿度】、【空气湿度、温度】、【水源情况】

-- 农田信息表 Fields
DROP TABLE IF EXISTS Fields;
CREATE TABLE Fields
(
    `field_id` INT   NOT NULL UNIQUE AUTO_INCREMENT COMMENT "农田自增ID",
    `area`     FLOAT NOT NULL COMMENT "农田面积，公顷",
    `crop`     VARCHAR(10) COMMENT "作物信息"
    `note`     VARCHAR(100) COMMENT "备注信息",
    PRIMARY KEY (`field_id`)
);

INSERT INTO Fields
VALUES (1, 1.23, "番茄", NULL);
INSERT INTO Fields
VALUES (2, 1.12, "草莓", NULL);
INSERT INTO Fields
VALUES (3, 2.12, "黄瓜", NULL);
INSERT INTO Fields
VALUES (4, 3.86, "玉米", NULL);
INSERT INTO Fields
VALUES (5, 1.56, "茄子", NULL);
INSERT INTO Fields
VALUES (6, 1.94, "丝瓜", NULL);
INSERT INTO Fields
VALUES (7, 1.52, "水稻", NULL);
INSERT INTO Fields
VALUES (8, 1.42, "水稻", NULL);
INSERT INTO Fields
VALUES (9, 1.66, "水稻", NULL);

-- 土壤状态表 Soil_Status
DROP TABLE IF EXISTS Soil_Status;
CREATE TABLE Soil_Status
(
    `field_id` INT       NOT NULL COMMENT "农田ID",
    `time`     TIMESTAMP NOT NULL COMMENT "检测时间戳",
    `moisture` DOUBLE    NOT NULL COMMENT "土壤湿度小数，体积含水量，在0-1之间",
    FOREIGN KEY (`field_id`) REFERENCES Fields (`field_id`),
    PRIMARY KEY (`field_id`, `time`)
);

-- 空气状态表 Air_Status
DROP TABLE IF EXISTS Air_Status;
CREATE TABLE Air_Status
(
    `field_id`    INT       NOT NULL COMMENT "农田ID",
    `time`        TIMESTAMP NOT NULL COMMENT "检测时间戳",
    `humidity`    DOUBLE    NOT NULL COMMENT "空气湿度百分数，在0-100之间",
    `temperature` DOUBLE    NOT NULL COMMENT "空气温度，摄氏度",
    FOREIGN KEY (`field_id`) REFERENCES Fields (`field_id`),
    PRIMARY KEY (`field_id`, `time`)
);

-- 水源状态表 Headwaters_Status
DROP TABLE IF EXISTS Headwaters_Status;
CREATE TABLE Headwaters_Status
(
    `field_id`        INT       NOT NULL COMMENT "农田ID",
    `time`            TIMESTAMP NOT NULL COMMENT "检测时间戳",
    `ph`              DOUBLE COMMENT "水源pH值，例6.0 - 7.5",
    `hardness`        DOUBLE COMMENT "水源硬度，例50 - 150 mg/L（以CaCO3计）",
    `solids`          DOUBLE COMMENT "总溶解固体，例< 500 mg/L",
    `chloramines`     DOUBLE COMMENT "氯胺，例< 4 mg/L",
    `sulfate`         DOUBLE COMMENT "硫酸盐，例< 200 mg/L",
    `conductivity`    DOUBLE COMMENT "电导率，例< 750 µS/cm",
    `organic_carbon`  DOUBLE COMMENT "有机碳，例< 2 mg/L",
    `trihalomethanes` DOUBLE COMMENT "三卤甲烷，例< 0.08 mg/L",
    `turbidity`       DOUBLE COMMENT "浊度，例< 5 NTU",
    `potability`      BOOLEAN   NOT NULL COMMENT "可饮用性",
    FOREIGN KEY (`field_id`) REFERENCES Fields (`field_id`),
    PRIMARY KEY (`field_id`, `time`)
);

-- -------------------------------------------------------- --

-- 气象数据
-- 包括【气象数据】

-- 气象数据表 Weather
DROP TABLE IF EXISTS Weather;
CREATE TABLE Weather
(
    `time`       TIMESTAMP   NOT NULL COMMENT "检测时间戳",
    `temp`       DOUBLE      NOT NULL COMMENT "温度",
    `text`       VARCHAR(5)  NOT NULL COMMENT "天气描述，如阴、晴、雨、雪等",
    `wind_dir`   VARCHAR(10) NOT NULL COMMENT "风向，枚举值：北风、东北风、东风、东南风、南风、西南风、西风、西北风、旋转风、无持续风向",
    `wind_scale` INT         NOT NULL COMMENT "风力等级，12级依次指代无风、软风、轻风、微风、和风、清风、强风、疾风、大风、烈风、狂风、暴风、飓风",
    `wind_speed` INT         NOT NULL COMMENT "风速，公里/小时",
    `humidity`   DOUBLE      NOT NULL COMMENT "相对湿度，0-1之间小数",
    `precip`     DOUBLE      NOT NULL COMMENT "当前小时累计降水量，毫米",
    `pressure`   INT         NOT NULL COMMENT "大气压强，百帕",
    `vis`        INT         NOT NULL COMMENT "能见度，公里",
    `cloud`      INT COMMENT "云量，0-100百分比数值",
    `dew`        INT COMMENT "露点温度，摄氏度",
    PRIMARY KEY (`time`)
);

-- -------------------------------------------------------- --

-- 农田和农机数据
-- 包括【农机信息】、【农机使用信息】、【施肥记录】

-- 农机信息表 Agri_Mach
-- 指标-维护状态 是否三个月内维护过
DROP TABLE IF EXISTS Agri_Mach;
CREATE TABLE Agri_Mach
(
    `mach_id`     INT         NOT NULL UNIQUE AUTO_INCREMENT COMMENT "农机递增ID",
    `name`        VARCHAR(10) NULL COMMENT "农机名称",
    `usage`       VARCHAR(5)  NOT NULL COMMENT "枚举值，耕种、播种、施肥、灌溉、收割、运输、土地整理和修建、畜牧业、农产品处理",
    `mach_status` BOOLEAN     NOT NULL COMMENT "农机状态，0为未在使用，1为正在使用",
    PRIMARY KEY (`mach_id`)
);

INSERT INTO Agri_Mach (`usage`, `name`, `mach_status`)
VALUES ('农产品处理', "作物处理1号", 0),
       ('播种', "播种农机1号", 1),
       ('施肥', "施肥农机1号", 0),
       ('灌溉', "洒水农机1号", 1),
       ('畜牧业', "放牧监管1号", 0),
       ('收割', "收割机", 1),
       ('施肥', "施肥农机2号", 1),
       ('耕种', "播种机", 1),
       ('农产品处理', "作物处理2号", 1);

-- 农机使用信息表 Agri_Mach_Use
DROP TABLE IF EXISTS Agri_Mach_Use;
CREATE TABLE Agri_Mach_Use
(
    `id`          INT         NOT NULL UNIQUE AUTO_INCREMENT COMMENT "农机使用事件递增ID",
    `mach_id`     INT         NOT NULL COMMENT "农机ID",
    `user_id`     INT         NOT NULL COMMENT "施肥用户ID",
    `date`        DATE        NOT NULL COMMENT "农机使用日期",
    `note`        VARCHAR(50) NOT NULL COMMENT "农机使用情况备注",
    `main_status` BOOLEAN     NOT NULL COMMENT "当次使用后是否进行维护",
    FOREIGN KEY (`user_id`) REFERENCES Users (`user_id`),
    FOREIGN KEY (`mach_id`) REFERENCES Agri_Mach (`mach_id`),
    PRIMARY KEY (`id`)
);

INSERT INTO Agri_Mach_Use(`mach_id`, `user_id`, `date`, `note`, `main_status`)
VALUES (1, 1, '1978-05-01', '使用情况良好', TRUE),
       (2, 2, '1949-02-23', '需要小型维护', FALSE),
       (3, 3, '2024-09-30', '操作顺利', TRUE),
       (4, 1, '2003-10-25', '需要更换零件', FALSE),
       (5, 2, '1869-06-10', '表现正常', TRUE),
       (6, 1, '2013-11-15', '表现正常', FALSE),
       (7, 1, '2023-09-24', '表现正常', FALSE),
       (8, 1, '2014-10-24', '表现正常', FALSE),
       (9, 1, '2024-03-16', '表现正常', FALSE);

-- 施肥信息表 Fertilization
-- 指标-施肥数量 密度*农田面积
-- 指标-下次施肥时间 
DROP TABLE IF EXISTS Fertilization;
CREATE TABLE Fertilization
(
    `id`       INT  NOT NULL UNIQUE AUTO_INCREMENT COMMENT "施肥事件递增ID",
    `user_id`  INT  NOT NULL COMMENT "施肥用户ID",
    `field_id` INT  NOT NULL COMMENT "农田ID",
    `date`     DATE NOT NULL COMMENT "施肥日期",
    `type`     VARCHAR(10) COMMENT "肥料种类",
    `density`  FLOAT COMMENT "施肥密度，kg/公顷",
    `note`     VARCHAR(100) COMMENT "备注信息",
    FOREIGN KEY (`user_id`) REFERENCES Users (`user_id`),
    FOREIGN KEY (`field_id`) REFERENCES Fields (`field_id`),
    PRIMARY KEY (`id`)
);

INSERT INTO Fertilization (`user_id`, `field_id`, `date`, `type`, `density`, `note`)
VALUES (1, 1, '2002-05-01', '有机肥', 150.0, '施肥效果良好'),
       (2, 2, '1987-09-12', '化肥', 200.0, '需进一步观察'),
       (3, 3, '2024-05-25', '复合肥', 180.0, '操作顺利'),
       (1, 4, '1849-10-12', '有机肥', 160.0, '需要补充施肥'),
       (2, 5, '2015-12-05', '化肥', 190.0, '表现正常');

-- -------------------------------------------------------- --

-- 传感器数据
-- 包括【传感器信息】、【传感器维护记录】

-- 传感器信息表 Sensors
DROP TABLE IF EXISTS Sensors;
CREATE TABLE Sensors
(
    `sensor_id` INT         NOT NULL UNIQUE AUTO_INCREMENT COMMENT "传感器递增ID",
    `field_id`  INT         NOT NULL COMMENT "农田ID，传感器所在农田",
    `name`      VARCHAR(10) NULL COMMENT "传感器名称",
    `type`      VARCHAR(10) NOT NULL COMMENT "传感器类型",
    `status`    BOOLEAN     NOT NULL COMMENT "传感器状态，是否可用",
    FOREIGN KEY (`field_id`) REFERENCES Fields (`field_id`),
    PRIMARY KEY (`sensor_id`)
);

INSERT INTO Sensors
VALUES (1, 1, "水源检测传感器", "headwaters", 1);
INSERT INTO Sensors
VALUES (2, 2, "水源检测传感器", "headwaters", 1);
INSERT INTO Sensors
VALUES (3, 3, "水源检测传感器", "headwaters", 1);
INSERT INTO Sensors
VALUES (4, 1, "农田空气传感器", "air", 1);
INSERT INTO Sensors
VALUES (5, 2, "农田空气传感器", "air", 1);
INSERT INTO Sensors
VALUES (6, 3, "农田空气传感器", "air", 1);
INSERT INTO Sensors
VALUES (7, 1, "土壤信息传感器", "soil", 1);
INSERT INTO Sensors
VALUES (8, 2, "土壤信息传感器", "soil", 1);
INSERT INTO Sensors
VALUES (9, 3, "土壤信息传感器", "soil", 1);
INSERT INTO Sensors
VALUES (10, 4, "水源检测传感器", "headwaters", 1);
INSERT INTO Sensors
VALUES (11, 5, "水源检测传感器", "headwaters", 1);
INSERT INTO Sensors
VALUES (12, 6, "水源检测传感器", "headwaters", 1);
INSERT INTO Sensors
VALUES (13, 7, "水源检测传感器", "headwaters", 1);
INSERT INTO Sensors
VALUES (14, 8, "水源检测传感器", "headwaters", 1);
INSERT INTO Sensors
VALUES (15, 5, "农田空气传感器", "air", 1);
INSERT INTO Sensors
VALUES (16, 7, "农田空气传感器", "air", 1);
INSERT INTO Sensors
VALUES (17, 8, "农田空气传感器", "air", 1);
INSERT INTO Sensors
VALUES (18, 9, "农田空气传感器", "air", 1);
INSERT INTO Sensors
VALUES (19, 4, "土壤信息传感器", "soil", 1);
INSERT INTO Sensors
VALUES (20, 5, "土壤信息传感器", "soil", 1);
INSERT INTO Sensors
VALUES (21, 6, "土壤信息传感器", "soil", 1);
INSERT INTO Sensors
VALUES (22, 7, "土壤信息传感器", "soil", 1);
INSERT INTO Sensors
VALUES (23, 8, "土壤信息传感器", "soil", 1);
INSERT INTO Sensors
VALUES (24, 9, "土壤信息传感器", "soil", 1);

-- 传感器维护信息表 Sensor_Maintenance
DROP TABLE IF EXISTS Sensor_Maintenance;
CREATE TABLE Sensor_Maintenance
(
    `id`        INT  NOT NULL UNIQUE AUTO_INCREMENT COMMENT "传感器维护事件递增ID",
    `sensor_id` INT  NOT NULL COMMENT "传感器ID",
    `date`      DATE NOT NULL COMMENT "传感器维护时间",
    FOREIGN KEY (`sensor_id`) REFERENCES Sensors (`sensor_id`),
    PRIMARY KEY (`id`)
);

INSERT INTO Sensor_Maintenance (`sensor_id`, `date`)
VALUES (1, '1734-05-01'),
       (2, '2003-05-15'),
       (3, '1902-06-02'),
       (4, '2024-06-20'),
       (5, '1895-07-10'),
       (1, '1995-05-23'),
       (2, '2000-12-11'),
       (3, '2022-07-18'),
       (4, '1985-09-22'),
       (5, '2010-03-15'),
       (6, '1998-11-05'),
       (1, '1974-06-20'),
       (2, '2015-08-14'),
       (3, '2021-02-02'),
       (4, '2007-04-25'),
       (5, '1980-01-01'),
       (6, '1990-10-10'),
       (1, '2002-12-24'),
       (2, '2019-11-30'),
       (3, '1996-03-08'),
       (4, '2013-05-06'),
       (5, '2008-07-19'),
       (6, '1983-02-15'),
       (1, '2020-12-01'),
       (2, '2005-06-17'),
       (3, '1993-09-29'),
       (4, '2017-04-03'),
       (5, '1999-11-20'),
       (6, '2012-08-12'),
       (1, '2003-10-05'),
       (2, '2023-01-28'),
       (3, '1987-05-18'),
       (4, '2018-02-09'),
       (5, '1994-06-30'),
       (6, '2011-09-27'),
       (1, '1982-11-21'),
       (2, '2009-03-16'),
       (3, '1997-08-05'),
       (4, '2014-10-22'),
       (5, '1988-07-01'),
       (6, '2006-12-13'),
       (1, '2021-06-04'),
       (2, '2001-09-15'),
       (3, '1992-04-09'),
       (4, '2016-11-29'),
       (5, '1984-01-10'),
       (6, '2004-02-26'),
       (1, '2022-03-07'),
       (2, '2010-05-20'),
       (3, '1991-08-25'),
       (4, '2018-12-19'),
       (5, '1986-02-02'),
       (6, '2007-11-03'),
       (1, '2015-01-12'),
       (2, '2020-08-22'),
       (3, '1998-04-13'),
       (4, '2013-06-28'),
       (5, '2000-07-05'),
       (6, '1995-09-10'),
       (1, '2023-12-25'),
       (2, '2008-11-27'),
       (3, '2019-04-21'),
       (4, '1996-02-08'),
       (5, '2012-09-30'),
       (6, '1981-10-14'),
       (1, '2017-07-15'),
       (2, '1993-01-09'),
       (3, '2005-10-20'),
       (4, '2021-05-22'),
       (5, '1990-06-12'),
       (6, '2014-11-08'),
       (1, '2009-08-17'),
       (2, '1983-02-19'),
       (3, '2016-03-03'),
       (4, '1999-12-15'),
       (5, '2023-06-18'),
       (6, '1985-05-04'),
       (1, '2018-09-01'),
       (2, '1987-07-25'),
       (3, '2020-10-11'),
       (4, '1994-03-30'),
       (5, '2011-12-07'),
       (6, '1997-05-28'),
       (1, '2022-08-15'),
       (2, '1989-09-19'),
       (3, '2006-04-02'),
       (4, '2010-01-21'),
       (5, '2002-07-07'),
       (6, '1991-11-13'),
       (1, '2019-03-24'),
       (2, '1984-12-04'),
       (3, '2015-06-13'),
       (4, '2000-03-11'),
       (5, '2021-01-30'),
       (6, '1996-08-27'),
       (1, '2013-10-16'),
       (2, '2023-07-26');