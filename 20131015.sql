-- MySQL dump 10.13  Distrib 5.1.61, for redhat-linux-gnu (x86_64)
--
-- Host: 10.67.15.70    Database: app_new31
-- ------------------------------------------------------
-- Server version	5.5.23-log
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+08:00";
SET NAMES utf8;

-- Dump completed on 2013-10-15  9:42:33

--
-- 限制导出的表
--

--
-- 限制表 `account_bsinfo`
--
ALTER TABLE `account_bsinfo`
  ADD CONSTRAINT `user_id_refs_id_9e42fd19` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- 限制表 `account_pts`
--
ALTER TABLE `account_pts`
  ADD CONSTRAINT `user_id_refs_id_07caa1a5` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- 限制表 `area_attribution`
--
ALTER TABLE `area_attribution`
  ADD CONSTRAINT `area_id_refs_id_baf7a40e` FOREIGN KEY (`area_id`) REFERENCES `area_area` (`id`),
  ADD CONSTRAINT `user_id_refs_id_7c1989f5` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- 限制表 `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `group_id_refs_id_f4b32aac` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `permission_id_refs_id_6ba0f519` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`);

--
-- 限制表 `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `content_type_id_refs_id_d043b34a` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- 限制表 `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `user_id_refs_id_40c41112` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  ADD CONSTRAINT `group_id_refs_id_274b862c` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- 限制表 `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `user_id_refs_id_4dc23c39` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  ADD CONSTRAINT `permission_id_refs_id_35d9ac25` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`);

--
-- 限制表 `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `user_id_refs_id_c0d12874` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  ADD CONSTRAINT `content_type_id_refs_id_93d2d1f8` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- 限制表 `finance_fnc`
--
ALTER TABLE `finance_fnc`
  ADD CONSTRAINT `ord_id_refs_sn_8c96daf4` FOREIGN KEY (`ord_id`) REFERENCES `order_ord` (`sn`),
  ADD CONSTRAINT `cod_id_refs_id_64bed894` FOREIGN KEY (`cod_id`) REFERENCES `payment_pay` (`id`);

--
-- 限制表 `inventory_invnum`
--
ALTER TABLE `inventory_invnum`
  ADD CONSTRAINT `pro_id_refs_id_1278057c` FOREIGN KEY (`pro_id`) REFERENCES `inventory_invpro` (`id`);

--
-- 限制表 `inventory_invpro`
--
ALTER TABLE `inventory_invpro`
  ADD CONSTRAINT `spec_id_refs_id_aa83ce51` FOREIGN KEY (`spec_id`) REFERENCES `item_itemspec` (`id`);

--
-- 限制表 `item_itemdesc`
--
ALTER TABLE `item_itemdesc`
  ADD CONSTRAINT `item_id_refs_id_5e2efa5c` FOREIGN KEY (`item_id`) REFERENCES `item_item` (`id`);

--
-- 限制表 `item_itemfee`
--
ALTER TABLE `item_itemfee`
  ADD CONSTRAINT `spec_id_refs_id_c0958068` FOREIGN KEY (`spec_id`) REFERENCES `item_itemspec` (`id`),
  ADD CONSTRAINT `dis_id_refs_id_06c4beb6` FOREIGN KEY (`dis_id`) REFERENCES `discount_dis` (`id`);

--
-- 限制表 `item_itemimg`
--
ALTER TABLE `item_itemimg`
  ADD CONSTRAINT `item_id_refs_id_858e31a5` FOREIGN KEY (`item_id`) REFERENCES `item_item` (`id`);

--
-- 限制表 `item_itemspec`
--
ALTER TABLE `item_itemspec`
  ADD CONSTRAINT `item_id_refs_id_7e3815fd` FOREIGN KEY (`item_id`) REFERENCES `item_item` (`id`),
  ADD CONSTRAINT `spec_id_refs_id_a9fcb3a1` FOREIGN KEY (`spec_id`) REFERENCES `spec_spec` (`id`);

--
-- 限制表 `item_item_tag`
--
ALTER TABLE `item_item_tag`
  ADD CONSTRAINT `item_id_refs_id_c9ebad3b` FOREIGN KEY (`item_id`) REFERENCES `item_item` (`id`),
  ADD CONSTRAINT `tag_id_refs_id_04f8d9c7` FOREIGN KEY (`tag_id`) REFERENCES `tag_tag` (`id`);

--
-- 限制表 `logistics_logcs`
--
ALTER TABLE `logistics_logcs`
  ADD CONSTRAINT `ord_id_refs_sn_9fa6d285` FOREIGN KEY (`ord_id`) REFERENCES `order_ord` (`sn`),
  ADD CONSTRAINT `cod_id_refs_id_fdb1934d` FOREIGN KEY (`cod_id`) REFERENCES `deliver_deliver` (`id`),
  ADD CONSTRAINT `dman_id_refs_id_c3d7347f` FOREIGN KEY (`dman_id`) REFERENCES `auth_user` (`id`);

--
-- 限制表 `log_accountlog`
--
ALTER TABLE `log_accountlog`
  ADD CONSTRAINT `act_id_refs_id_eec489f3` FOREIGN KEY (`act_id`) REFERENCES `auth_user` (`id`),
  ADD CONSTRAINT `user_id_refs_id_eec489f3` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- 限制表 `log_ordlog`
--
ALTER TABLE `log_ordlog`
  ADD CONSTRAINT `ord_id_refs_sn_83847d94` FOREIGN KEY (`ord_id`) REFERENCES `order_ord` (`sn`),
  ADD CONSTRAINT `user_id_refs_id_649095e4` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- 限制表 `message_msg`
--
ALTER TABLE `message_msg`
  ADD CONSTRAINT `user_id_refs_id_9c355cb1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- 限制表 `order_ord`
--
ALTER TABLE `order_ord`
  ADD CONSTRAINT `user_id_refs_id_e7dee65a` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- 限制表 `produce_pro`
--
ALTER TABLE `produce_pro`
  ADD CONSTRAINT `ord_id_refs_sn_ba26c730` FOREIGN KEY (`ord_id`) REFERENCES `order_ord` (`sn`);

--
-- 限制表 `purview_elesub`
--
ALTER TABLE `purview_elesub`
  ADD CONSTRAINT `sub_id_refs_id_2acd0649` FOREIGN KEY (`sub_id`) REFERENCES `purview_element` (`id`),
  ADD CONSTRAINT `path_id_refs_id_2acd0649` FOREIGN KEY (`path_id`) REFERENCES `purview_element` (`id`);

--
-- 限制表 `purview_privilege_element`
--
ALTER TABLE `purview_privilege_element`
  ADD CONSTRAINT `privilege_id_refs_id_4ec70abb` FOREIGN KEY (`privilege_id`) REFERENCES `purview_privilege` (`id`),
  ADD CONSTRAINT `element_id_refs_id_7fc8c0d8` FOREIGN KEY (`element_id`) REFERENCES `purview_element` (`id`);

--
-- 限制表 `purview_role_privilege`
--
ALTER TABLE `purview_role_privilege`
  ADD CONSTRAINT `role_id_refs_id_a2b216d1` FOREIGN KEY (`role_id`) REFERENCES `purview_role` (`id`),
  ADD CONSTRAINT `privilege_id_refs_id_724e59bb` FOREIGN KEY (`privilege_id`) REFERENCES `purview_privilege` (`id`);

--
-- 限制表 `purview_role_user`
--
ALTER TABLE `purview_role_user`
  ADD CONSTRAINT `role_id_refs_id_9cc1cd87` FOREIGN KEY (`role_id`) REFERENCES `purview_role` (`id`),
  ADD CONSTRAINT `user_id_refs_id_a611a90b` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
