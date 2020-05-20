-- phpMyAdmin SQL Dump
-- version 4.6.6deb5
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: May 11, 2020 at 12:38 PM
-- Server version: 10.0.28-MariaDB-2+b1
-- PHP Version: 7.3.14-1~deb10u1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `curd`
--

-- --------------------------------------------------------

--
-- Stand-in structure for view `daily_raport`
-- (See below for the actual view)
--
CREATE TABLE `daily_raport` (
`daily number of tickets` bigint(21)
,`summary price` double
,`DATA` date
);

-- --------------------------------------------------------

--
-- Table structure for table `movie`
--

CREATE TABLE `movie` (
  `movie_id` int(11) NOT NULL,
  `movie_name` text COLLATE utf8_polish_ci NOT NULL,
  `ticket_price` float NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_polish_ci;

--
-- Dumping data for table `movie`
--

INSERT INTO `movie` (`movie_id`, `movie_name`, `ticket_price`) VALUES
(1, 'NEW TEST', 15),
(2, 'TEST MOVIE', 10),
(3, 'Scary', 12);

-- --------------------------------------------------------

--
-- Stand-in structure for view `overall_raport`
-- (See below for the actual view)
--
CREATE TABLE `overall_raport` (
`number of tickets` bigint(21)
,`summary price` double
);

-- --------------------------------------------------------

--
-- Table structure for table `ticket`
--

CREATE TABLE `ticket` (
  `ticket_number` int(11) NOT NULL,
  `name` text COLLATE utf8_polish_ci NOT NULL,
  `surname` text COLLATE utf8_polish_ci NOT NULL,
  `movie_id` int(11) NOT NULL,
  `discount` float DEFAULT '0',
  `day_of_valid` date NOT NULL,
  `ticket_status` int(1) NOT NULL DEFAULT '1',
  `date_of_sold` date NOT NULL,
  `barcode` text COLLATE utf8_polish_ci
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_polish_ci;

--
-- Dumping data for table `ticket`
--

INSERT INTO `ticket` (`ticket_number`, `name`, `surname`, `movie_id`, `discount`, `day_of_valid`, `ticket_status`, `date_of_sold`, `barcode`) VALUES
(12, 'Bogdan', 'Dzik', 3, 10, '2020-05-01', 1, '2020-03-26', '1570235849880224356090451048290505009664963126'),
(14, 'Jan', 'Kowalski', 2, 30, '2020-05-10', 0, '2020-05-08', '26571351471594181068762172696980376987185208'),
(15, 'Ewelina', 'Kopytko', 2, 30, '2020-05-09', 1, '2020-05-08', '225669305827245944539670843460529226068024');

-- --------------------------------------------------------

--
-- Stand-in structure for view `ticket_view`
-- (See below for the actual view)
--
CREATE TABLE `ticket_view` (
`barcode` mediumtext
,`first and last name` mediumtext
,`movie_name` text
,`ticket price` double
,`day_of_valid` date
,`ticket_status` int(1)
,`discount` float
);

-- --------------------------------------------------------

--
-- Structure for view `daily_raport`
--
DROP TABLE IF EXISTS `daily_raport`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `daily_raport`  AS  select count(`ticket`.`ticket_number`) AS `daily number of tickets`,sum((`movie`.`ticket_price` * (1 - (`ticket`.`discount` / 100)))) AS `summary price`,curdate() AS `DATA` from (`ticket` join `movie` on((`movie`.`movie_id` = `ticket`.`movie_id`))) where (`ticket`.`date_of_sold` = curdate()) ;

-- --------------------------------------------------------

--
-- Structure for view `overall_raport`
--
DROP TABLE IF EXISTS `overall_raport`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `overall_raport`  AS  select count(`ticket`.`ticket_number`) AS `number of tickets`,sum((`movie`.`ticket_price` * (1 - (`ticket`.`discount` / 100)))) AS `summary price` from (`ticket` join `movie` on((`movie`.`movie_id` = `ticket`.`movie_id`))) ;

-- --------------------------------------------------------

--
-- Structure for view `ticket_view`
--
DROP TABLE IF EXISTS `ticket_view`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `ticket_view`  AS  select concat(`ticket`.`ticket_number`,`ticket`.`barcode`) AS `barcode`,concat(`ticket`.`name`,' ',`ticket`.`surname`) AS `first and last name`,`movie`.`movie_name` AS `movie_name`,(`movie`.`ticket_price` * (1 - (`ticket`.`discount` / 100))) AS `ticket price`,`ticket`.`day_of_valid` AS `day_of_valid`,`ticket`.`ticket_status` AS `ticket_status`,`ticket`.`discount` AS `discount` from (`ticket` join `movie` on((`movie`.`movie_id` = `ticket`.`movie_id`))) ;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `movie`
--
ALTER TABLE `movie`
  ADD PRIMARY KEY (`movie_id`);

--
-- Indexes for table `ticket`
--
ALTER TABLE `ticket`
  ADD PRIMARY KEY (`ticket_number`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `movie`
--
ALTER TABLE `movie`
  MODIFY `movie_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
--
-- AUTO_INCREMENT for table `ticket`
--
ALTER TABLE `ticket`
  MODIFY `ticket_number` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
