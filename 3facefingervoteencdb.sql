-- phpMyAdmin SQL Dump
-- version 2.11.6
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Apr 15, 2025 at 08:57 AM
-- Server version: 5.0.51
-- PHP Version: 5.2.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `3facefingervoteencdb`
--

-- --------------------------------------------------------

--
-- Table structure for table `cantb`
--

CREATE TABLE `cantb` (
  `id` bigint(250) NOT NULL auto_increment,
  `Name` varchar(250) NOT NULL,
  `PartName` varchar(250) NOT NULL,
  `PartCode` varchar(250) NOT NULL,
  `Image` varchar(500) NOT NULL,
  `Address` varchar(250) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=4 ;

--
-- Dumping data for table `cantb`
--

INSERT INTO `cantb` (`id`, `Name`, `PartName`, `PartCode`, `Image`, `Address`) VALUES
(1, 'Vijay', '1001', 'TVK', '1 (1).jpg', 'Tiruchirappalli'),
(2, 'Vijay', '10024', 'TVK', '1 (1).jpg', 'Chennai'),
(3, 'Stalin', '1254', 'DMK', '1.jpg', 'Cuddalore');

-- --------------------------------------------------------

--
-- Table structure for table `regtb`
--

CREATE TABLE `regtb` (
  `UserName` varchar(250) NOT NULL,
  `FatherName` varchar(250) NOT NULL,
  `Gender` varchar(250) NOT NULL,
  `Age` varchar(250) NOT NULL,
  `Email` varchar(250) NOT NULL,
  `Phone` varchar(250) NOT NULL,
  `Address` varchar(250) NOT NULL,
  `VoterId` varchar(250) NOT NULL,
  `AadharId` varchar(250) NOT NULL,
  `FImage` varchar(500) NOT NULL,
  `Pukey` varchar(250) NOT NULL,
  `PvKey` varchar(250) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `regtb`
--

INSERT INTO `regtb` (`UserName`, `FatherName`, `Gender`, `Age`, `Email`, `Phone`, `Address`, `VoterId`, `AadharId`, `FImage`, `Pukey`, `PvKey`) VALUES
('ibbu', 'ibbu', 'Male', '24', 'sangeeth5535@gmail.com', '9087259509', 'Tiruchirappalli', '12345678998', '123456789984', '7228.png', '02bd0b5b54091af2b3d12167226815a5396d23797229bb8390517591678b860e52', '241e8a5fdacb9a182aa0c9a3e93ac7a17ac0c50c7e997ecf411074782403c4de');

-- --------------------------------------------------------

--
-- Table structure for table `temptb`
--

CREATE TABLE `temptb` (
  `id` bigint(50) NOT NULL,
  `UserName` varchar(250) NOT NULL,
  `Status` varchar(250) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `temptb`
--

INSERT INTO `temptb` (`id`, `UserName`, `Status`) VALUES
(0, '12345678998', '3121');

-- --------------------------------------------------------

--
-- Table structure for table `votedtb`
--

CREATE TABLE `votedtb` (
  `id` bigint(50) NOT NULL auto_increment,
  `VoterId` varchar(250) NOT NULL,
  `PartCode` varchar(250) NOT NULL,
  `Image` varchar(250) NOT NULL,
  `count` int(20) NOT NULL,
  `Hash1` varchar(250) NOT NULL,
  `Hash2` varchar(250) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

--
-- Dumping data for table `votedtb`
--

