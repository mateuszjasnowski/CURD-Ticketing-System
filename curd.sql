-- phpMyAdmin SQL Dump
-- version 4.9.5deb2
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: May 22, 2020 at 05:16 PM
-- Server version: 8.0.20-0ubuntu0.20.04.1
-- PHP Version: 7.4.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `curd`
--
CREATE DATABASE IF NOT EXISTS `curd` DEFAULT CHARACTER SET utf8 COLLATE utf8_polish_ci;
USE `curd`;

-- --------------------------------------------------------

--
-- Stand-in structure for view `daily_raport`
-- (See below for the actual view)
--
DROP VIEW IF EXISTS `daily_raport`;
CREATE TABLE IF NOT EXISTS `daily_raport` (
`daily number of tickets` bigint
,`summary price` double(22,2)
,`DATA` date
);

-- --------------------------------------------------------

--
-- Table structure for table `movie`
--

DROP TABLE IF EXISTS `movie`;
CREATE TABLE IF NOT EXISTS `movie` (
  `movie_id` int NOT NULL AUTO_INCREMENT,
  `movie_name` text CHARACTER SET utf8 COLLATE utf8_polish_ci NOT NULL,
  `ticket_price` float NOT NULL DEFAULT '0',
  PRIMARY KEY (`movie_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8 COLLATE=utf8_polish_ci;

--
-- Dumping data for table `movie`
--

INSERT INTO `movie` (`movie_id`, `movie_name`, `ticket_price`) VALUES
(1, 'Romeo i Julia', 35),
(2, 'Przygody Bolka i Lolka', 20),
(3, 'Kolacja u Moncka', 45),
(4, 'Wystawa WOŚP', 2),
(5, 'Stand-up Cera do Pudru ciepłego', 29),
(6, 'Qlimax', 87),
(7, 'Koncert Sing', 55),
(8, 'Koncert Korteza', 43),
(9, 'Trixi one', 25);

-- --------------------------------------------------------

--
-- Stand-in structure for view `overall_raport`
-- (See below for the actual view)
--
DROP VIEW IF EXISTS `overall_raport`;
CREATE TABLE IF NOT EXISTS `overall_raport` (
`number of tickets` bigint
,`summary price` double(22,2)
);

-- --------------------------------------------------------

--
-- Table structure for table `ticket`
--

DROP TABLE IF EXISTS `ticket`;
CREATE TABLE IF NOT EXISTS `ticket` (
  `ticket_number` int NOT NULL AUTO_INCREMENT,
  `name` text CHARACTER SET utf8 COLLATE utf8_polish_ci NOT NULL,
  `surname` text CHARACTER SET utf8 COLLATE utf8_polish_ci NOT NULL,
  `movie_id` int NOT NULL,
  `discount` float DEFAULT '0',
  `day_of_valid` date NOT NULL,
  `ticket_status` int NOT NULL DEFAULT '1',
  `date_of_sold` date NOT NULL,
  `barcode` text CHARACTER SET utf8 COLLATE utf8_polish_ci,
  PRIMARY KEY (`ticket_number`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8 COLLATE=utf8_polish_ci;

--
-- Dumping data for table `ticket`
--

INSERT INTO `ticket` (`ticket_number`, `name`, `surname`, `movie_id`, `discount`, `day_of_valid`, `ticket_status`, `date_of_sold`, `barcode`) VALUES
(12, 'Bogdan', 'Dzik', 3, 10, '2020-05-01', 1, '2020-03-26', '1570235849880224356090451048290505009664963126'),
(14, 'Jan', 'Kowalski', 1, 25, '2020-05-10', 0, '2020-05-08', '26571351471594181068762172696980376987185208'),
(15, 'Ewelina', 'Kopytko', 2, 30, '2020-05-09', 1, '2020-05-08', '225669305827245944539670843460529226068024'),
(20, 'Filip', 'Skonopi', 1, 0, '2020-05-13', 1, '2020-05-13', '128386242434832347767813089247427012931891'),
(21, 'Janina', 'Dziób', 2, 50, '2020-05-14', 1, '2020-05-14', '291023109088132130530807246020712149300'),
(22, 'Anna', 'Pol', 1, 30, '2020-05-15', 1, '2020-05-14', '16372736638227218989269006496052'),
(23, 'Jessica', 'Fat', 5, 0, '2020-05-23', 1, '2020-05-22', '55576131894353633699404817707570'),
(24, 'Christopher', 'Majster', 7, 30, '2020-05-23', 1, '2020-05-22', '726331230093669370530219676423362530062898'),
(25, 'Michalina', 'Szpilka', 8, 30, '2020-10-12', 1, '2020-05-22', '828406185945414690438477466108933637485106'),
(26, 'Robert', 'Srodek', 6, 0, '2020-10-20', 1, '2020-05-22', '6110920104793690822624558196553155424818'),
(27, 'Paweł', 'Klos', 9, 30, '2020-08-10', 1, '2020-05-22', '91529771853924982639540336306500146'),
(28, 'Filomena', 'Gwóźdź', 5, 0, '2020-12-28', 1, '2020-05-22', '51593785865141577534227836673819468130140631602'),
(29, 'Filip ', 'Kret', 8, 25, '2020-05-30', 1, '2020-05-22', '81530244129258895831729839497097778'),
(30, 'Zuzanna ', 'Wiercik', 8, 30, '2020-05-30', 1, '2020-05-22', '829744661603732682928862894216513986572850'),
(31, 'Karolina', 'Zaraza', 3, 0, '2020-06-01', 1, '2020-05-22', '3120136492333621561025470186750116442674');

-- --------------------------------------------------------

--
-- Stand-in structure for view `ticket_view`
-- (See below for the actual view)
--
DROP VIEW IF EXISTS `ticket_view`;
CREATE TABLE IF NOT EXISTS `ticket_view` (
`barcode` mediumtext
,`first and last name` mediumtext
,`movie_name` text
,`ticket price` double(22,2)
,`day_of_valid` date
,`ticket_status` int
,`discount` float
);

-- --------------------------------------------------------

--
-- Structure for view `daily_raport`
--
DROP TABLE IF EXISTS `daily_raport`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `daily_raport`  AS  select count(`ticket`.`ticket_number`) AS `daily number of tickets`,round(sum((`movie`.`ticket_price` * (1 - (`ticket`.`discount` / 100)))),2) AS `summary price`,curdate() AS `DATA` from (`ticket` join `movie` on((`movie`.`movie_id` = `ticket`.`movie_id`))) where (`ticket`.`date_of_sold` = curdate()) ;

-- --------------------------------------------------------

--
-- Structure for view `overall_raport`
--
DROP TABLE IF EXISTS `overall_raport`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `overall_raport`  AS  select count(`ticket`.`ticket_number`) AS `number of tickets`,round(sum((`movie`.`ticket_price` * (1 - (`ticket`.`discount` / 100)))),2) AS `summary price` from (`ticket` join `movie` on((`movie`.`movie_id` = `ticket`.`movie_id`))) ;

-- --------------------------------------------------------

--
-- Structure for view `ticket_view`
--
DROP TABLE IF EXISTS `ticket_view`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `ticket_view`  AS  select concat(`ticket`.`ticket_number`,`ticket`.`barcode`) AS `barcode`,concat(`ticket`.`name`,' ',`ticket`.`surname`) AS `first and last name`,`movie`.`movie_name` AS `movie_name`,round((`movie`.`ticket_price` * (1 - (`ticket`.`discount` / 100))),2) AS `ticket price`,`ticket`.`day_of_valid` AS `day_of_valid`,`ticket`.`ticket_status` AS `ticket_status`,`ticket`.`discount` AS `discount` from (`ticket` join `movie` on((`movie`.`movie_id` = `ticket`.`movie_id`))) ;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
