/*
 Navicat Premium Data Transfer

 Source Server         : mysql
 Source Server Type    : MySQL
 Source Server Version : 50727
 Source Host           : localhost:3306
 Source Schema         : ebds_demo

 Target Server Type    : MySQL
 Target Server Version : 50727
 File Encoding         : 65001

 Date: 18/11/2019 10:00:38
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Procedure structure for fake_dms_dpt_avg
-- ----------------------------
DROP PROCEDURE IF EXISTS `fake_dms_dpt_avg`;
delimiter //
CREATE DEFINER=`root`@`localhost` PROCEDURE `fake_dms_dpt_avg`()
BEGIN
	INSERT INTO dms_dpt_avg(a_efficiency, a_accuracy, a_workhour, time)
	SELECT AVG(efficiency) AS a_efficiency, AVG(accuracy) AS a_accuracy, AVG(workhour) AS a_workhour, MAX(time) AS `time` FROM dms_dpt_online;
END
//
delimiter ;

-- ----------------------------
-- Procedure structure for fake_dms_dpt_daily
-- ----------------------------
DROP PROCEDURE IF EXISTS `fake_dms_dpt_daily`;
delimiter //
CREATE DEFINER=`root`@`localhost` PROCEDURE `fake_dms_dpt_daily`()
BEGIN
	INSERT INTO dms_dpt_daily(efficiency, accuracy, workhour, time)
	SELECT AVG(efficiency) AS efficiency, AVG(accuracy) AS accuracy, AVG(workhour) AS workhour, time AS `time` 
	FROM dms_workshop_daily GROUP BY time;
END
//
delimiter ;

-- ----------------------------
-- Procedure structure for fake_dms_dpt_online
-- ----------------------------
DROP PROCEDURE IF EXISTS `fake_dms_dpt_online`;
delimiter //
CREATE DEFINER=`root`@`localhost` PROCEDURE `fake_dms_dpt_online`()
BEGIN
	INSERT INTO dms_dpt_online(efficiency, accuracy, workhour, time)
	SELECT AVG(efficiency) AS efficiency, AVG(accuracy) AS accuracy, AVG(workhour) AS workhour, time AS `time` 
	FROM dms_workshop_online GROUP BY time;
END
//
delimiter ;

-- ----------------------------
-- Procedure structure for fake_dms_group_avg
-- ----------------------------
DROP PROCEDURE IF EXISTS `fake_dms_group_avg`;
delimiter //
CREATE DEFINER=`root`@`localhost` PROCEDURE `fake_dms_group_avg`()
BEGIN
	DECLARE `cur_group_id` VARCHAR(255);

	DECLARE done INT DEFAULT false; -- 结束标志
	DECLARE group_id_cursor CURSOR FOR SELECT DISTINCT group_id FROM dms_group_online; -- 定义游标
	
	DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = true;  
	OPEN group_id_cursor;
	read_loop:LOOP 
			FETCH group_id_cursor INTO `cur_group_id`;
			-- 判断游标的循环是否结束  
			IF done THEN  
				LEAVE read_loop;
			END IF; 
			
			INSERT INTO dms_group_avg(group_id, a_efficiency, a_accuracy, a_workhour, time)
			SELECT cur_group_id AS group_id, AVG(efficiency) AS efficiency, AVG(accuracy) AS accuracy, AVG(workhour) AS workhour, MAX(time) AS `time`
			FROM dms_group_online WHERE group_id=cur_group_id; 
			
	END LOOP;
	CLOSE group_id_cursor; -- 关闭stat_id游标

END
//
delimiter ;

-- ----------------------------
-- Procedure structure for fake_dms_group_online
-- ----------------------------
DROP PROCEDURE IF EXISTS `fake_dms_group_online`;
delimiter //
CREATE DEFINER=`root`@`localhost` PROCEDURE `fake_dms_group_online`()
BEGIN
	DECLARE `cur_time` VARCHAR(255);

	DECLARE done INT DEFAULT false; -- 结束标志
	DECLARE cur_time_cursor CURSOR FOR SELECT DISTINCT(time) FROM dms_team_online; -- 定义游标
	
	DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = true;  
	OPEN cur_time_cursor;
	read_loop:LOOP 
			FETCH cur_time_cursor INTO `cur_time`;
			-- 判断游标的循环是否结束  
			IF done THEN  
				LEAVE read_loop;
			END IF; 
			
			INSERT INTO dms_group_online(group_id, efficiency, accuracy, workhour, time)
			SELECT w.group_id AS group_id, AVG(o.efficiency) AS efficiency, AVG(o.accuracy) AS accuracy, AVG(o.workhour) AS workhour, `cur_time` AS `time`
			FROM dms_team_online AS o JOIN sms_team_group_workshop AS w ON o.team_id=w.team_id 
			WHERE o.time=`cur_time`
			GROUP BY w.group_id;

	END LOOP;
	CLOSE cur_time_cursor; -- 关闭stat_id游标

END
//
delimiter ;

-- ----------------------------
-- Procedure structure for fake_dms_stat_avg
-- ----------------------------
DROP PROCEDURE IF EXISTS `fake_dms_stat_avg`;
delimiter //
CREATE DEFINER=`root`@`localhost` PROCEDURE `fake_dms_stat_avg`()
BEGIN
	DECLARE `cur_stat_id` VARCHAR(255);

	DECLARE done INT DEFAULT false; -- 结束标志
	DECLARE stat_id_cursor CURSOR FOR SELECT DISTINCT stat_id FROM dms_stat_online; -- 定义游标
	
	DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = true;  
	OPEN stat_id_cursor;
	read_loop:LOOP 
			FETCH stat_id_cursor INTO `cur_stat_id`;
			-- 判断游标的循环是否结束  
			IF done THEN  
				LEAVE read_loop;
			END IF; 
			
			INSERT INTO dms_stat_avg(stat_id, a_efficiency, a_accuracy, a_workhour, time)
			SELECT cur_stat_id, AVG(efficiency) AS a_efficiency, AVG(accuracy) AS a_accuracy, AVG(workhour) AS a_workhour, MAX(time) AS `time`
			FROM dms_stat_online WHERE stat_id=cur_stat_id;

			
	END LOOP;
	CLOSE stat_id_cursor; -- 关闭stat_id游标

END
//
delimiter ;

-- ----------------------------
-- Procedure structure for fake_dms_stat_online
-- ----------------------------
DROP PROCEDURE IF EXISTS `fake_dms_stat_online`;
delimiter //
CREATE DEFINER=`root`@`localhost` PROCEDURE `fake_dms_stat_online`(IN begin_datetime VARCHAR(255), IN minutes INT)
BEGIN
	DECLARE i INT;  -- 循环次数flag
	DECLARE `time` VARCHAR(255);
	DECLARE stat_id_online INT;  -- stat_id
	DECLARE efficiency DECIMAL(6, 1);
	DECLARE accuracy DECIMAL(6, 1);
	DECLARE workhour DECIMAL(6, 1);
	
	DECLARE s_efficiency DECIMAL(6, 1);
	DECLARE s_accuracy DECIMAL(6, 1);
	DECLARE s_workhour DECIMAL(6, 1);
	
	DECLARE done INT DEFAULT false; -- 结束标志
	DECLARE cur_stat_standard CURSOR FOR SELECT m.stat_id AS stat_id, t.s_efficiency AS efficiency, t.s_accuracy AS accuracy, t.s_workhour AS workhour 
	FROM standard_team AS t JOIN sms_team_stat_member AS m ON t.team_id=m.team_id; -- 定义游标
	
	DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = true;  
	
	SET i = 0;

	WHILE i<=minutes DO  -- 一天1440分钟
		SET `time` = DATE_ADD(begin_datetime, INTERVAL i MINUTE);
		SET i = i+1;
		SET done = false;  -- 重置结束标志
		OPEN cur_stat_standard; -- 打开stat_id游标
		read_loop:LOOP 
			FETCH cur_stat_standard INTO stat_id_online, s_efficiency, s_accuracy, s_workhour;
			-- 判断游标的循环是否结束  
			IF done THEN  
				LEAVE read_loop;
			END IF; 
			IF (SELECT RAND() < 0.001) THEN  -- 百分之0.1的概率为0
				SET efficiency = 0;
			ELSE
				SET efficiency = FLOOR(60 + (RAND() * (s_efficiency-60+1))); -- 60-s_efficiency
			END IF;
			IF (SELECT RAND() < 0.001) THEN -- 百分之0.1的概率为0
				SET accuracy = 0;
			ELSE
				SET accuracy = FLOOR(70 + (RAND() * (s_accuracy-70+1))); -- 70-s_accuracy
			END IF;
			IF (SELECT RAND() < 0.001) THEN -- 百分之0.1的概率为0
				SET workhour = 0;
			ELSE
				SET workhour = FLOOR(15 + (RAND() * (s_workhour-15+1))); -- 15-s_workhour
			END IF;
			
-- 			SELECT stat_id_online, efficiency, accuracy, workhour,`time`;
			INSERT INTO dms_stat_online(stat_id, efficiency, accuracy, workhour, time)
			VALUE(stat_id_online, efficiency, accuracy, workhour,`time`);
			
		END LOOP;
		CLOSE cur_stat_standard; -- 关闭stat_id游标
	END WHILE;

END
//
delimiter ;

-- ----------------------------
-- Procedure structure for fake_dms_team_avg
-- ----------------------------
DROP PROCEDURE IF EXISTS `fake_dms_team_avg`;
delimiter //
CREATE DEFINER=`root`@`localhost` PROCEDURE `fake_dms_team_avg`()
BEGIN
	DECLARE `cur_team_id` VARCHAR(255);

	DECLARE done INT DEFAULT false; -- 结束标志
	DECLARE team_id_cursor CURSOR FOR SELECT DISTINCT team_id FROM dms_team_online; -- 定义游标
	
	DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = true;  
	OPEN team_id_cursor;
	read_loop:LOOP 
			FETCH team_id_cursor INTO `cur_team_id`;
			-- 判断游标的循环是否结束  
			IF done THEN  
				LEAVE read_loop;
			END IF; 
			
			INSERT INTO dms_team_avg(team_id, a_efficiency, a_accuracy, a_workhour, time)
			SELECT cur_team_id AS team_id, AVG(efficiency) AS a_efficiency, AVG(accuracy) AS a_accuracy, AVG(workhour) AS a_workhour, MAX(time) AS `time`
			FROM dms_team_online WHERE team_id=cur_team_id;

			
	END LOOP;
	CLOSE team_id_cursor; -- 关闭stat_id游标

END
//
delimiter ;

-- ----------------------------
-- Procedure structure for fake_dms_team_online
-- ----------------------------
DROP PROCEDURE IF EXISTS `fake_dms_team_online`;
delimiter //
CREATE DEFINER=`root`@`localhost` PROCEDURE `fake_dms_team_online`()
BEGIN
	DECLARE `cur_time` VARCHAR(255);

	DECLARE done INT DEFAULT false; -- 结束标志
	DECLARE cur_time_cursor CURSOR FOR SELECT DISTINCT(time) FROM dms_stat_online; -- 定义游标
	
	DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = true;  
	OPEN cur_time_cursor;
	read_loop:LOOP 
			FETCH cur_time_cursor INTO `cur_time`;
			-- 判断游标的循环是否结束  
			IF done THEN  
				LEAVE read_loop;
			END IF; 
			
			INSERT INTO dms_team_online(team_id, efficiency, accuracy, workhour, time)
			SELECT m.team_id AS team_id, AVG(o.efficiency) AS efficiency, AVG(o.accuracy) AS accuracy, AVG(o.workhour) AS workhour, `cur_time` AS `time`
			FROM dms_stat_online AS o 
			JOIN sms_team_stat_member AS m ON o.stat_id=m.stat_id
			WHERE o.time=`cur_time`
			GROUP BY m.team_id ;
			
	END LOOP;
	CLOSE cur_time_cursor; -- 关闭stat_id游标

END
//
delimiter ;

-- ----------------------------
-- Procedure structure for fake_dms_workshop_avg
-- ----------------------------
DROP PROCEDURE IF EXISTS `fake_dms_workshop_avg`;
delimiter //
CREATE DEFINER=`root`@`localhost` PROCEDURE `fake_dms_workshop_avg`()
BEGIN
	DECLARE `cur_workshop_id` VARCHAR(255);

	DECLARE done INT DEFAULT false; -- 结束标志
	DECLARE workshop_id_cursor CURSOR FOR SELECT DISTINCT workshop_id FROM dms_workshop_online; -- 定义游标
	
	DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = true;  
	OPEN workshop_id_cursor;
	read_loop:LOOP 
			FETCH workshop_id_cursor INTO `cur_workshop_id`;
			-- 判断游标的循环是否结束  
			IF done THEN  
				LEAVE read_loop;
			END IF; 
			
			INSERT INTO dms_workshop_avg(workshop_id, a_efficiency, a_accuracy, a_workhour, time)
			SELECT cur_workshop_id AS workshop_id, AVG(efficiency) AS efficiency, AVG(accuracy) AS accuracy, AVG(workhour) AS workhour, MAX(time) AS `time`
			FROM dms_workshop_online WHERE workshop_id=cur_workshop_id; 
	
	END LOOP;
	CLOSE workshop_id_cursor; -- 关闭stat_id游标

END
//
delimiter ;

-- ----------------------------
-- Procedure structure for fake_dms_workshop_online
-- ----------------------------
DROP PROCEDURE IF EXISTS `fake_dms_workshop_online`;
delimiter //
CREATE DEFINER=`root`@`localhost` PROCEDURE `fake_dms_workshop_online`()
BEGIN
	DECLARE `cur_time` VARCHAR(255);

	DECLARE done INT DEFAULT false; -- 结束标志
	DECLARE cur_time_cursor CURSOR FOR SELECT DISTINCT(time) FROM dms_group_online; -- 定义游标
	
	DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = true;  
	OPEN cur_time_cursor;
	read_loop:LOOP 
			FETCH cur_time_cursor INTO `cur_time`;
			-- 判断游标的循环是否结束  
			IF done THEN  
				LEAVE read_loop;
			END IF; 
			
			INSERT INTO dms_workshop_online(workshop_id, efficiency, accuracy, workhour, time)
			SELECT w.workshop_id AS workshop_id, AVG(o.efficiency) AS efficiency, AVG(o.accuracy) AS accuracy, AVG(o.workhour) AS workhour, `cur_time` AS `time`
			FROM dms_group_online AS o 
			JOIN (SELECT DISTINCT group_id, workshop_id FROM sms_team_group_workshop) AS w ON o.group_id=w.group_id
			WHERE o.time=`cur_time`
			GROUP BY w.workshop_id;

			
	END LOOP;
	CLOSE cur_time_cursor; -- 关闭stat_id游标

END
//
delimiter ;

SET FOREIGN_KEY_CHECKS = 1;
