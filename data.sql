INSERT INTO `item_item` (`name`, `sn`, `onl`, `show`) VALUES
( '香浓巧克力', '3133001', 1, 1),
( '德国烤奶酪', '3133002', 1, 1),
( '蓝莓芝士', '3133010', 1, 1),
( '香橙可可', '3133003', 1, 1),
( '提拉米苏', '3133004', 1, 1),
( '茶之蜜', '3133008', 1, 1),
( '抹茶慕斯', '3133011', 1, 1),
( '焰火', '3133006', 1, 1),
( '樱桃巧克力', '3133013', 1, 1),
( '谁动了我的奶酪', '3133009', 1, 1),
( 'Rubus idaeus white chocolate M', '3133015', 1, 1),
( '芒果冻奶酪', '3133007', 1, 1),
( '杏仁咖啡', '3133014', 1, 1),
( '歌剧魅影', '3133012', 1, 1),
( '波尔多', '3133005', 1, 1),
( '蓝莓果肉曲奇', '3155004', 1, 1),
( '丹麦原味曲奇', '3155001', 1, 1),
( '红酒巧克力曲奇', '3155002', 1, 1),
( '百利燕麦曲奇', '3155005', 1, 1),
( '经典巧克力曲奇', '3155003', 1, 1),
( '朗姆黑加仑曲奇', '3155006', 1, 1),
( '风尚浓露', '3177011', 1, 1),
( '柠檬万象巧克力', '3177005', 1, 1),
( '原味松露巧克力', '3177001', 1, 1),
( 'Cognac chocolate浓纯干邑酒巧克力', '3177007', 1, 1),
( '什锦曲奇', '3155007', 1, 1),
( '72%黑纯巧克力', '3177003', 1, 1),
( '餐具套装(随蛋糕配送)', '3199005', 1, 1),
( 'dream of red wine chocolate梦幻红', '3177006', 1, 1),
( '晨露树莓巧克力', '3177004', 1, 1),
( 'Black chocolate rocher优澈黑巧克力', '3177002', 1, 1),
( '风尚果香', '3177009', 1, 1),
( '风尚酒香', '3177010', 1, 1),
( '幸运草白巧克力', '3177008', 1, 1),
( '覆盆子白巧克力(活动款)', '3166006', 1, 1),
( '杏仁咖啡(活动款)', '3166007', 1, 1),
( '芒果冻奶酪(活动款)', '3166010', 1, 1),
( '茶之蜜(活动款)', '3166011', 1, 1),
( '香蕉榛子慕斯', '3133016', 1, 1),
( '果园轻乳酪', '3133017', 1, 1),
( '巧克力淡奶慕斯', '3133018', 1, 1),
( '榴莲小姐', '3133019', 1, 1),
( '松露薄荷慕斯', '3133020', 1, 1),
( '奶酪菠萝派', '3133021', 1, 1),
( '生日套装兑换(生日牌/冷烟花/蜡烛)', '3199006', 1, 1),
( '奶酪芒果派', '3133022', 1, 1),
( '杏仁优澈巧克力', '3177012', 1, 1);

INSERT INTO `spec_spec` (`value`) VALUES
('1.0磅：约16×16(cm)'),
('1.5磅：约20×20(cm)'),
('2.5磅：约23×23(cm)'),
('3.5磅：约26×26(cm)'),
('5.5磅：约30×30(cm)'),
('10.0磅：约39×39(cm)');

INSERT INTO `item_itemimg` (`id`, `item_id`, `img`, `typ`, `onl`) VALUES
(3, 1, 'images/3133001b1a.jpg', 0, 1),
(4, 1, 'images/3133001b1b.jpg', 0, 1),
(5, 1, 'images/3133001b1c.jpg', 0, 1),
(6, 1, 'images/3133001b1d.jpg', 0, 1),
(7, 2, 'images/3133002b1a.jpg', 0, 1),
(8, 1, 'images/3133002b1b.jpg', 0, 1),
(9, 2, 'images/3133002b1c.jpg', 0, 1),
(10, 1, 'images/3133001b2a.jpg', 1, 1),
(11, 1, 'images/3133001b2b.jpg', 1, 1),
(12, 2, 'images/3133002b2a.jpg', 1, 1),
(13, 2, 'images/3133002b2b.jpg', 1, 1),
(14, 2, 'images/3133002b2c.jpg', 1, 1);



INSERT INTO `tag_tag` (`tag`,`onl`) VALUES
('cake', 1),
('蛋糕', 1),
('乳酪', 1),
('原味', 1),
('奶酪', 1),
('巧克力', 1),
('慕斯', 1),
('曲奇', 1),
('松露', 1),
('派', 1),
('芒果', 1),
('芝士', 1);

INSERT INTO `payment_pay` (`cod`, `config`, `onl`) VALUES
('payafter', 'payafter', 1),
('alipay', 'alipay', 1),
('post', 'post', 1);

INSERT INTO `area_area` (`id`, `name`, `onl`, `sub_id`) VALUES
(1, '南宁', 1, NULL),
(2, '青秀区', 1, 1),
(3, '西乡塘区', 1, 1),
(4, '兴宁区', 1, 1);

INSERT INTO `signtime_signtime` (`start`, `end`, `onl`) VALUES
('06:00:00', '07:00:00', 1),
('07:00:00', '08:00:00', 1);

INSERT INTO `discount_dis` (`dis`, `onl`) VALUES
(1, 1),
(0.95, 1),
(0.9, 1);

INSERT INTO `purview_element` (`id`, `path`, `typ`, `onl`, `sub_id`) VALUES
(1, '/office/', 1, 1, NULL),
(2, '/order/', 1, 1, NULL),
(3, '/order/new/', 1, 1, 2),
(4, '/order/submit/', 2, 1, NULL),
(5, '/order/additemtoorder/', 2, 1, NULL),
(6, '/order/delitem/', 3, 1, NULL),
(7, '/order/edit/', 4, 1, NULL),
(8, '/order/0/', 4, 1, NULL),
(9, '/order/1/', 4, 1, NULL),
(10, '/order/2/', 4, 1, NULL),
(11, '/order/3/', 4, 1, NULL),
(12, '/logistics/', 1, 1, NULL),
(13, '/logistics/edit/', 4, 1, NULL),
(14, '/logistics/submit/', 4, 1, NULL),
(15, '/logistics/0/', 4, 1, NULL),
(16, '/logistics/1/', 4, 1, NULL),
(17, '/logistics/2/', 4, 1, NULL),
(18, '/logistics/3/', 4, 1, NULL),
(19, '/logistics/4/', 4, 1, NULL),
(20, '/logistics/5/', 4, 1, NULL),
(21, '/produce/', 1, 1, NULL),
(22, '/produce/0/', 4, 1, NULL),
(23, '/produce/1/', 4, 1, NULL),
(24, '/produce/2/', 4, 1, NULL),
(25, '/produce/3/', 4, 1, NULL),
(26, '/produce/4/', 4, 1, NULL),
(27, '/inventory/', 1, 1, NULL);


INSERT INTO `purview_privilege` (`id`, `name`, `onl`) VALUES
(1, 0, 1);

INSERT INTO `purview_role` (`id`, `role`, `onl`) VALUES
(1, -1, 1);
