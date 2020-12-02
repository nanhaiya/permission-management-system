-- 用户表 	// 密码（MD5加密）
insert into
	tab_user (username, password, gender, birthday, telephone, remark)
values
	('root', '63a9f0ea7bb98050796b649e85481845', '男', '1998-08-04', '18574394525', null),	-- 密码 root
	('lisa', '202cb962ac59075b964b07152d234b70', '女', '1995-12-15', '18375497258', null);	-- 密码 123


-- 角色表
INSERT INTO
	tab_role (name)
VALUES
	('管理员'),
	('普通用户');