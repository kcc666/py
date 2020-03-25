

-- 创建一个学生表
create table students(
id int unsigned primary key auto_increment not null,
name varchar(20) default "",
age tinyint unsigned default 0,
height decimal(5,2),
gender enum("男","女","中性","保密") default "保密",
cls_id int unsigned default 0,
is_delete bit default 0
);

-- 创建一个班级表
create table class(
id int unsigned primary key auto_increment not null,
name varchar (30) not null
);


-- 插入学生数据
insert into students values
(0,'小明',18,180.00,2,1,0),
(0,'小月月',18,180.00,2,2,1),
(0,'彭于晏',29,185.00,1,1,0),
(0,'刘德华',59,175.00,1,2,1),
(0,'黄蓉',38,160.00,2,1,0),
(0,'凤姐',28,150.00,4,2,1),
(0,'王祖贤',18,172.00,2,1,1),
(0,'周杰伦',36,NULL,1,1,0),
(0,'程坤',27,181.00,1,2,0),
(0,'刘亦菲',25,166.00,2,2,0),
(0,'金星',33,162.00,3,3,1),
(0,'静香',12,180.00,2,4,0),
(0,'郭靖',12,170.00,1,4,0),
(0,'周杰',34,176.00,2,5,0)

-- 插入班级数据
insert into class values
(0,"中一班"),
(0,"中二班"),
(0,"中三班"),
(0,"中四班"),
(0,"中五班");

-- 查询指定字段
select name,age from students;

-- 给字段起别名
select name as "姓名",age as "年龄" from students;

-- 去重的方式查询数据
select distinct gender from students;

-- 查询大于18岁的信息
select name,age from students where age>18;

-- 查询所有大于18小于28的信息
select * from students where age>18 and age<28;

-- 查询所有18以上或者身高大于180的
select * from students where age>18 or height>180;

-- 18以上的女性
select * from students where age>18 and gender="女";

-- 年龄不是18以上的女性
select * from students where not age>=18;

-- 查询名字以小开头的信息
select name from students where name like "小%";

-- 查询名字是两个字开头的信息
select name from students where name like "__";

-- 查询至少有两个字的名字
select name from students where name like "__%";

-- 查询以周开始,伦结尾的姓名
select name from students where name like "周%伦";

-- 查询以周开头的姓名
select name from students where name rlike "周.*";

-- 范围查询
select name,age from students where age in (12,18,34);

insert into Tway values(
        0,
        "LJ888999"
        );