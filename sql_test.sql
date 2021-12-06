--users table creation
CREATE TABLE messaging.`users` (
  `id` int DEFAULT NULL,
  `createdAt` datetime DEFAULT NULL,
  `updatedAt` datetime DEFAULT NULL,
  `firstName` text,
  `lastName` text,
  `address` text,
  `city` text,
  `country` text,
  `zipCode` text,
  `email` text,
  `birthDate` datetime DEFAULT NULL,
  `profile.gender` text,
  `profile.isSmoking` tinyint(1) DEFAULT NULL,
  `profile.profession` text,
  `profile.income` text
);

--messages table creation
CREATE TABLE messaging.`messages` (
  `id` int DEFAULT NULL,
  `createdAt` datetime DEFAULT NULL,
  `receiverId` int DEFAULT NULL,
  `senderId` int DEFAULT NULL,
  `message` text
);

--subscriptions table creation
CREATE TABLE messaging.`subscriptions` (
  `id` int DEFAULT NULL,
  `createdAt` datetime DEFAULT NULL,
  `startDate` datetime DEFAULT NULL,
  `endDate` datetime DEFAULT NULL,
  `status` text,
  `amount` double DEFAULT NULL
);

--Total messages being sent every day
select createdAt, count(message) as message_count from messaging.messages group by date_format(createdAt,'%Y-%m-%d') order by createdAt desc;;
	
--Users that did not receive any message
select u.* from messaging.users u left join messaging.messages m on u.id=m.receiverId where m.receiverId is null;

--Active subscriptions today
select date_format(createdAt,'%Y-%m-%d') as createdAt, count(status) as active_status_count
from messaging.subscriptions where date_format(createdAt,'%Y-%m-%d')= date_format(now(),'%Y-%m-%d') and status='Active';

--Users sending messages without an active subscription
select users.* from messaging.users users join
(select distinct id from messaging.subscriptions where id not in
(select distinct id from messaging.subscriptions where status = 'Active')) subs on users.id = subs.id


