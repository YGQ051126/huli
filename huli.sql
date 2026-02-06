/*
 Navicat Premium Dump SQL

 Source Server         : Market
 Source Server Type    : MySQL
 Source Server Version : 80039 (8.0.39)
 Source Host           : localhost:3306
 Source Schema         : huli

 Target Server Type    : MySQL
 Target Server Version : 80039 (8.0.39)
 File Encoding         : 65001

 Date: 06/02/2026 14:55:34
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for activity_gallery_activity
-- ----------------------------
DROP TABLE IF EXISTS `activity_gallery_activity`;
CREATE TABLE `activity_gallery_activity`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `description` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `activity_date` date NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `staff_id` bigint NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `activity_gallery_activity_staff_id_c17bb125_fk`(`staff_id` ASC) USING BTREE,
  CONSTRAINT `activity_gallery_activity_staff_id_c17bb125_fk` FOREIGN KEY (`staff_id`) REFERENCES `users_staffuser` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 15 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of activity_gallery_activity
-- ----------------------------
INSERT INTO `activity_gallery_activity` VALUES (2, 'Test Activity', 'This is a test activity description', '2026-01-15', '2026-01-15 09:49:54.689606', '2026-01-15 09:49:54.689606', NULL);
INSERT INTO `activity_gallery_activity` VALUES (4, '分点', '第三方', '2026-01-07', '2026-01-19 13:24:36.144417', '2026-01-19 13:24:36.144417', NULL);
INSERT INTO `activity_gallery_activity` VALUES (5, '分点11', '额', '2026-01-15', '2026-01-19 13:44:50.740603', '2026-01-19 13:44:50.740603', NULL);
INSERT INTO `activity_gallery_activity` VALUES (6, '测完3.1', '使得', '2026-01-07', '2026-01-19 13:52:36.853095', '2026-01-19 13:52:36.853095', NULL);
INSERT INTO `activity_gallery_activity` VALUES (10, '地方', '速度', '2026-01-06', '2026-01-20 06:13:48.991691', '2026-01-20 06:13:48.991691', NULL);
INSERT INTO `activity_gallery_activity` VALUES (11, '德萨比', '大风', '2026-01-14', '2026-01-20 06:26:08.671480', '2026-01-20 06:26:08.671480', NULL);
INSERT INTO `activity_gallery_activity` VALUES (12, 'srg', 'dfa', '2026-01-07', '2026-01-20 06:40:57.901566', '2026-01-20 06:40:57.901566', NULL);
INSERT INTO `activity_gallery_activity` VALUES (13, '额我给', '阿三哥', '2026-01-06', '2026-01-20 07:00:55.681762', '2026-01-20 07:00:55.681762', NULL);
INSERT INTO `activity_gallery_activity` VALUES (14, '测试3.2', '0', '2026-01-26', '2026-01-26 10:19:08.804275', '2026-01-26 10:19:08.804275', NULL);

-- ----------------------------
-- Table structure for activity_gallery_activitymedia
-- ----------------------------
DROP TABLE IF EXISTS `activity_gallery_activitymedia`;
CREATE TABLE `activity_gallery_activitymedia`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `media_type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `file_url` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `file_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `file_size` int NOT NULL,
  `uploaded_at` datetime(6) NOT NULL,
  `activity_id` bigint NOT NULL,
  `uploaded_by_id` bigint NULL DEFAULT NULL,
  `file_path` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `image_path` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `activity_gallery_activitymedia_uploaded_by_id_f18377b0_fk`(`uploaded_by_id` ASC) USING BTREE,
  CONSTRAINT `activity_gallery_activitymedia_uploaded_by_id_f18377b0_fk` FOREIGN KEY (`uploaded_by_id`) REFERENCES `users_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of activity_gallery_activitymedia
-- ----------------------------
INSERT INTO `activity_gallery_activitymedia` VALUES (2, 'image', '/media/activity_media/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE%202026-01-08%20144008.png', '屏幕截图 2026-01-08 144008.png', 10148, '2026-01-20 07:00:55.684841', 13, 2, 'activity_media/屏幕截图 2026-01-08 144008.png', 'activity_media/屏幕截图 2026-01-08 144008.png');
INSERT INTO `activity_gallery_activitymedia` VALUES (3, 'image', '/media/activity_media/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE%202026-01-08%20144008_wztTwV2.png', '屏幕截图 2026-01-08 144008.png', 10148, '2026-01-26 10:19:08.815087', 14, 2, 'activity_media/屏幕截图 2026-01-08 144008_wztTwV2.png', 'activity_media/屏幕截图 2026-01-08 144008_wztTwV2.png');
INSERT INTO `activity_gallery_activitymedia` VALUES (4, 'video', '/media/activity_media/hmm.mp4', 'hmm.mp4', 26283944, '2026-01-26 10:19:08.843346', 14, 2, 'activity_media/hmm.mp4', '');

-- ----------------------------
-- Table structure for activity_gallery_activitymedia_patients
-- ----------------------------
DROP TABLE IF EXISTS `activity_gallery_activitymedia_patients`;
CREATE TABLE `activity_gallery_activitymedia_patients`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `activitymedia_id` bigint NOT NULL,
  `patient_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `activity_gallery_activ_activitymedia_id_patien_d3f3f218_uniq`(`activitymedia_id` ASC, `patient_id` ASC) USING BTREE,
  INDEX `activity_gallery_activitymedia_patients_patient_id_058d3de1_fk`(`patient_id` ASC) USING BTREE,
  CONSTRAINT `activity_gallery_activitymedia_patients_patient_id_058d3de1_fk` FOREIGN KEY (`patient_id`) REFERENCES `patients_patient` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of activity_gallery_activitymedia_patients
-- ----------------------------

-- ----------------------------
-- Table structure for activity_gallery_activityparticipant
-- ----------------------------
DROP TABLE IF EXISTS `activity_gallery_activityparticipant`;
CREATE TABLE `activity_gallery_activityparticipant`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `activity_id` bigint NOT NULL,
  `patient_id` int NOT NULL,
  `staff_id` bigint NULL DEFAULT NULL,
  `created_at` datetime(6) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `activity_gallery_activityparticipant_patient_id_d91c8946_fk`(`patient_id` ASC) USING BTREE,
  INDEX `activity_gallery_activityparticipant_staff_id_53f83af2_fk`(`staff_id` ASC) USING BTREE,
  CONSTRAINT `activity_gallery_activityparticipant_patient_id_d91c8946_fk` FOREIGN KEY (`patient_id`) REFERENCES `patients_patient` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `activity_gallery_activityparticipant_staff_id_53f83af2_fk` FOREIGN KEY (`staff_id`) REFERENCES `users_staffuser` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of activity_gallery_activityparticipant
-- ----------------------------

-- ----------------------------
-- Table structure for announcements_announcement
-- ----------------------------
DROP TABLE IF EXISTS `announcements_announcement`;
CREATE TABLE `announcements_announcement`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `content` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `target_role` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `publish_time` datetime(6) NOT NULL,
  `expire_time` datetime(6) NULL DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `created_by_id` bigint NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `announcements_announcement_created_by_id_79d7d337_fk`(`created_by_id` ASC) USING BTREE,
  CONSTRAINT `announcements_announcement_created_by_id_79d7d337_fk` FOREIGN KEY (`created_by_id`) REFERENCES `users_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of announcements_announcement
-- ----------------------------

-- ----------------------------
-- Table structure for appointments_appointment
-- ----------------------------
DROP TABLE IF EXISTS `appointments_appointment`;
CREATE TABLE `appointments_appointment`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `date` date NOT NULL,
  `time_slot` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `notes` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `approved_at` datetime(6) NULL DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `approved_by_id` bigint NULL DEFAULT NULL,
  `family_user_id` bigint NOT NULL,
  `patient_id` int NOT NULL,
  `staff_user_id` bigint NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `appointments_appointment_patient_id_631d13da_fk`(`patient_id` ASC) USING BTREE,
  INDEX `appointments_appointment_approved_by_id_bc3e294c_fk`(`approved_by_id` ASC) USING BTREE,
  INDEX `appointments_appointment_family_user_id_ccb1a70b_fk`(`family_user_id` ASC) USING BTREE,
  INDEX `appointments_appointment_staff_user_id_bb0f4550_fk`(`staff_user_id` ASC) USING BTREE,
  CONSTRAINT `appointments_appointment_approved_by_id_bc3e294c_fk` FOREIGN KEY (`approved_by_id`) REFERENCES `users_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `appointments_appointment_family_user_id_ccb1a70b_fk` FOREIGN KEY (`family_user_id`) REFERENCES `users_familyuser` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `appointments_appointment_patient_id_631d13da_fk` FOREIGN KEY (`patient_id`) REFERENCES `patients_patient` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `appointments_appointment_staff_user_id_bb0f4550_fk` FOREIGN KEY (`staff_user_id`) REFERENCES `users_staffuser` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of appointments_appointment
-- ----------------------------
INSERT INTO `appointments_appointment` VALUES (1, 'visit', '2026-01-29', '09:00-11:00', 'approved', '1.1', '2026-01-28 12:04:14.383333', '2026-01-28 12:03:52.118198', '2026-01-28 12:04:14.383333', 1, 9, 16, NULL);

-- ----------------------------
-- Table structure for appointments_appointmenttimeslot
-- ----------------------------
DROP TABLE IF EXISTS `appointments_appointmenttimeslot`;
CREATE TABLE `appointments_appointmenttimeslot`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `start_time` time(6) NOT NULL,
  `end_time` time(6) NOT NULL,
  `is_available` tinyint(1) NOT NULL,
  `max_appointments` int NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of appointments_appointmenttimeslot
-- ----------------------------

-- ----------------------------
-- Table structure for auth_group
-- ----------------------------
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_group
-- ----------------------------

-- ----------------------------
-- Table structure for auth_group_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_group_permissions_group_id_permission_id_0cd325b0_uniq`(`group_id` ASC, `permission_id` ASC) USING BTREE,
  INDEX `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm`(`permission_id` ASC) USING BTREE,
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_group_permissions
-- ----------------------------

-- ----------------------------
-- Table structure for auth_permission
-- ----------------------------
DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_permission_content_type_id_codename_01ab375a_uniq`(`content_type_id` ASC, `codename` ASC) USING BTREE,
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 205 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_permission
-- ----------------------------
INSERT INTO `auth_permission` VALUES (1, 'Can add log entry', 1, 'add_logentry');
INSERT INTO `auth_permission` VALUES (2, 'Can change log entry', 1, 'change_logentry');
INSERT INTO `auth_permission` VALUES (3, 'Can delete log entry', 1, 'delete_logentry');
INSERT INTO `auth_permission` VALUES (4, 'Can view log entry', 1, 'view_logentry');
INSERT INTO `auth_permission` VALUES (5, 'Can add permission', 2, 'add_permission');
INSERT INTO `auth_permission` VALUES (6, 'Can change permission', 2, 'change_permission');
INSERT INTO `auth_permission` VALUES (7, 'Can delete permission', 2, 'delete_permission');
INSERT INTO `auth_permission` VALUES (8, 'Can view permission', 2, 'view_permission');
INSERT INTO `auth_permission` VALUES (9, 'Can add group', 3, 'add_group');
INSERT INTO `auth_permission` VALUES (10, 'Can change group', 3, 'change_group');
INSERT INTO `auth_permission` VALUES (11, 'Can delete group', 3, 'delete_group');
INSERT INTO `auth_permission` VALUES (12, 'Can view group', 3, 'view_group');
INSERT INTO `auth_permission` VALUES (13, 'Can add content type', 4, 'add_contenttype');
INSERT INTO `auth_permission` VALUES (14, 'Can change content type', 4, 'change_contenttype');
INSERT INTO `auth_permission` VALUES (15, 'Can delete content type', 4, 'delete_contenttype');
INSERT INTO `auth_permission` VALUES (16, 'Can view content type', 4, 'view_contenttype');
INSERT INTO `auth_permission` VALUES (17, 'Can add session', 5, 'add_session');
INSERT INTO `auth_permission` VALUES (18, 'Can change session', 5, 'change_session');
INSERT INTO `auth_permission` VALUES (19, 'Can delete session', 5, 'delete_session');
INSERT INTO `auth_permission` VALUES (20, 'Can view session', 5, 'view_session');
INSERT INTO `auth_permission` VALUES (21, 'Can add 用户', 6, 'add_user');
INSERT INTO `auth_permission` VALUES (22, 'Can change 用户', 6, 'change_user');
INSERT INTO `auth_permission` VALUES (23, 'Can delete 用户', 6, 'delete_user');
INSERT INTO `auth_permission` VALUES (24, 'Can view 用户', 6, 'view_user');
INSERT INTO `auth_permission` VALUES (25, 'Can add 工作人员', 7, 'add_staffuser');
INSERT INTO `auth_permission` VALUES (26, 'Can change 工作人员', 7, 'change_staffuser');
INSERT INTO `auth_permission` VALUES (27, 'Can delete 工作人员', 7, 'delete_staffuser');
INSERT INTO `auth_permission` VALUES (28, 'Can view 工作人员', 7, 'view_staffuser');
INSERT INTO `auth_permission` VALUES (29, 'Can add 亲属用户', 8, 'add_familyuser');
INSERT INTO `auth_permission` VALUES (30, 'Can change 亲属用户', 8, 'change_familyuser');
INSERT INTO `auth_permission` VALUES (31, 'Can delete 亲属用户', 8, 'delete_familyuser');
INSERT INTO `auth_permission` VALUES (32, 'Can view 亲属用户', 8, 'view_familyuser');
INSERT INTO `auth_permission` VALUES (33, 'Can add 健康评估', 9, 'add_healthassessment');
INSERT INTO `auth_permission` VALUES (34, 'Can change 健康评估', 9, 'change_healthassessment');
INSERT INTO `auth_permission` VALUES (35, 'Can delete 健康评估', 9, 'delete_healthassessment');
INSERT INTO `auth_permission` VALUES (36, 'Can view 健康评估', 9, 'view_healthassessment');
INSERT INTO `auth_permission` VALUES (37, 'Can add 医疗记录', 10, 'add_medicalrecord');
INSERT INTO `auth_permission` VALUES (38, 'Can change 医疗记录', 10, 'change_medicalrecord');
INSERT INTO `auth_permission` VALUES (39, 'Can delete 医疗记录', 10, 'delete_medicalrecord');
INSERT INTO `auth_permission` VALUES (40, 'Can view 医疗记录', 10, 'view_medicalrecord');
INSERT INTO `auth_permission` VALUES (41, 'Can add 院民', 11, 'add_patient');
INSERT INTO `auth_permission` VALUES (42, 'Can change 院民', 11, 'change_patient');
INSERT INTO `auth_permission` VALUES (43, 'Can delete 院民', 11, 'delete_patient');
INSERT INTO `auth_permission` VALUES (44, 'Can view 院民', 11, 'view_patient');
INSERT INTO `auth_permission` VALUES (45, 'Can add 预约', 12, 'add_appointment');
INSERT INTO `auth_permission` VALUES (46, 'Can change 预约', 12, 'change_appointment');
INSERT INTO `auth_permission` VALUES (47, 'Can delete 预约', 12, 'delete_appointment');
INSERT INTO `auth_permission` VALUES (48, 'Can view 预约', 12, 'view_appointment');
INSERT INTO `auth_permission` VALUES (49, 'Can add 预约时间段', 13, 'add_appointmenttimeslot');
INSERT INTO `auth_permission` VALUES (50, 'Can change 预约时间段', 13, 'change_appointmenttimeslot');
INSERT INTO `auth_permission` VALUES (51, 'Can delete 预约时间段', 13, 'delete_appointmenttimeslot');
INSERT INTO `auth_permission` VALUES (52, 'Can view 预约时间段', 13, 'view_appointmenttimeslot');
INSERT INTO `auth_permission` VALUES (53, 'Can add 护理记录', 14, 'add_carerecord');
INSERT INTO `auth_permission` VALUES (54, 'Can change 护理记录', 14, 'change_carerecord');
INSERT INTO `auth_permission` VALUES (55, 'Can delete 护理记录', 14, 'delete_carerecord');
INSERT INTO `auth_permission` VALUES (56, 'Can view 护理记录', 14, 'view_carerecord');
INSERT INTO `auth_permission` VALUES (57, 'Can add 护理模板', 15, 'add_caretemplate');
INSERT INTO `auth_permission` VALUES (58, 'Can change 护理模板', 15, 'change_caretemplate');
INSERT INTO `auth_permission` VALUES (59, 'Can delete 护理模板', 15, 'delete_caretemplate');
INSERT INTO `auth_permission` VALUES (60, 'Can view 护理模板', 15, 'view_caretemplate');
INSERT INTO `auth_permission` VALUES (61, 'Can add 生命体征', 16, 'add_vitalsigns');
INSERT INTO `auth_permission` VALUES (62, 'Can change 生命体征', 16, 'change_vitalsigns');
INSERT INTO `auth_permission` VALUES (63, 'Can delete 生命体征', 16, 'delete_vitalsigns');
INSERT INTO `auth_permission` VALUES (64, 'Can view 生命体征', 16, 'view_vitalsigns');
INSERT INTO `auth_permission` VALUES (65, 'Can add 任务', 17, 'add_task');
INSERT INTO `auth_permission` VALUES (66, 'Can change 任务', 17, 'change_task');
INSERT INTO `auth_permission` VALUES (67, 'Can delete 任务', 17, 'delete_task');
INSERT INTO `auth_permission` VALUES (68, 'Can view 任务', 17, 'view_task');
INSERT INTO `auth_permission` VALUES (69, 'Can add 任务分配', 18, 'add_taskassignment');
INSERT INTO `auth_permission` VALUES (70, 'Can change 任务分配', 18, 'change_taskassignment');
INSERT INTO `auth_permission` VALUES (71, 'Can delete 任务分配', 18, 'delete_taskassignment');
INSERT INTO `auth_permission` VALUES (72, 'Can view 任务分配', 18, 'view_taskassignment');
INSERT INTO `auth_permission` VALUES (73, 'Can add 任务完成记录', 19, 'add_taskcompletion');
INSERT INTO `auth_permission` VALUES (74, 'Can change 任务完成记录', 19, 'change_taskcompletion');
INSERT INTO `auth_permission` VALUES (75, 'Can delete 任务完成记录', 19, 'delete_taskcompletion');
INSERT INTO `auth_permission` VALUES (76, 'Can view 任务完成记录', 19, 'view_taskcompletion');
INSERT INTO `auth_permission` VALUES (77, 'Can add Conversation', 20, 'add_conversation');
INSERT INTO `auth_permission` VALUES (78, 'Can change Conversation', 20, 'change_conversation');
INSERT INTO `auth_permission` VALUES (79, 'Can delete Conversation', 20, 'delete_conversation');
INSERT INTO `auth_permission` VALUES (80, 'Can view Conversation', 20, 'view_conversation');
INSERT INTO `auth_permission` VALUES (81, 'Can add Message', 21, 'add_message');
INSERT INTO `auth_permission` VALUES (82, 'Can change Message', 21, 'change_message');
INSERT INTO `auth_permission` VALUES (83, 'Can delete Message', 21, 'delete_message');
INSERT INTO `auth_permission` VALUES (84, 'Can view Message', 21, 'view_message');
INSERT INTO `auth_permission` VALUES (85, 'Can add Notification', 22, 'add_notification');
INSERT INTO `auth_permission` VALUES (86, 'Can change Notification', 22, 'change_notification');
INSERT INTO `auth_permission` VALUES (87, 'Can delete Notification', 22, 'delete_notification');
INSERT INTO `auth_permission` VALUES (88, 'Can view Notification', 22, 'view_notification');
INSERT INTO `auth_permission` VALUES (89, 'Can add 账单', 23, 'add_bill');
INSERT INTO `auth_permission` VALUES (90, 'Can change 账单', 23, 'change_bill');
INSERT INTO `auth_permission` VALUES (91, 'Can delete 账单', 23, 'delete_bill');
INSERT INTO `auth_permission` VALUES (92, 'Can view 账单', 23, 'view_bill');
INSERT INTO `auth_permission` VALUES (93, 'Can add 账单明细', 24, 'add_billitem');
INSERT INTO `auth_permission` VALUES (94, 'Can change 账单明细', 24, 'change_billitem');
INSERT INTO `auth_permission` VALUES (95, 'Can delete 账单明细', 24, 'delete_billitem');
INSERT INTO `auth_permission` VALUES (96, 'Can view 账单明细', 24, 'view_billitem');
INSERT INTO `auth_permission` VALUES (97, 'Can add 支付记录', 25, 'add_payment');
INSERT INTO `auth_permission` VALUES (98, 'Can change 支付记录', 25, 'change_payment');
INSERT INTO `auth_permission` VALUES (99, 'Can delete 支付记录', 25, 'delete_payment');
INSERT INTO `auth_permission` VALUES (100, 'Can view 支付记录', 25, 'view_payment');
INSERT INTO `auth_permission` VALUES (101, 'Can add 个性化服务申请', 26, 'add_customservicerequest');
INSERT INTO `auth_permission` VALUES (102, 'Can change 个性化服务申请', 26, 'change_customservicerequest');
INSERT INTO `auth_permission` VALUES (103, 'Can delete 个性化服务申请', 26, 'delete_customservicerequest');
INSERT INTO `auth_permission` VALUES (104, 'Can view 个性化服务申请', 26, 'view_customservicerequest');
INSERT INTO `auth_permission` VALUES (105, 'Can add 服务', 27, 'add_service');
INSERT INTO `auth_permission` VALUES (106, 'Can change 服务', 27, 'change_service');
INSERT INTO `auth_permission` VALUES (107, 'Can delete 服务', 27, 'delete_service');
INSERT INTO `auth_permission` VALUES (108, 'Can view 服务', 27, 'view_service');
INSERT INTO `auth_permission` VALUES (109, 'Can add 服务执行记录', 28, 'add_serviceexecution');
INSERT INTO `auth_permission` VALUES (110, 'Can change 服务执行记录', 28, 'change_serviceexecution');
INSERT INTO `auth_permission` VALUES (111, 'Can delete 服务执行记录', 28, 'delete_serviceexecution');
INSERT INTO `auth_permission` VALUES (112, 'Can view 服务执行记录', 28, 'view_serviceexecution');
INSERT INTO `auth_permission` VALUES (113, 'Can add 床位', 29, 'add_bed');
INSERT INTO `auth_permission` VALUES (114, 'Can change 床位', 29, 'change_bed');
INSERT INTO `auth_permission` VALUES (115, 'Can delete 床位', 29, 'delete_bed');
INSERT INTO `auth_permission` VALUES (116, 'Can view 床位', 29, 'view_bed');
INSERT INTO `auth_permission` VALUES (117, 'Can add 床位分配', 30, 'add_bedassignment');
INSERT INTO `auth_permission` VALUES (118, 'Can change 床位分配', 30, 'change_bedassignment');
INSERT INTO `auth_permission` VALUES (119, 'Can delete 床位分配', 30, 'delete_bedassignment');
INSERT INTO `auth_permission` VALUES (120, 'Can view 床位分配', 30, 'view_bedassignment');
INSERT INTO `auth_permission` VALUES (121, 'Can add 房间', 31, 'add_room');
INSERT INTO `auth_permission` VALUES (122, 'Can change 房间', 31, 'change_room');
INSERT INTO `auth_permission` VALUES (123, 'Can delete 房间', 31, 'delete_room');
INSERT INTO `auth_permission` VALUES (124, 'Can view 房间', 31, 'view_room');
INSERT INTO `auth_permission` VALUES (125, 'Can add 保洁请求', 32, 'add_cleaningrequest');
INSERT INTO `auth_permission` VALUES (126, 'Can change 保洁请求', 32, 'change_cleaningrequest');
INSERT INTO `auth_permission` VALUES (127, 'Can delete 保洁请求', 32, 'delete_cleaningrequest');
INSERT INTO `auth_permission` VALUES (128, 'Can view 保洁请求', 32, 'view_cleaningrequest');
INSERT INTO `auth_permission` VALUES (129, 'Can add 活动', 33, 'add_activity');
INSERT INTO `auth_permission` VALUES (130, 'Can change 活动', 33, 'change_activity');
INSERT INTO `auth_permission` VALUES (131, 'Can delete 活动', 33, 'delete_activity');
INSERT INTO `auth_permission` VALUES (132, 'Can view 活动', 33, 'view_activity');
INSERT INTO `auth_permission` VALUES (133, 'Can add 活动媒体', 34, 'add_activitymedia');
INSERT INTO `auth_permission` VALUES (134, 'Can change 活动媒体', 34, 'change_activitymedia');
INSERT INTO `auth_permission` VALUES (135, 'Can delete 活动媒体', 34, 'delete_activitymedia');
INSERT INTO `auth_permission` VALUES (136, 'Can view 活动媒体', 34, 'view_activitymedia');
INSERT INTO `auth_permission` VALUES (137, 'Can add 活动参与者', 35, 'add_activityparticipant');
INSERT INTO `auth_permission` VALUES (138, 'Can change 活动参与者', 35, 'change_activityparticipant');
INSERT INTO `auth_permission` VALUES (139, 'Can delete 活动参与者', 35, 'delete_activityparticipant');
INSERT INTO `auth_permission` VALUES (140, 'Can view 活动参与者', 35, 'view_activityparticipant');
INSERT INTO `auth_permission` VALUES (141, 'Can add 关怀提醒', 36, 'add_carereminder');
INSERT INTO `auth_permission` VALUES (142, 'Can change 关怀提醒', 36, 'change_carereminder');
INSERT INTO `auth_permission` VALUES (143, 'Can delete 关怀提醒', 36, 'delete_carereminder');
INSERT INTO `auth_permission` VALUES (144, 'Can view 关怀提醒', 36, 'view_carereminder');
INSERT INTO `auth_permission` VALUES (145, 'Can add 通知', 37, 'add_notification');
INSERT INTO `auth_permission` VALUES (146, 'Can change 通知', 37, 'change_notification');
INSERT INTO `auth_permission` VALUES (147, 'Can delete 通知', 37, 'delete_notification');
INSERT INTO `auth_permission` VALUES (148, 'Can view 通知', 37, 'view_notification');
INSERT INTO `auth_permission` VALUES (149, 'Can add 提醒参与记录', 38, 'add_reminderparticipation');
INSERT INTO `auth_permission` VALUES (150, 'Can change 提醒参与记录', 38, 'change_reminderparticipation');
INSERT INTO `auth_permission` VALUES (151, 'Can delete 提醒参与记录', 38, 'delete_reminderparticipation');
INSERT INTO `auth_permission` VALUES (152, 'Can view 提醒参与记录', 38, 'view_reminderparticipation');
INSERT INTO `auth_permission` VALUES (153, 'Can add 房间信息', 39, 'add_room');
INSERT INTO `auth_permission` VALUES (154, 'Can change 房间信息', 39, 'change_room');
INSERT INTO `auth_permission` VALUES (155, 'Can delete 房间信息', 39, 'delete_room');
INSERT INTO `auth_permission` VALUES (156, 'Can view 房间信息', 39, 'view_room');
INSERT INTO `auth_permission` VALUES (157, 'Can add 公告', 40, 'add_announcement');
INSERT INTO `auth_permission` VALUES (158, 'Can change 公告', 40, 'change_announcement');
INSERT INTO `auth_permission` VALUES (159, 'Can delete 公告', 40, 'delete_announcement');
INSERT INTO `auth_permission` VALUES (160, 'Can view 公告', 40, 'view_announcement');
INSERT INTO `auth_permission` VALUES (161, 'Can add 请假申请', 41, 'add_leaverequest');
INSERT INTO `auth_permission` VALUES (162, 'Can change 请假申请', 41, 'change_leaverequest');
INSERT INTO `auth_permission` VALUES (163, 'Can delete 请假申请', 41, 'delete_leaverequest');
INSERT INTO `auth_permission` VALUES (164, 'Can view 请假申请', 41, 'view_leaverequest');
INSERT INTO `auth_permission` VALUES (165, 'Can add 院民健康记录', 42, 'add_patienthealthrecord');
INSERT INTO `auth_permission` VALUES (166, 'Can change 院民健康记录', 42, 'change_patienthealthrecord');
INSERT INTO `auth_permission` VALUES (167, 'Can delete 院民健康记录', 42, 'delete_patienthealthrecord');
INSERT INTO `auth_permission` VALUES (168, 'Can view 院民健康记录', 42, 'view_patienthealthrecord');
INSERT INTO `auth_permission` VALUES (169, 'Can add 院民档案', 43, 'add_patientdocument');
INSERT INTO `auth_permission` VALUES (170, 'Can change 院民档案', 43, 'change_patientdocument');
INSERT INTO `auth_permission` VALUES (171, 'Can delete 院民档案', 43, 'delete_patientdocument');
INSERT INTO `auth_permission` VALUES (172, 'Can view 院民档案', 43, 'view_patientdocument');
INSERT INTO `auth_permission` VALUES (173, 'Can add 公告阅读状态', 44, 'add_announcementreadstatus');
INSERT INTO `auth_permission` VALUES (174, 'Can change 公告阅读状态', 44, 'change_announcementreadstatus');
INSERT INTO `auth_permission` VALUES (175, 'Can delete 公告阅读状态', 44, 'delete_announcementreadstatus');
INSERT INTO `auth_permission` VALUES (176, 'Can view 公告阅读状态', 44, 'view_announcementreadstatus');
INSERT INTO `auth_permission` VALUES (177, 'Can add 注册申请', 45, 'add_registerapplication');
INSERT INTO `auth_permission` VALUES (178, 'Can change 注册申请', 45, 'change_registerapplication');
INSERT INTO `auth_permission` VALUES (179, 'Can delete 注册申请', 45, 'delete_registerapplication');
INSERT INTO `auth_permission` VALUES (180, 'Can view 注册申请', 45, 'view_registerapplication');
INSERT INTO `auth_permission` VALUES (181, 'Can add Service Feedback', 46, 'add_servicefeedback');
INSERT INTO `auth_permission` VALUES (182, 'Can change Service Feedback', 46, 'change_servicefeedback');
INSERT INTO `auth_permission` VALUES (183, 'Can delete Service Feedback', 46, 'delete_servicefeedback');
INSERT INTO `auth_permission` VALUES (184, 'Can view Service Feedback', 46, 'view_servicefeedback');
INSERT INTO `auth_permission` VALUES (185, 'Can add Service Order', 47, 'add_serviceorder');
INSERT INTO `auth_permission` VALUES (186, 'Can change Service Order', 47, 'change_serviceorder');
INSERT INTO `auth_permission` VALUES (187, 'Can delete Service Order', 47, 'delete_serviceorder');
INSERT INTO `auth_permission` VALUES (188, 'Can view Service Order', 47, 'view_serviceorder');
INSERT INTO `auth_permission` VALUES (189, 'Can add Service Review', 48, 'add_servicereview');
INSERT INTO `auth_permission` VALUES (190, 'Can change Service Review', 48, 'change_servicereview');
INSERT INTO `auth_permission` VALUES (191, 'Can delete Service Review', 48, 'delete_servicereview');
INSERT INTO `auth_permission` VALUES (192, 'Can view Service Review', 48, 'view_servicereview');
INSERT INTO `auth_permission` VALUES (193, 'Can add Order Item', 49, 'add_serviceorderitem');
INSERT INTO `auth_permission` VALUES (194, 'Can change Order Item', 49, 'change_serviceorderitem');
INSERT INTO `auth_permission` VALUES (195, 'Can delete Order Item', 49, 'delete_serviceorderitem');
INSERT INTO `auth_permission` VALUES (196, 'Can view Order Item', 49, 'view_serviceorderitem');
INSERT INTO `auth_permission` VALUES (197, 'Can add Feedback Image', 50, 'add_servicefeedbackimage');
INSERT INTO `auth_permission` VALUES (198, 'Can change Feedback Image', 50, 'change_servicefeedbackimage');
INSERT INTO `auth_permission` VALUES (199, 'Can delete Feedback Image', 50, 'delete_servicefeedbackimage');
INSERT INTO `auth_permission` VALUES (200, 'Can view Feedback Image', 50, 'view_servicefeedbackimage');
INSERT INTO `auth_permission` VALUES (201, 'Can add Daily Care Task', 51, 'add_dailycaretask');
INSERT INTO `auth_permission` VALUES (202, 'Can change Daily Care Task', 51, 'change_dailycaretask');
INSERT INTO `auth_permission` VALUES (203, 'Can delete Daily Care Task', 51, 'delete_dailycaretask');
INSERT INTO `auth_permission` VALUES (204, 'Can view Daily Care Task', 51, 'view_dailycaretask');

-- ----------------------------
-- Table structure for bed_scheduling_bedassignment
-- ----------------------------
DROP TABLE IF EXISTS `bed_scheduling_bedassignment`;
CREATE TABLE `bed_scheduling_bedassignment`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `bed_number` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `assign_date` datetime(6) NOT NULL,
  `release_date` datetime(6) NULL DEFAULT NULL,
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `notes` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `cleaning_notified` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `assigned_by_id` bigint NULL DEFAULT NULL,
  `elderly_id` int NOT NULL,
  `room_id` bigint NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `bed_scheduling_bedas_assigned_by_id_52de195f_fk_users_use`(`assigned_by_id` ASC) USING BTREE,
  INDEX `bed_scheduling_bedas_elderly_id_da5a9155_fk_patients_`(`elderly_id` ASC) USING BTREE,
  INDEX `bed_scheduling_bedassignment_room_id_ed1982d3_fk_rooms_id`(`room_id` ASC) USING BTREE,
  CONSTRAINT `bed_scheduling_bedas_assigned_by_id_52de195f_fk_users_use` FOREIGN KEY (`assigned_by_id`) REFERENCES `users_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `bed_scheduling_bedas_elderly_id_da5a9155_fk_patients_` FOREIGN KEY (`elderly_id`) REFERENCES `patients_patient` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `bed_scheduling_bedassignment_room_id_ed1982d3_fk_rooms_id` FOREIGN KEY (`room_id`) REFERENCES `rooms` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of bed_scheduling_bedassignment
-- ----------------------------
INSERT INTO `bed_scheduling_bedassignment` VALUES (1, '1', '2026-02-05 13:24:22.490907', '2026-02-05 15:41:15.514670', 'completed', '', 1, '2026-02-05 13:24:22.492470', '2026-02-05 15:41:15.514670', 1, 1, 1);
INSERT INTO `bed_scheduling_bedassignment` VALUES (2, '1', '2026-02-05 13:25:00.899506', '2026-02-05 15:41:15.511546', 'completed', '', 1, '2026-02-05 13:25:00.901038', '2026-02-05 15:41:15.511546', 1, 1, 1);
INSERT INTO `bed_scheduling_bedassignment` VALUES (3, '2', '2026-02-05 13:12:05.801000', NULL, 'active', '', 1, '2026-02-05 13:29:18.624100', '2026-02-05 13:29:18.624100', 1, 1, 1);
INSERT INTO `bed_scheduling_bedassignment` VALUES (4, '2', '2026-02-05 13:12:05.801000', NULL, 'active', '', 1, '2026-02-05 13:29:59.589878', '2026-02-05 13:29:59.589878', 2, 19, 1);
INSERT INTO `bed_scheduling_bedassignment` VALUES (5, '3', '2026-02-05 13:12:05.801000', NULL, 'active', '', 1, '2026-02-05 13:46:03.352967', '2026-02-05 13:46:03.352967', 2, 1, 1);
INSERT INTO `bed_scheduling_bedassignment` VALUES (6, '1', '2026-02-05 15:40:09.801000', '2026-02-05 20:22:30.500072', 'completed', '', 1, '2026-02-05 15:41:36.735587', '2026-02-05 20:22:30.500072', 10, 1, 1);
INSERT INTO `bed_scheduling_bedassignment` VALUES (7, '1', '2026-02-05 20:33:28.694000', NULL, 'active', '', 1, '2026-02-05 20:34:11.104095', '2026-02-05 20:34:11.104095', 10, 1, 1);

-- ----------------------------
-- Table structure for care_records_carerecord
-- ----------------------------
DROP TABLE IF EXISTS `care_records_carerecord`;
CREATE TABLE `care_records_carerecord`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `record_date` date NOT NULL,
  `record_time` time(6) NOT NULL,
  `vital_signs` json NULL,
  `diet` json NULL,
  `sleep` json NULL,
  `bowel_movement` json NULL,
  `mental_state` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `medications` json NULL,
  `care_activities` json NULL,
  `notes` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `patient_id` int NOT NULL,
  `staff_id` bigint NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `care_records_carerecord_patient_id_dc6027a6_fk`(`patient_id` ASC) USING BTREE,
  INDEX `care_records_carerec_staff_id_e0b85e50_fk_users_sta`(`staff_id` ASC) USING BTREE,
  CONSTRAINT `care_records_carerec_staff_id_e0b85e50_fk_users_sta` FOREIGN KEY (`staff_id`) REFERENCES `users_staffuser` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `care_records_carerecord_patient_id_dc6027a6_fk` FOREIGN KEY (`patient_id`) REFERENCES `patients_patient` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of care_records_carerecord
-- ----------------------------

-- ----------------------------
-- Table structure for care_records_caretemplate
-- ----------------------------
DROP TABLE IF EXISTS `care_records_caretemplate`;
CREATE TABLE `care_records_caretemplate`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `care_level` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `template_content` json NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `created_by_id` bigint NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `care_records_caretemplate_created_by_id_5ec8557c_fk`(`created_by_id` ASC) USING BTREE,
  CONSTRAINT `care_records_caretemplate_created_by_id_5ec8557c_fk` FOREIGN KEY (`created_by_id`) REFERENCES `users_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of care_records_caretemplate
-- ----------------------------
INSERT INTO `care_records_caretemplate` VALUES (1, '基础护理模板', '一级护理', '{\"fields\": [{\"key\": \"vital_signs\", \"type\": \"group\", \"label\": \"生命体征\", \"children\": [{\"key\": \"temperature\", \"step\": 0.1, \"type\": \"number\", \"label\": \"体温(°C)\", \"required\": true}, {\"key\": \"blood_pressure\", \"type\": \"text\", \"label\": \"血压(mmHg)\", \"required\": true, \"placeholder\": \"收缩压/舒张压\"}, {\"key\": \"heart_rate\", \"type\": \"number\", \"label\": \"心率(次/分)\", \"required\": true}]}, {\"key\": \"diet\", \"type\": \"group\", \"label\": \"饮食记录\", \"children\": [{\"key\": \"breakfast\", \"type\": \"select\", \"label\": \"早餐\", \"options\": [\"全部食用\", \"部分食用\", \"未食用\"], \"required\": true}, {\"key\": \"lunch\", \"type\": \"select\", \"label\": \"午餐\", \"options\": [\"全部食用\", \"部分食用\", \"未食用\"], \"required\": true}, {\"key\": \"dinner\", \"type\": \"select\", \"label\": \"晚餐\", \"options\": [\"全部食用\", \"部分食用\", \"未食用\"], \"required\": true}, {\"key\": \"water_intake\", \"type\": \"number\", \"label\": \"饮水量(ml)\", \"required\": false}]}, {\"key\": \"mental_state\", \"type\": \"select\", \"label\": \"精神状态\", \"options\": [\"良好\", \"平静\", \"烦躁\", \"抑郁\", \"其他\"], \"required\": true}, {\"key\": \"notes\", \"type\": \"textarea\", \"label\": \"备注\", \"required\": false}]}', 1, '2026-01-26 09:53:33.109142', '2026-01-26 09:53:33.109142', 1);
INSERT INTO `care_records_caretemplate` VALUES (2, '高级护理模板', '特级护理', '{\"fields\": [{\"key\": \"vital_signs\", \"type\": \"group\", \"label\": \"生命体征\", \"children\": [{\"key\": \"temperature\", \"step\": 0.1, \"type\": \"number\", \"label\": \"体温(°C)\", \"required\": true}, {\"key\": \"blood_pressure\", \"type\": \"text\", \"label\": \"血压(mmHg)\", \"required\": true}, {\"key\": \"heart_rate\", \"type\": \"number\", \"label\": \"心率(次/分)\", \"required\": true}, {\"key\": \"respiratory_rate\", \"type\": \"number\", \"label\": \"呼吸(次/分)\", \"required\": true}, {\"key\": \"oxygen_saturation\", \"type\": \"number\", \"label\": \"血氧(%)\", \"required\": true}]}, {\"key\": \"special_care\", \"type\": \"checkbox_group\", \"label\": \"专项护理\", \"options\": [\"翻身拍背\", \"吸痰\", \"口腔护理\", \"会阴护理\", \"鼻饲\"], \"required\": false}, {\"key\": \"diet\", \"type\": \"group\", \"label\": \"饮食/营养\", \"children\": [{\"key\": \"meal_type\", \"type\": \"select\", \"label\": \"进食方式\", \"options\": [\"自主进食\", \"协助进食\", \"鼻饲\"], \"required\": true}, {\"key\": \"intake_amount\", \"type\": \"select\", \"label\": \"进食量\", \"options\": [\"正常\", \"偏少\", \"拒食\"], \"required\": true}]}, {\"key\": \"excretion\", \"type\": \"group\", \"label\": \"排泄\", \"children\": [{\"key\": \"urination\", \"type\": \"select\", \"label\": \"小便\", \"options\": [\"正常\", \"失禁\", \"留置导尿\"], \"required\": true}, {\"key\": \"defecation\", \"type\": \"select\", \"label\": \"大便\", \"options\": [\"正常\", \"便秘\", \"腹泻\", \"失禁\"], \"required\": true}]}, {\"key\": \"skin_condition\", \"type\": \"select\", \"label\": \"皮肤状况\", \"options\": [\"完好\", \"压红\", \"破损\", \"压疮\"], \"required\": true}, {\"key\": \"mental_state\", \"type\": \"select\", \"label\": \"意识/精神\", \"options\": [\"清醒\", \"嗜睡\", \"昏迷\", \"躁动\"], \"required\": true}, {\"key\": \"notes\", \"type\": \"textarea\", \"label\": \"交班/备注\", \"required\": false}]}', 1, '2026-01-26 09:53:33.122867', '2026-01-26 09:53:33.122867', 1);
INSERT INTO `care_records_caretemplate` VALUES (3, '通用护理模板', '通用', '{\"fields\": [{\"key\": \"vital_signs\", \"type\": \"group\", \"label\": \"生命体征\", \"children\": [{\"key\": \"temperature\", \"step\": 0.1, \"type\": \"number\", \"label\": \"体温(°C)\", \"required\": true}, {\"key\": \"blood_pressure\", \"type\": \"text\", \"label\": \"血压(mmHg)\", \"required\": true, \"placeholder\": \"收缩压/舒张压\"}, {\"key\": \"heart_rate\", \"type\": \"number\", \"label\": \"心率(次/分)\", \"required\": true}]}, {\"key\": \"diet\", \"type\": \"group\", \"label\": \"饮食记录\", \"children\": [{\"key\": \"breakfast\", \"type\": \"select\", \"label\": \"早餐\", \"options\": [\"全部食用\", \"部分食用\", \"未食用\"], \"required\": true}, {\"key\": \"lunch\", \"type\": \"select\", \"label\": \"午餐\", \"options\": [\"全部食用\", \"部分食用\", \"未食用\"], \"required\": true}, {\"key\": \"dinner\", \"type\": \"select\", \"label\": \"晚餐\", \"options\": [\"全部食用\", \"部分食用\", \"未食用\"], \"required\": true}, {\"key\": \"water_intake\", \"type\": \"number\", \"label\": \"饮水量(ml)\", \"required\": false}]}, {\"key\": \"mental_state\", \"type\": \"select\", \"label\": \"精神状态\", \"options\": [\"良好\", \"平静\", \"烦躁\", \"抑郁\", \"其他\"], \"required\": true}, {\"key\": \"notes\", \"type\": \"textarea\", \"label\": \"备注\", \"required\": false}]}', 1, '2026-01-26 09:53:33.127006', '2026-01-26 09:53:33.127006', 1);

-- ----------------------------
-- Table structure for care_records_dailycaretask
-- ----------------------------
DROP TABLE IF EXISTS `care_records_dailycaretask`;
CREATE TABLE `care_records_dailycaretask`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `task_date` date NOT NULL,
  `vital_signs_normal` tinyint(1) NOT NULL,
  `diet_normal` tinyint(1) NOT NULL,
  `mental_normal` tinyint(1) NOT NULL,
  `is_completed` tinyint(1) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `last_updated_by_id` bigint NULL DEFAULT NULL,
  `patient_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `care_records_dailycaretask_patient_id_task_date_dff4da9c_uniq`(`patient_id` ASC, `task_date` ASC) USING BTREE,
  INDEX `care_records_dailyca_last_updated_by_id_06761eaf_fk_users_sta`(`last_updated_by_id` ASC) USING BTREE,
  CONSTRAINT `care_records_dailyca_last_updated_by_id_06761eaf_fk_users_sta` FOREIGN KEY (`last_updated_by_id`) REFERENCES `users_staffuser` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `care_records_dailyca_patient_id_16c808c8_fk_patients_` FOREIGN KEY (`patient_id`) REFERENCES `patients_patient` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 13 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of care_records_dailycaretask
-- ----------------------------
INSERT INTO `care_records_dailycaretask` VALUES (1, '2026-01-30', 1, 1, 1, 1, '2026-01-30 16:29:23.711811', 2, 1);
INSERT INTO `care_records_dailycaretask` VALUES (2, '2026-01-30', 1, 1, 1, 1, '2026-01-30 16:29:23.714854', 2, 2);
INSERT INTO `care_records_dailycaretask` VALUES (3, '2026-01-30', 1, 1, 1, 1, '2026-01-30 16:29:23.716443', 2, 16);
INSERT INTO `care_records_dailycaretask` VALUES (4, '2026-01-30', 1, 1, 1, 1, '2026-01-30 16:29:23.717271', 2, 17);
INSERT INTO `care_records_dailycaretask` VALUES (5, '2026-01-30', 1, 1, 1, 1, '2026-01-30 16:29:23.717799', 2, 18);
INSERT INTO `care_records_dailycaretask` VALUES (6, '2026-01-30', 1, 1, 1, 1, '2026-01-30 16:29:23.719340', 2, 19);
INSERT INTO `care_records_dailycaretask` VALUES (7, '2026-02-05', 1, 1, 1, 1, '2026-02-05 14:07:33.027720', 2, 1);
INSERT INTO `care_records_dailycaretask` VALUES (8, '2026-02-05', 1, 1, 1, 1, '2026-02-05 14:07:33.029260', 2, 2);
INSERT INTO `care_records_dailycaretask` VALUES (9, '2026-02-05', 1, 1, 1, 1, '2026-02-05 14:07:33.030784', 2, 16);
INSERT INTO `care_records_dailycaretask` VALUES (10, '2026-02-05', 1, 1, 1, 1, '2026-02-05 14:07:33.030784', 2, 17);
INSERT INTO `care_records_dailycaretask` VALUES (11, '2026-02-05', 1, 1, 1, 1, '2026-02-05 14:07:33.032371', 2, 18);
INSERT INTO `care_records_dailycaretask` VALUES (12, '2026-02-05', 1, 1, 1, 1, '2026-02-05 14:07:33.032371', 2, 19);

-- ----------------------------
-- Table structure for care_records_vitalsigns
-- ----------------------------
DROP TABLE IF EXISTS `care_records_vitalsigns`;
CREATE TABLE `care_records_vitalsigns`  (
  `care_record_id` bigint NOT NULL,
  `temperature` decimal(5, 2) NULL DEFAULT NULL,
  `heart_rate` int NULL DEFAULT NULL,
  `respiratory_rate` int NULL DEFAULT NULL,
  `blood_oxygen` int NULL DEFAULT NULL,
  `diastolic_pressure` int NULL DEFAULT NULL,
  `systolic_pressure` int NULL DEFAULT NULL,
  PRIMARY KEY (`care_record_id`) USING BTREE,
  CONSTRAINT `care_records_vitalsi_care_record_id_1158d0e2_fk_care_reco` FOREIGN KEY (`care_record_id`) REFERENCES `care_records_carerecord` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of care_records_vitalsigns
-- ----------------------------

-- ----------------------------
-- Table structure for communication_conversation
-- ----------------------------
DROP TABLE IF EXISTS `communication_conversation`;
CREATE TABLE `communication_conversation`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `updated_at` datetime(6) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `last_message_id` bigint NULL DEFAULT NULL,
  `patient_id` int NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `communication_conver_last_message_id_47721bd6_fk_communica`(`last_message_id` ASC) USING BTREE,
  INDEX `communication_conversation_patient_id_23cad0bb_fk`(`patient_id` ASC) USING BTREE,
  CONSTRAINT `communication_conver_last_message_id_47721bd6_fk_communica` FOREIGN KEY (`last_message_id`) REFERENCES `communication_message` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `communication_conversation_patient_id_23cad0bb_fk` FOREIGN KEY (`patient_id`) REFERENCES `patients_patient` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of communication_conversation
-- ----------------------------

-- ----------------------------
-- Table structure for communication_conversation_participants
-- ----------------------------
DROP TABLE IF EXISTS `communication_conversation_participants`;
CREATE TABLE `communication_conversation_participants`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `conversation_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `communication_conversati_conversation_id_user_id_5ccf0df7_uniq`(`conversation_id` ASC, `user_id` ASC) USING BTREE,
  INDEX `communication_conversation_participants_user_id_21a3bebd_fk`(`user_id` ASC) USING BTREE,
  CONSTRAINT `communication_conver_conversation_id_0fe30449_fk_communica` FOREIGN KEY (`conversation_id`) REFERENCES `communication_conversation` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `communication_conversation_participants_user_id_21a3bebd_fk` FOREIGN KEY (`user_id`) REFERENCES `users_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of communication_conversation_participants
-- ----------------------------

-- ----------------------------
-- Table structure for communication_message
-- ----------------------------
DROP TABLE IF EXISTS `communication_message`;
CREATE TABLE `communication_message`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `content` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `duration` int NULL DEFAULT NULL,
  `file_url` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `is_read` tinyint(1) NOT NULL,
  `read_at` datetime(6) NULL DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `patient_id` int NULL DEFAULT NULL,
  `receiver_id` bigint NULL DEFAULT NULL,
  `sender_id` bigint NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `communication_message_patient_id_048ddaac_fk`(`patient_id` ASC) USING BTREE,
  INDEX `communication_message_receiver_id_a453b719_fk`(`receiver_id` ASC) USING BTREE,
  INDEX `communication_message_sender_id_11380a9e_fk`(`sender_id` ASC) USING BTREE,
  CONSTRAINT `communication_message_patient_id_048ddaac_fk` FOREIGN KEY (`patient_id`) REFERENCES `patients_patient` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `communication_message_receiver_id_a453b719_fk` FOREIGN KEY (`receiver_id`) REFERENCES `users_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `communication_message_sender_id_11380a9e_fk` FOREIGN KEY (`sender_id`) REFERENCES `users_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of communication_message
-- ----------------------------
INSERT INTO `communication_message` VALUES (1, 'text', '你好', NULL, NULL, 'sent', 0, NULL, '2026-01-17 07:28:22.117736', '2026-01-17 07:28:22.117736', NULL, 4, 2);
INSERT INTO `communication_message` VALUES (2, 'text', '你好', NULL, NULL, 'sent', 0, NULL, '2026-01-28 12:15:38.418189', '2026-01-28 12:15:38.418189', NULL, 2, 9);
INSERT INTO `communication_message` VALUES (3, 'text', '你好', NULL, NULL, 'sent', 0, NULL, '2026-02-05 15:47:39.784304', '2026-02-05 15:47:39.784304', NULL, 4, 10);
INSERT INTO `communication_message` VALUES (4, 'text', '你好', NULL, NULL, 'sent', 0, NULL, '2026-02-05 15:53:05.649034', '2026-02-05 15:53:05.649034', NULL, 4, 10);
INSERT INTO `communication_message` VALUES (5, 'text', '在吗', NULL, NULL, 'sent', 0, NULL, '2026-02-05 16:45:14.673629', '2026-02-05 16:45:14.673629', NULL, 4, 10);
INSERT INTO `communication_message` VALUES (6, 'text', '你好', NULL, NULL, 'sent', 0, NULL, '2026-02-06 14:49:19.995197', '2026-02-06 14:49:19.995197', NULL, 10, 9);

-- ----------------------------
-- Table structure for communication_notification
-- ----------------------------
DROP TABLE IF EXISTS `communication_notification`;
CREATE TABLE `communication_notification`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `content` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `related_id` int NULL DEFAULT NULL,
  `related_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `read_at` datetime(6) NULL DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `communication_notification_user_id_6611ccd5_fk`(`user_id` ASC) USING BTREE,
  CONSTRAINT `communication_notification_user_id_6611ccd5_fk` FOREIGN KEY (`user_id`) REFERENCES `users_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of communication_notification
-- ----------------------------

-- ----------------------------
-- Table structure for django_admin_log
-- ----------------------------
DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE `django_admin_log`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `object_repr` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `action_flag` smallint UNSIGNED NOT NULL,
  `change_message` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `content_type_id` int NULL DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `django_admin_log_content_type_id_c4bce8eb_fk_django_co`(`content_type_id` ASC) USING BTREE,
  INDEX `django_admin_log_user_id_c564eba6_fk`(`user_id` ASC) USING BTREE,
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk` FOREIGN KEY (`user_id`) REFERENCES `users_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `django_admin_log_chk_1` CHECK (`action_flag` >= 0)
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_admin_log
-- ----------------------------

-- ----------------------------
-- Table structure for django_content_type
-- ----------------------------
DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `model` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `django_content_type_app_label_model_76bd3d3b_uniq`(`app_label` ASC, `model` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 52 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_content_type
-- ----------------------------
INSERT INTO `django_content_type` VALUES (33, 'activity_gallery', 'activity');
INSERT INTO `django_content_type` VALUES (34, 'activity_gallery', 'activitymedia');
INSERT INTO `django_content_type` VALUES (35, 'activity_gallery', 'activityparticipant');
INSERT INTO `django_content_type` VALUES (1, 'admin', 'logentry');
INSERT INTO `django_content_type` VALUES (40, 'announcements', 'announcement');
INSERT INTO `django_content_type` VALUES (44, 'announcements', 'announcementreadstatus');
INSERT INTO `django_content_type` VALUES (12, 'appointments', 'appointment');
INSERT INTO `django_content_type` VALUES (13, 'appointments', 'appointmenttimeslot');
INSERT INTO `django_content_type` VALUES (3, 'auth', 'group');
INSERT INTO `django_content_type` VALUES (2, 'auth', 'permission');
INSERT INTO `django_content_type` VALUES (29, 'bed_scheduling', 'bed');
INSERT INTO `django_content_type` VALUES (30, 'bed_scheduling', 'bedassignment');
INSERT INTO `django_content_type` VALUES (32, 'bed_scheduling', 'cleaningrequest');
INSERT INTO `django_content_type` VALUES (31, 'bed_scheduling', 'room');
INSERT INTO `django_content_type` VALUES (14, 'care_records', 'carerecord');
INSERT INTO `django_content_type` VALUES (15, 'care_records', 'caretemplate');
INSERT INTO `django_content_type` VALUES (51, 'care_records', 'dailycaretask');
INSERT INTO `django_content_type` VALUES (16, 'care_records', 'vitalsigns');
INSERT INTO `django_content_type` VALUES (20, 'communication', 'conversation');
INSERT INTO `django_content_type` VALUES (21, 'communication', 'message');
INSERT INTO `django_content_type` VALUES (22, 'communication', 'notification');
INSERT INTO `django_content_type` VALUES (4, 'contenttypes', 'contenttype');
INSERT INTO `django_content_type` VALUES (36, 'notifications', 'carereminder');
INSERT INTO `django_content_type` VALUES (37, 'notifications', 'notification');
INSERT INTO `django_content_type` VALUES (38, 'notifications', 'reminderparticipation');
INSERT INTO `django_content_type` VALUES (9, 'patients', 'healthassessment');
INSERT INTO `django_content_type` VALUES (10, 'patients', 'medicalrecord');
INSERT INTO `django_content_type` VALUES (11, 'patients', 'patient');
INSERT INTO `django_content_type` VALUES (43, 'patients', 'patientdocument');
INSERT INTO `django_content_type` VALUES (42, 'patients', 'patienthealthrecord');
INSERT INTO `django_content_type` VALUES (23, 'payments', 'bill');
INSERT INTO `django_content_type` VALUES (24, 'payments', 'billitem');
INSERT INTO `django_content_type` VALUES (25, 'payments', 'payment');
INSERT INTO `django_content_type` VALUES (39, 'rooms', 'room');
INSERT INTO `django_content_type` VALUES (26, 'services', 'customservicerequest');
INSERT INTO `django_content_type` VALUES (27, 'services', 'service');
INSERT INTO `django_content_type` VALUES (28, 'services', 'serviceexecution');
INSERT INTO `django_content_type` VALUES (46, 'services', 'servicefeedback');
INSERT INTO `django_content_type` VALUES (50, 'services', 'servicefeedbackimage');
INSERT INTO `django_content_type` VALUES (47, 'services', 'serviceorder');
INSERT INTO `django_content_type` VALUES (49, 'services', 'serviceorderitem');
INSERT INTO `django_content_type` VALUES (48, 'services', 'servicereview');
INSERT INTO `django_content_type` VALUES (5, 'sessions', 'session');
INSERT INTO `django_content_type` VALUES (17, 'tasks', 'task');
INSERT INTO `django_content_type` VALUES (18, 'tasks', 'taskassignment');
INSERT INTO `django_content_type` VALUES (19, 'tasks', 'taskcompletion');
INSERT INTO `django_content_type` VALUES (8, 'users', 'familyuser');
INSERT INTO `django_content_type` VALUES (41, 'users', 'leaverequest');
INSERT INTO `django_content_type` VALUES (45, 'users', 'registerapplication');
INSERT INTO `django_content_type` VALUES (7, 'users', 'staffuser');
INSERT INTO `django_content_type` VALUES (6, 'users', 'user');

-- ----------------------------
-- Table structure for django_migrations
-- ----------------------------
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 82 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_migrations
-- ----------------------------
INSERT INTO `django_migrations` VALUES (1, 'patients', '0001_initial', '2025-12-06 07:37:48.102694');
INSERT INTO `django_migrations` VALUES (2, 'contenttypes', '0001_initial', '2025-12-06 07:37:48.168722');
INSERT INTO `django_migrations` VALUES (3, 'contenttypes', '0002_remove_content_type_name', '2025-12-06 07:37:48.237104');
INSERT INTO `django_migrations` VALUES (4, 'auth', '0001_initial', '2025-12-06 07:37:48.533418');
INSERT INTO `django_migrations` VALUES (5, 'auth', '0002_alter_permission_name_max_length', '2025-12-06 07:37:48.623663');
INSERT INTO `django_migrations` VALUES (6, 'auth', '0003_alter_user_email_max_length', '2025-12-06 07:37:48.623663');
INSERT INTO `django_migrations` VALUES (7, 'auth', '0004_alter_user_username_opts', '2025-12-06 07:37:48.640611');
INSERT INTO `django_migrations` VALUES (8, 'auth', '0005_alter_user_last_login_null', '2025-12-06 07:37:48.648816');
INSERT INTO `django_migrations` VALUES (9, 'auth', '0006_require_contenttypes_0002', '2025-12-06 07:37:48.654205');
INSERT INTO `django_migrations` VALUES (10, 'auth', '0007_alter_validators_add_error_messages', '2025-12-06 07:37:48.664523');
INSERT INTO `django_migrations` VALUES (11, 'auth', '0008_alter_user_username_max_length', '2025-12-06 07:37:48.673081');
INSERT INTO `django_migrations` VALUES (12, 'auth', '0009_alter_user_last_name_max_length', '2025-12-06 07:37:48.679348');
INSERT INTO `django_migrations` VALUES (13, 'auth', '0010_alter_group_name_max_length', '2025-12-06 07:37:48.696806');
INSERT INTO `django_migrations` VALUES (14, 'auth', '0011_update_proxy_permissions', '2025-12-06 07:37:48.707990');
INSERT INTO `django_migrations` VALUES (15, 'auth', '0012_alter_user_first_name_max_length', '2025-12-06 07:37:48.714535');
INSERT INTO `django_migrations` VALUES (16, 'users', '0001_initial', '2025-12-06 07:37:49.302664');
INSERT INTO `django_migrations` VALUES (20, 'admin', '0001_initial', '2025-12-06 07:37:50.185486');
INSERT INTO `django_migrations` VALUES (21, 'admin', '0002_logentry_remove_auto_add', '2025-12-06 07:37:50.207522');
INSERT INTO `django_migrations` VALUES (22, 'admin', '0003_logentry_add_action_flag_choices', '2025-12-06 07:37:50.222316');
INSERT INTO `django_migrations` VALUES (23, 'appointments', '0001_initial', '2025-12-06 07:37:50.272214');
INSERT INTO `django_migrations` VALUES (24, 'appointments', '0002_initial', '2025-12-06 07:37:50.663304');
INSERT INTO `django_migrations` VALUES (25, 'bed_scheduling', '0001_initial', '2025-12-06 07:37:50.817130');
INSERT INTO `django_migrations` VALUES (26, 'bed_scheduling', '0002_initial', '2025-12-06 07:37:51.387342');
INSERT INTO `django_migrations` VALUES (27, 'care_records', '0001_initial', '2025-12-06 07:37:51.496887');
INSERT INTO `django_migrations` VALUES (28, 'care_records', '0002_initial', '2025-12-06 07:37:51.751006');
INSERT INTO `django_migrations` VALUES (29, 'communication', '0001_initial', '2025-12-06 07:37:51.821400');
INSERT INTO `django_migrations` VALUES (30, 'communication', '0002_initial', '2025-12-06 07:37:52.514742');
INSERT INTO `django_migrations` VALUES (31, 'notifications', '0001_initial', '2025-12-06 07:37:52.581447');
INSERT INTO `django_migrations` VALUES (32, 'notifications', '0002_initial', '2025-12-06 07:37:52.957393');
INSERT INTO `django_migrations` VALUES (33, 'patients', '0002_initial', '2025-12-06 07:37:53.434666');
INSERT INTO `django_migrations` VALUES (34, 'payments', '0001_initial', '2025-12-06 07:37:53.606130');
INSERT INTO `django_migrations` VALUES (35, 'payments', '0002_initial', '2025-12-06 07:37:54.051014');
INSERT INTO `django_migrations` VALUES (36, 'services', '0001_initial', '2025-12-06 07:37:54.176012');
INSERT INTO `django_migrations` VALUES (37, 'services', '0002_initial', '2025-12-06 07:37:54.780102');
INSERT INTO `django_migrations` VALUES (38, 'sessions', '0001_initial', '2025-12-06 07:37:54.825536');
INSERT INTO `django_migrations` VALUES (39, 'tasks', '0001_initial', '2025-12-06 07:37:54.943881');
INSERT INTO `django_migrations` VALUES (40, 'tasks', '0002_initial', '2025-12-06 07:37:55.999216');
INSERT INTO `django_migrations` VALUES (41, 'patients', '0003_alter_patient_id_card', '2026-01-05 11:28:39.411242');
INSERT INTO `django_migrations` VALUES (42, 'users', '0002_alter_user_managers_remove_user_groups_and_more', '2026-01-05 11:28:39.612422');
INSERT INTO `django_migrations` VALUES (43, 'patients', '0004_patient_health_level', '2026-01-05 13:25:49.692801');
INSERT INTO `django_migrations` VALUES (44, 'rooms', '0001_initial', '2026-01-07 11:37:32.319463');
INSERT INTO `django_migrations` VALUES (45, 'patients', '0005_add_room_field', '2026-01-07 11:59:33.167586');
INSERT INTO `django_migrations` VALUES (46, 'rooms', '0002_alter_room_options_remove_room_bed1_id_and_more', '2026-01-09 08:08:53.063097');
INSERT INTO `django_migrations` VALUES (47, 'announcements', '0001_initial', '2026-01-09 08:09:54.914676');
INSERT INTO `django_migrations` VALUES (48, 'users', '0003_leaverequest', '2026-01-09 08:39:46.493282');
INSERT INTO `django_migrations` VALUES (49, 'users', '0004_user_gender', '2026-01-09 10:01:19.675185');
INSERT INTO `django_migrations` VALUES (50, 'announcements', '0002_announcementreadstatus', '2026-01-12 11:37:47.006762');
INSERT INTO `django_migrations` VALUES (51, 'rooms', '0003_alter_room_created_at_alter_room_updated_at', '2026-01-12 11:37:47.012949');
INSERT INTO `django_migrations` VALUES (52, 'bed_scheduling', '0003_alter_bed_patient', '2026-01-16 06:44:16.006973');
INSERT INTO `django_migrations` VALUES (53, 'patients', '0006_alter_healthassessment_options_and_more', '2026-01-16 06:44:17.774549');
INSERT INTO `django_migrations` VALUES (54, 'users', '0005_staffuser_id', '2026-01-16 07:06:11.645703');
INSERT INTO `django_migrations` VALUES (55, 'users', '0006_remove_staffuser_id_alter_user_id', '2026-01-16 07:06:24.006890');
INSERT INTO `django_migrations` VALUES (57, 'activity_gallery', '0001_initial', '2026-01-16 07:08:36.526741');
INSERT INTO `django_migrations` VALUES (58, 'activity_gallery', '0002_initial', '2026-01-16 07:09:00.237200');
INSERT INTO `django_migrations` VALUES (59, 'activity_gallery', '0003_initial', '2026-01-16 07:09:20.884530');
INSERT INTO `django_migrations` VALUES (60, 'activity_gallery', '0004_alter_activity_staff', '2026-01-16 07:09:31.214093');
INSERT INTO `django_migrations` VALUES (61, 'activity_gallery', '0005_auto_20260116_1510', '2026-01-16 07:12:26.026367');
INSERT INTO `django_migrations` VALUES (62, 'activity_gallery', '0006_alter_activity_staff', '2026-01-16 07:14:10.128120');
INSERT INTO `django_migrations` VALUES (63, 'activity_gallery', '0007_activitymedia_file_path', '2026-01-19 13:45:35.581095');
INSERT INTO `django_migrations` VALUES (64, 'activity_gallery', '0008_activitymedia_image_path', '2026-01-19 13:45:35.614108');
INSERT INTO `django_migrations` VALUES (65, 'announcements', '0003_alter_announcement_options_and_more', '2026-01-19 13:45:35.753211');
INSERT INTO `django_migrations` VALUES (66, 'patients', '0007_remove_patient_bed_remove_patient_room_and_more', '2026-01-20 10:40:40.789567');
INSERT INTO `django_migrations` VALUES (67, 'patients', '0008_rename_room_id_patient_room_and_more', '2026-01-20 13:52:19.615547');
INSERT INTO `django_migrations` VALUES (68, 'patients', '0009_patient_bed_id', '2026-01-20 14:03:21.346614');
INSERT INTO `django_migrations` VALUES (69, 'bed_scheduling', '0004_remove_bedassignment_assigned_by_and_more', '2026-01-21 13:32:00.742139');
INSERT INTO `django_migrations` VALUES (70, 'patients', '0010_patient_primary_nurse_alter_healthassessment_id_and_more', '2026-01-22 14:01:20.272565');
INSERT INTO `django_migrations` VALUES (71, 'users', '0007_familyuser_balance', '2026-01-26 10:55:12.348076');
INSERT INTO `django_migrations` VALUES (72, 'payments', '0003_alter_payment_payment_method', '2026-01-26 10:58:27.816548');
INSERT INTO `django_migrations` VALUES (73, 'users', '0008_alter_user_id_registerapplication', '2026-01-27 06:59:52.476127');
INSERT INTO `django_migrations` VALUES (74, 'services', '0003_servicefeedback_serviceorder_and_more', '2026-01-29 07:30:25.307416');
INSERT INTO `django_migrations` VALUES (75, 'services', '0004_alter_customservicerequest_options_and_more', '2026-01-29 08:18:47.176394');
INSERT INTO `django_migrations` VALUES (76, 'users', '0009_alter_familyuser_options_alter_leaverequest_options_and_more', '2026-01-29 08:39:06.094749');
INSERT INTO `django_migrations` VALUES (77, 'users', '0010_alter_staffuser_department_alter_staffuser_position', '2026-01-30 06:13:43.933216');
INSERT INTO `django_migrations` VALUES (78, 'care_records', '0003_alter_carerecord_options_alter_caretemplate_options_and_more', '2026-01-30 16:21:48.537351');
INSERT INTO `django_migrations` VALUES (79, 'users', '0011_leaverequest_rejection_reason', '2026-01-30 20:28:31.092886');
INSERT INTO `django_migrations` VALUES (80, 'bed_scheduling', '0005_initial', '2026-02-05 13:15:25.009823');
INSERT INTO `django_migrations` VALUES (81, 'users', '0012_alter_user_email_alter_user_phone', '2026-02-06 13:26:23.594212');

-- ----------------------------
-- Table structure for django_session
-- ----------------------------
DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session`  (
  `session_key` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `session_data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`) USING BTREE,
  INDEX `django_session_expire_date_a5c62663`(`expire_date` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_session
-- ----------------------------

-- ----------------------------
-- Table structure for notifications_carereminder
-- ----------------------------
DROP TABLE IF EXISTS `notifications_carereminder`;
CREATE TABLE `notifications_carereminder`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `content` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `reminder_date` date NOT NULL,
  `is_participated` tinyint(1) NOT NULL,
  `participation_type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `patient_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `notifications_carereminder_patient_id_1976be6a_fk`(`patient_id` ASC) USING BTREE,
  CONSTRAINT `notifications_carereminder_patient_id_1976be6a_fk` FOREIGN KEY (`patient_id`) REFERENCES `patients_patient` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of notifications_carereminder
-- ----------------------------

-- ----------------------------
-- Table structure for notifications_notification
-- ----------------------------
DROP TABLE IF EXISTS `notifications_notification`;
CREATE TABLE `notifications_notification`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `content` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `related_id` int NULL DEFAULT NULL,
  `related_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `read_at` datetime(6) NULL DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `notifications_notification_user_id_b5e8c0ff_fk`(`user_id` ASC) USING BTREE,
  CONSTRAINT `notifications_notification_user_id_b5e8c0ff_fk` FOREIGN KEY (`user_id`) REFERENCES `users_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of notifications_notification
-- ----------------------------

-- ----------------------------
-- Table structure for notifications_reminderparticipation
-- ----------------------------
DROP TABLE IF EXISTS `notifications_reminderparticipation`;
CREATE TABLE `notifications_reminderparticipation`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `participation_type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `message` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `created_at` datetime(6) NOT NULL,
  `family_id` bigint NOT NULL,
  `reminder_id` bigint NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `notifications_remind_reminder_id_43e7a30d_fk_notificat`(`reminder_id` ASC) USING BTREE,
  INDEX `notifications_reminderparticipation_family_id_dd500393_fk`(`family_id` ASC) USING BTREE,
  CONSTRAINT `notifications_remind_reminder_id_43e7a30d_fk_notificat` FOREIGN KEY (`reminder_id`) REFERENCES `notifications_carereminder` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `notifications_reminderparticipation_family_id_dd500393_fk` FOREIGN KEY (`family_id`) REFERENCES `users_familyuser` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of notifications_reminderparticipation
-- ----------------------------

-- ----------------------------
-- Table structure for patients_healthassessment
-- ----------------------------
DROP TABLE IF EXISTS `patients_healthassessment`;
CREATE TABLE `patients_healthassessment`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `assessment_date` datetime(6) NOT NULL,
  `health_level` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `vital_signs` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `chronic_diseases` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `allergies` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `assessment_summary` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `created_by_id` bigint NULL DEFAULT NULL,
  `patient_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `patients_healthassessment_patient_id_b1bef1c0_fk`(`patient_id` ASC) USING BTREE,
  INDEX `patients_healthassessment_created_by_id_f2141781_fk`(`created_by_id` ASC) USING BTREE,
  CONSTRAINT `patients_healthassessment_created_by_id_f2141781_fk` FOREIGN KEY (`created_by_id`) REFERENCES `users_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `patients_healthassessment_patient_id_b1bef1c0_fk` FOREIGN KEY (`patient_id`) REFERENCES `patients_patient` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of patients_healthassessment
-- ----------------------------

-- ----------------------------
-- Table structure for patients_medicalrecord
-- ----------------------------
DROP TABLE IF EXISTS `patients_medicalrecord`;
CREATE TABLE `patients_medicalrecord`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `record_date` datetime(6) NOT NULL,
  `diagnosis` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `treatment` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `medications` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `doctor_id` bigint NULL DEFAULT NULL,
  `patient_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `patients_medicalrecord_patient_id_c059a22f_fk`(`patient_id` ASC) USING BTREE,
  INDEX `patients_medicalrecord_doctor_id_fab97954_fk`(`doctor_id` ASC) USING BTREE,
  CONSTRAINT `patients_medicalrecord_doctor_id_fab97954_fk` FOREIGN KEY (`doctor_id`) REFERENCES `users_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `patients_medicalrecord_patient_id_c059a22f_fk` FOREIGN KEY (`patient_id`) REFERENCES `patients_patient` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of patients_medicalrecord
-- ----------------------------

-- ----------------------------
-- Table structure for patients_patient
-- ----------------------------
DROP TABLE IF EXISTS `patients_patient`;
CREATE TABLE `patients_patient`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `gender` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `age` int NOT NULL,
  `id_card` varchar(18) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `phone` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `address` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `care_level` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `admission_date` date NULL DEFAULT NULL,
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `health_level` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `allergies` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `blood_type` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `emergency_contact` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `emergency_phone` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `medical_history` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `room` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `bed_id` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `primary_nurse_id` bigint NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `patients_patient_primary_nurse_id_624fe9eb`(`primary_nurse_id` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 20 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of patients_patient
-- ----------------------------
INSERT INTO `patients_patient` VALUES (1, '王五', 'male', 75, '110101194501011236', '13700137000', '北京市西城区', 'level3', '2023-03-01', 'active', '2025-12-11 04:13:22.298416', '2026-02-05 20:34:11.104095', 'good', NULL, NULL, NULL, NULL, NULL, '101', '1', NULL);
INSERT INTO `patients_patient` VALUES (2, '赵六', 'female', 68, '110101195201011237', '13600136000', '北京市东城区', 'level2', '2023-04-01', 'active', '2025-12-11 04:13:22.301415', '2025-12-11 04:13:22.301415', 'good', NULL, NULL, NULL, NULL, NULL, '102', '1', NULL);
INSERT INTO `patients_patient` VALUES (16, '单方事故', 'male', 15, '235165161655555555', '15806549116', '安徽', 'level1', '2026-01-05', 'active', '2026-01-05 12:47:55.345538', '2026-02-05 12:56:54.284359', 'good', NULL, NULL, NULL, NULL, NULL, '103', '1', NULL);
INSERT INTO `patients_patient` VALUES (17, '搞个群', 'male', 60, '156156464464444444', '15805684919', '安徽', 'level2', '2026-01-06', 'active', '2026-01-06 04:02:51.248523', '2026-01-06 04:02:51.248523', 'normal', NULL, NULL, NULL, NULL, NULL, '103', '2', NULL);
INSERT INTO `patients_patient` VALUES (18, '测试1', 'male', 80, '165165151195655555', '15805684919', '安徽112', 'level3', '2026-01-06', 'active', '2026-01-06 05:43:59.337400', '2026-01-07 11:21:41.029149', 'poor', NULL, NULL, NULL, NULL, NULL, '103', '3', NULL);
INSERT INTO `patients_patient` VALUES (19, 'TestElderly', 'male', 80, '110101194001010000', '13800138000', NULL, 'level1', '2026-01-07', 'active', '2026-01-07 12:28:43.730681', '2026-01-07 12:28:43.730681', 'good', NULL, NULL, NULL, NULL, NULL, '201', '4', NULL);

-- ----------------------------
-- Table structure for patients_patientdocument
-- ----------------------------
DROP TABLE IF EXISTS `patients_patientdocument`;
CREATE TABLE `patients_patientdocument`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `document_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `file_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `file_url` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `file_size` int NOT NULL,
  `uploaded_at` datetime(6) NOT NULL,
  `patient_id` int NOT NULL,
  `uploaded_by_id` bigint NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `patients_patientdocument_patient_id_992efd30_fk`(`patient_id` ASC) USING BTREE,
  INDEX `patients_patientdocument_uploaded_by_id_aab77fbc_fk`(`uploaded_by_id` ASC) USING BTREE,
  CONSTRAINT `patients_patientdocument_patient_id_992efd30_fk` FOREIGN KEY (`patient_id`) REFERENCES `patients_patient` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `patients_patientdocument_uploaded_by_id_aab77fbc_fk` FOREIGN KEY (`uploaded_by_id`) REFERENCES `users_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of patients_patientdocument
-- ----------------------------

-- ----------------------------
-- Table structure for patients_patienthealthrecord
-- ----------------------------
DROP TABLE IF EXISTS `patients_patienthealthrecord`;
CREATE TABLE `patients_patienthealthrecord`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `record_type` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `content` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `recorded_at` datetime(6) NOT NULL,
  `patient_id` int NOT NULL,
  `recorded_by_id` bigint NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `patients_patienthealthrecord_patient_id_0ac7e352_fk`(`patient_id` ASC) USING BTREE,
  INDEX `patients_patienthealthrecord_recorded_by_id_7b074264_fk`(`recorded_by_id` ASC) USING BTREE,
  CONSTRAINT `patients_patienthealthrecord_patient_id_0ac7e352_fk` FOREIGN KEY (`patient_id`) REFERENCES `patients_patient` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `patients_patienthealthrecord_recorded_by_id_7b074264_fk` FOREIGN KEY (`recorded_by_id`) REFERENCES `users_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of patients_patienthealthrecord
-- ----------------------------

-- ----------------------------
-- Table structure for payments_bill
-- ----------------------------
DROP TABLE IF EXISTS `payments_bill`;
CREATE TABLE `payments_bill`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `bill_type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `month` varchar(7) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `total_amount` decimal(10, 2) NOT NULL,
  `paid_amount` decimal(10, 2) NOT NULL,
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `due_date` date NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `family_id` bigint NULL DEFAULT NULL,
  `patient_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `payments_bill_patient_id_1eac5e23_fk`(`patient_id` ASC) USING BTREE,
  INDEX `payments_bill_family_id_a3d0ba9e_fk`(`family_id` ASC) USING BTREE,
  CONSTRAINT `payments_bill_family_id_a3d0ba9e_fk` FOREIGN KEY (`family_id`) REFERENCES `users_familyuser` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `payments_bill_patient_id_1eac5e23_fk` FOREIGN KEY (`patient_id`) REFERENCES `patients_patient` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of payments_bill
-- ----------------------------
INSERT INTO `payments_bill` VALUES (1, 'monthly', '2026-01', 5000.00, 5000.00, 'paid', '2026-01-28', '2026-01-30 21:28:53.923591', '2026-01-30 21:35:44.692134', 9, 16);

-- ----------------------------
-- Table structure for payments_billitem
-- ----------------------------
DROP TABLE IF EXISTS `payments_billitem`;
CREATE TABLE `payments_billitem`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `item_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `description` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `quantity` int NOT NULL,
  `unit_price` decimal(10, 2) NOT NULL,
  `amount` decimal(10, 2) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `bill_id` bigint NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `payments_billitem_bill_id_15fc4cf1_fk_payments_bill_id`(`bill_id` ASC) USING BTREE,
  CONSTRAINT `payments_billitem_bill_id_15fc4cf1_fk_payments_bill_id` FOREIGN KEY (`bill_id`) REFERENCES `payments_bill` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of payments_billitem
-- ----------------------------

-- ----------------------------
-- Table structure for payments_payment
-- ----------------------------
DROP TABLE IF EXISTS `payments_payment`;
CREATE TABLE `payments_payment`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `amount` decimal(10, 2) NOT NULL,
  `payment_method` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `transaction_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `paid_at` datetime(6) NULL DEFAULT NULL,
  `notes` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `bill_id` bigint NOT NULL,
  `family_id` bigint NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `transaction_id`(`transaction_id` ASC) USING BTREE,
  INDEX `payments_payment_bill_id_80d854b4_fk_payments_bill_id`(`bill_id` ASC) USING BTREE,
  INDEX `payments_payment_family_id_24d9dedc_fk`(`family_id` ASC) USING BTREE,
  CONSTRAINT `payments_payment_bill_id_80d854b4_fk_payments_bill_id` FOREIGN KEY (`bill_id`) REFERENCES `payments_bill` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `payments_payment_family_id_24d9dedc_fk` FOREIGN KEY (`family_id`) REFERENCES `users_familyuser` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of payments_payment
-- ----------------------------
INSERT INTO `payments_payment` VALUES (1, 5000.00, 'online', 'PAYB199D6B2CB38_1', 'pending', NULL, 'Bulk payment group PAYB199D6B2CB38', '2026-01-30 21:33:06.532923', '2026-01-30 21:33:06.532923', 1, 9);
INSERT INTO `payments_payment` VALUES (2, 5000.00, 'online', 'PAYC5AFC522B9CA_1', 'pending', NULL, 'Bulk payment group PAYC5AFC522B9CA', '2026-01-30 21:33:54.731966', '2026-01-30 21:33:54.731966', 1, 9);
INSERT INTO `payments_payment` VALUES (3, 5000.00, 'online', 'PAYC54D7AA7A4BD_1', 'success', '2026-01-30 21:35:44.690617', 'Bulk payment group PAYC54D7AA7A4BD', '2026-01-30 21:35:44.690617', '2026-01-30 21:35:44.690617', 1, 9);

-- ----------------------------
-- Table structure for rooms
-- ----------------------------
DROP TABLE IF EXISTS `rooms`;
CREATE TABLE `rooms`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `room_number` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `bed1` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `bed2` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `bed3` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `bed4` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `room_number`(`room_number` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 10 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of rooms
-- ----------------------------
INSERT INTO `rooms` VALUES (1, '101', '王五', 'TestElderly', '', '', '2026-01-07 11:39:39.890295', '2026-02-05 20:34:11.103066');
INSERT INTO `rooms` VALUES (2, '102', '', '2', '3', '4', '2026-01-07 11:39:39.894618', '2026-02-05 14:11:52.058212');
INSERT INTO `rooms` VALUES (3, '103', '单方事故', '搞个群', '测试1', '4', '2026-01-07 11:39:39.897810', '2026-01-07 11:39:39.897810');
INSERT INTO `rooms` VALUES (4, '104', '1', '2', '3', '4', '2026-01-07 11:39:39.900898', '2026-01-07 11:39:39.900898');
INSERT INTO `rooms` VALUES (5, '201', '1', '2', '3', 'TestElderly', '2026-01-07 11:39:39.905195', '2026-01-07 11:39:39.905195');
INSERT INTO `rooms` VALUES (6, '202', '1', '2', '3', '4', '2026-01-07 11:39:39.908262', '2026-01-07 11:39:39.908262');
INSERT INTO `rooms` VALUES (7, '203', '1', '2', '3', '4', '2026-01-07 11:39:39.912068', '2026-01-07 11:39:39.912068');
INSERT INTO `rooms` VALUES (8, '204', '1', '2', '3', '4', '2026-01-07 11:39:39.915468', '2026-01-07 11:39:39.915468');
INSERT INTO `rooms` VALUES (9, '301', '1', '2', '3', '', '2026-01-07 11:39:39.918561', '2026-01-07 11:39:39.918561');

-- ----------------------------
-- Table structure for services_customservicerequest
-- ----------------------------
DROP TABLE IF EXISTS `services_customservicerequest`;
CREATE TABLE `services_customservicerequest`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `service_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `description` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `expected_date` date NOT NULL,
  `amount` decimal(10, 2) NOT NULL,
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `approved_at` datetime(6) NULL DEFAULT NULL,
  `feedback` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `rating` int NULL DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `approved_by_id` bigint NULL DEFAULT NULL,
  `family_id` bigint NOT NULL,
  `patient_id` int NOT NULL,
  `service_id` bigint NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `services_customservi_service_id_f3b3e448_fk_services_`(`service_id` ASC) USING BTREE,
  INDEX `services_customservicerequest_patient_id_ff937981_fk`(`patient_id` ASC) USING BTREE,
  INDEX `services_customservicerequest_approved_by_id_74b75162_fk`(`approved_by_id` ASC) USING BTREE,
  INDEX `services_customservicerequest_family_id_795c4831_fk`(`family_id` ASC) USING BTREE,
  CONSTRAINT `services_customservi_service_id_f3b3e448_fk_services_` FOREIGN KEY (`service_id`) REFERENCES `services_service` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `services_customservicerequest_approved_by_id_74b75162_fk` FOREIGN KEY (`approved_by_id`) REFERENCES `users_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `services_customservicerequest_family_id_795c4831_fk` FOREIGN KEY (`family_id`) REFERENCES `users_familyuser` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `services_customservicerequest_patient_id_ff937981_fk` FOREIGN KEY (`patient_id`) REFERENCES `patients_patient` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of services_customservicerequest
-- ----------------------------

-- ----------------------------
-- Table structure for services_service
-- ----------------------------
DROP TABLE IF EXISTS `services_service`;
CREATE TABLE `services_service`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `service_type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `description` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `price` decimal(10, 2) NOT NULL,
  `duration` int NULL DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of services_service
-- ----------------------------
INSERT INTO `services_service` VALUES (1, '专业护理', 'medical', '提供专业的医疗护理服务', 100.00, NULL, 1, '2026-01-29 07:32:37.641847', '2026-01-29 07:32:37.641847');
INSERT INTO `services_service` VALUES (2, '康复训练', 'daily', '针对老年人的康复训练课程', 150.00, NULL, 1, '2026-01-29 07:32:37.644379', '2026-01-29 07:32:37.644379');
INSERT INTO `services_service` VALUES (3, '心理疏导', 'consultation', '专业的心理咨询与疏导', 200.00, NULL, 1, '2026-01-29 07:32:37.644909', '2026-01-29 07:32:37.644909');
INSERT INTO `services_service` VALUES (4, '按摩', 'custom', '身体按摩', 50.00, NULL, 1, '2026-01-30 14:52:01.473088', '2026-01-30 14:52:01.473088');

-- ----------------------------
-- Table structure for services_serviceexecution
-- ----------------------------
DROP TABLE IF EXISTS `services_serviceexecution`;
CREATE TABLE `services_serviceexecution`  (
  `custom_service_id` bigint NOT NULL,
  `execution_date` date NOT NULL,
  `start_time` time(6) NOT NULL,
  `end_time` time(6) NOT NULL,
  `notes` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `staff_id` bigint NOT NULL,
  PRIMARY KEY (`custom_service_id`) USING BTREE,
  INDEX `services_serviceexecution_staff_id_c7fa85cb_fk`(`staff_id` ASC) USING BTREE,
  CONSTRAINT `services_serviceexec_custom_service_id_71cb6322_fk_services_` FOREIGN KEY (`custom_service_id`) REFERENCES `services_customservicerequest` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `services_serviceexecution_staff_id_c7fa85cb_fk` FOREIGN KEY (`staff_id`) REFERENCES `users_staffuser` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of services_serviceexecution
-- ----------------------------

-- ----------------------------
-- Table structure for services_servicefeedback
-- ----------------------------
DROP TABLE IF EXISTS `services_servicefeedback`;
CREATE TABLE `services_servicefeedback`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `content` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `order_id` bigint NOT NULL,
  `staff_id` bigint NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `order_id`(`order_id` ASC) USING BTREE,
  INDEX `services_servicefeed_staff_id_23df7a43_fk_users_sta`(`staff_id` ASC) USING BTREE,
  CONSTRAINT `services_servicefeed_order_id_07f14883_fk_services_` FOREIGN KEY (`order_id`) REFERENCES `services_serviceorder` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `services_servicefeed_staff_id_23df7a43_fk_users_sta` FOREIGN KEY (`staff_id`) REFERENCES `users_staffuser` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of services_servicefeedback
-- ----------------------------
INSERT INTO `services_servicefeedback` VALUES (1, '已经完成', '2026-01-30 06:44:32.396761', 1, 2);

-- ----------------------------
-- Table structure for services_servicefeedbackimage
-- ----------------------------
DROP TABLE IF EXISTS `services_servicefeedbackimage`;
CREATE TABLE `services_servicefeedbackimage`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `image` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `feedback_id` bigint NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `services_servicefeed_feedback_id_07ae068b_fk_services_`(`feedback_id` ASC) USING BTREE,
  CONSTRAINT `services_servicefeed_feedback_id_07ae068b_fk_services_` FOREIGN KEY (`feedback_id`) REFERENCES `services_servicefeedback` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of services_servicefeedbackimage
-- ----------------------------
INSERT INTO `services_servicefeedbackimage` VALUES (1, 'feedback_images/屏幕截图_2025-12-29_194037.png', '2026-01-30 06:44:32.399846', 1);

-- ----------------------------
-- Table structure for services_serviceorder
-- ----------------------------
DROP TABLE IF EXISTS `services_serviceorder`;
CREATE TABLE `services_serviceorder`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `order_no` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `total_amount` decimal(10, 2) NOT NULL,
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `paid_at` datetime(6) NULL DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `family_id` bigint NOT NULL,
  `patient_id` int NOT NULL,
  `note` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `staff_id` bigint NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `order_no`(`order_no` ASC) USING BTREE,
  INDEX `services_serviceorde_family_id_3336702c_fk_users_fam`(`family_id` ASC) USING BTREE,
  INDEX `services_serviceorder_patient_id_55ec1fc7_fk_patients_patient_id`(`patient_id` ASC) USING BTREE,
  INDEX `services_serviceorde_staff_id_eb964328_fk_users_sta`(`staff_id` ASC) USING BTREE,
  CONSTRAINT `services_serviceorde_family_id_3336702c_fk_users_fam` FOREIGN KEY (`family_id`) REFERENCES `users_familyuser` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `services_serviceorde_staff_id_eb964328_fk_users_sta` FOREIGN KEY (`staff_id`) REFERENCES `users_staffuser` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `services_serviceorder_patient_id_55ec1fc7_fk_patients_patient_id` FOREIGN KEY (`patient_id`) REFERENCES `patients_patient` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of services_serviceorder
-- ----------------------------
INSERT INTO `services_serviceorder` VALUES (1, 'ORD32505BEC', 250.00, 'rated', '2026-01-29 08:23:27.477842', '2026-01-29 08:23:27.477842', '2026-01-30 06:45:11.300838', 9, 16, NULL, NULL);

-- ----------------------------
-- Table structure for services_serviceorderitem
-- ----------------------------
DROP TABLE IF EXISTS `services_serviceorderitem`;
CREATE TABLE `services_serviceorderitem`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `service_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `price` decimal(10, 2) NOT NULL,
  `order_id` bigint NOT NULL,
  `service_id` bigint NULL DEFAULT NULL,
  `quantity` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `services_serviceorde_order_id_a73ba646_fk_services_`(`order_id` ASC) USING BTREE,
  INDEX `services_serviceorde_service_id_7927301f_fk_services_`(`service_id` ASC) USING BTREE,
  CONSTRAINT `services_serviceorde_order_id_a73ba646_fk_services_` FOREIGN KEY (`order_id`) REFERENCES `services_serviceorder` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `services_serviceorde_service_id_7927301f_fk_services_` FOREIGN KEY (`service_id`) REFERENCES `services_service` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of services_serviceorderitem
-- ----------------------------
INSERT INTO `services_serviceorderitem` VALUES (1, '专业护理', 100.00, 1, 1, 1);
INSERT INTO `services_serviceorderitem` VALUES (2, '康复训练', 150.00, 1, 2, 1);

-- ----------------------------
-- Table structure for services_servicereview
-- ----------------------------
DROP TABLE IF EXISTS `services_servicereview`;
CREATE TABLE `services_servicereview`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `rating` int NOT NULL,
  `comment` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `created_at` datetime(6) NOT NULL,
  `order_id` bigint NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `order_id`(`order_id` ASC) USING BTREE,
  CONSTRAINT `services_servicerevi_order_id_4b4cb5b6_fk_services_` FOREIGN KEY (`order_id`) REFERENCES `services_serviceorder` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of services_servicereview
-- ----------------------------
INSERT INTO `services_servicereview` VALUES (1, 5, '666', '2026-01-30 06:45:11.297732', 1);

-- ----------------------------
-- Table structure for tasks_task
-- ----------------------------
DROP TABLE IF EXISTS `tasks_task`;
CREATE TABLE `tasks_task`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `description` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `due_date` date NOT NULL,
  `due_time` time(6) NULL DEFAULT NULL,
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `priority` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `completed_at` datetime(6) NULL DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `created_by_id` bigint NULL DEFAULT NULL,
  `patient_id` int NULL DEFAULT NULL,
  `staff_id` bigint NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `tasks_task_patient_id_d01e369b_fk`(`patient_id` ASC) USING BTREE,
  INDEX `tasks_task_staff_id_3256c024_fk`(`staff_id` ASC) USING BTREE,
  INDEX `tasks_task_created_by_id_1345568a_fk`(`created_by_id` ASC) USING BTREE,
  CONSTRAINT `tasks_task_created_by_id_1345568a_fk` FOREIGN KEY (`created_by_id`) REFERENCES `users_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `tasks_task_patient_id_d01e369b_fk` FOREIGN KEY (`patient_id`) REFERENCES `patients_patient` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `tasks_task_staff_id_3256c024_fk` FOREIGN KEY (`staff_id`) REFERENCES `users_staffuser` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tasks_task
-- ----------------------------
INSERT INTO `tasks_task` VALUES (1, 'bed_scheduling', '保洁：清理房间101床位3', '为院民 王五 分配床位后，请清理房间 101 的床位 3。', '2026-02-05', NULL, 'completed', 'high', '2026-02-05 13:46:21.214466', '2026-02-05 13:46:03.356147', '2026-02-05 13:46:21.214466', 2, 1, 10);
INSERT INTO `tasks_task` VALUES (2, 'bed_scheduling', '保洁：清理房间101床位1', '为院民 王五 分配床位后，请清理房间 101 的床位 1。', '2026-02-05', NULL, 'completed', 'high', '2026-02-05 15:42:01.784912', '2026-02-05 15:41:36.737601', '2026-02-05 15:42:01.784912', 10, 1, 10);
INSERT INTO `tasks_task` VALUES (3, 'bed_scheduling', '保洁：清理房间101床位1', '为院民 王五 分配床位后，请清理房间 101 的床位 1。', '2026-02-05', NULL, 'pending', 'high', NULL, '2026-02-05 20:34:11.108805', '2026-02-05 20:34:11.108805', 10, 1, 10);

-- ----------------------------
-- Table structure for tasks_taskassignment
-- ----------------------------
DROP TABLE IF EXISTS `tasks_taskassignment`;
CREATE TABLE `tasks_taskassignment`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `assigned_at` datetime(6) NOT NULL,
  `assigned_by_id` bigint NULL DEFAULT NULL,
  `staff_id` bigint NOT NULL,
  `task_id` bigint NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `tasks_taskassignment_task_id_6281ef9c_fk_tasks_task_id`(`task_id` ASC) USING BTREE,
  INDEX `tasks_taskassignment_staff_id_64aef0f7_fk`(`staff_id` ASC) USING BTREE,
  INDEX `tasks_taskassignment_assigned_by_id_62933098_fk`(`assigned_by_id` ASC) USING BTREE,
  CONSTRAINT `tasks_taskassignment_assigned_by_id_62933098_fk` FOREIGN KEY (`assigned_by_id`) REFERENCES `users_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `tasks_taskassignment_staff_id_64aef0f7_fk` FOREIGN KEY (`staff_id`) REFERENCES `users_staffuser` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `tasks_taskassignment_task_id_6281ef9c_fk_tasks_task_id` FOREIGN KEY (`task_id`) REFERENCES `tasks_task` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tasks_taskassignment
-- ----------------------------
INSERT INTO `tasks_taskassignment` VALUES (1, '2026-02-05 13:46:03.357431', 2, 10, 1);
INSERT INTO `tasks_taskassignment` VALUES (2, '2026-02-05 15:41:36.738606', 10, 10, 2);
INSERT INTO `tasks_taskassignment` VALUES (3, '2026-02-05 20:34:11.108805', 10, 10, 3);

-- ----------------------------
-- Table structure for tasks_taskcompletion
-- ----------------------------
DROP TABLE IF EXISTS `tasks_taskcompletion`;
CREATE TABLE `tasks_taskcompletion`  (
  `task_id` bigint NOT NULL,
  `completed_at` datetime(6) NOT NULL,
  `completion_notes` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `attached_files` json NULL,
  `completed_by_id` bigint NOT NULL,
  PRIMARY KEY (`task_id`) USING BTREE,
  INDEX `tasks_taskcompletion_completed_by_id_41fe32b7_fk`(`completed_by_id` ASC) USING BTREE,
  CONSTRAINT `tasks_taskcompletion_completed_by_id_41fe32b7_fk` FOREIGN KEY (`completed_by_id`) REFERENCES `users_staffuser` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `tasks_taskcompletion_task_id_4823011f_fk_tasks_task_id` FOREIGN KEY (`task_id`) REFERENCES `tasks_task` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tasks_taskcompletion
-- ----------------------------
INSERT INTO `tasks_taskcompletion` VALUES (1, '2026-02-05 13:46:21.217550', '', NULL, 10);
INSERT INTO `tasks_taskcompletion` VALUES (2, '2026-02-05 15:42:01.786498', '', NULL, 10);

-- ----------------------------
-- Table structure for users_familyuser
-- ----------------------------
DROP TABLE IF EXISTS `users_familyuser`;
CREATE TABLE `users_familyuser`  (
  `user_id` bigint NOT NULL,
  `relationship` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `proof_file` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `patient_id` int NOT NULL,
  `balance` decimal(10, 2) NOT NULL,
  PRIMARY KEY (`user_id`) USING BTREE,
  INDEX `users_familyuser_patient_id_c686b398_fk`(`patient_id` ASC) USING BTREE,
  CONSTRAINT `users_familyuser_patient_id_c686b398_fk` FOREIGN KEY (`patient_id`) REFERENCES `patients_patient` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `users_familyuser_user_id_29da564c_fk` FOREIGN KEY (`user_id`) REFERENCES `users_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of users_familyuser
-- ----------------------------
INSERT INTO `users_familyuser` VALUES (4, '家属', '', 'approved', '2026-01-12 11:37:45.994874', '2026-01-12 11:37:45.994874', 1, 0.00);
INSERT INTO `users_familyuser` VALUES (5, '家属', '', 'approved', '2026-01-12 11:37:45.999235', '2026-01-12 11:37:45.999235', 1, 0.00);
INSERT INTO `users_familyuser` VALUES (9, 'relative', '', 'pending', '2026-01-27 09:19:18.929378', '2026-01-27 09:19:18.929378', 16, 0.00);

-- ----------------------------
-- Table structure for users_leaverequest
-- ----------------------------
DROP TABLE IF EXISTS `users_leaverequest`;
CREATE TABLE `users_leaverequest`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `reason` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `approved_at` datetime(6) NULL DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `approved_by_id` bigint NULL DEFAULT NULL,
  `staff_id` bigint NOT NULL,
  `rejection_reason` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `users_leaverequest_approved_by_id_e85f704c_fk`(`approved_by_id` ASC) USING BTREE,
  INDEX `users_leaverequest_staff_id_b3e507ad_fk`(`staff_id` ASC) USING BTREE,
  CONSTRAINT `users_leaverequest_approved_by_id_e85f704c_fk` FOREIGN KEY (`approved_by_id`) REFERENCES `users_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `users_leaverequest_staff_id_b3e507ad_fk` FOREIGN KEY (`staff_id`) REFERENCES `users_staffuser` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of users_leaverequest
-- ----------------------------
INSERT INTO `users_leaverequest` VALUES (1, 'annual', '2026-01-30', '2026-02-11', '过年', 'approved', '2026-01-30 20:42:15.544578', '2026-01-30 20:41:44.548597', '2026-01-30 20:42:15.544578', 1, 2, NULL);

-- ----------------------------
-- Table structure for users_registerapplication
-- ----------------------------
DROP TABLE IF EXISTS `users_registerapplication`;
CREATE TABLE `users_registerapplication`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `username` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `password` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `real_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `phone` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `patient_id_card` varchar(18) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `relationship` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `approved_at` datetime(6) NULL DEFAULT NULL,
  `rejection_reason` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `approved_by_id` bigint NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username` ASC) USING BTREE,
  INDEX `users_registerapplic_approved_by_id_5ba0afac_fk_users_use`(`approved_by_id` ASC) USING BTREE,
  CONSTRAINT `users_registerapplic_approved_by_id_5ba0afac_fk_users_use` FOREIGN KEY (`approved_by_id`) REFERENCES `users_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of users_registerapplication
-- ----------------------------
INSERT INTO `users_registerapplication` VALUES (1, 'family', 'family123', 'p1', '1234512345', '235165161655555555', 'relative', 'approved', '2026-01-27 07:30:05.697095', '2026-01-27 09:19:18.932458', '2026-01-27 09:19:18.932458', NULL, 1);

-- ----------------------------
-- Table structure for users_staffuser
-- ----------------------------
DROP TABLE IF EXISTS `users_staffuser`;
CREATE TABLE `users_staffuser`  (
  `user_id` bigint NOT NULL,
  `position` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `department` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`user_id`) USING BTREE,
  CONSTRAINT `users_staffuser_user_id_05485441_fk` FOREIGN KEY (`user_id`) REFERENCES `users_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of users_staffuser
-- ----------------------------
INSERT INTO `users_staffuser` VALUES (2, 'Nurse', 'Nursing', '2026-01-30 06:26:03.277072', '2026-01-30 06:26:03.277072');
INSERT INTO `users_staffuser` VALUES (6, '3124', 'nursing', '2026-01-09 12:51:23.809002', '2026-01-10 04:49:51.268941');
INSERT INTO `users_staffuser` VALUES (7, '护理', 'nursing', '2026-01-10 02:16:29.084163', '2026-01-10 02:16:29.084163');
INSERT INTO `users_staffuser` VALUES (10, '保洁', '后勤', '2026-02-05 13:46:03.346971', '2026-02-05 21:36:51.066834');
INSERT INTO `users_staffuser` VALUES (13, '护士', 'nursing', '2026-02-06 13:32:41.506641', '2026-02-06 13:48:27.562381');

-- ----------------------------
-- Table structure for users_user
-- ----------------------------
DROP TABLE IF EXISTS `users_user`;
CREATE TABLE `users_user`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `last_login` datetime(6) NULL DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `first_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `last_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `username` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `password` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `role` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `real_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `email` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `avatar` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `relationship` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `patient_id` int NULL DEFAULT NULL,
  `position` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `department` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `gender` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username` ASC) USING BTREE,
  UNIQUE INDEX `phone`(`phone` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 14 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of users_user
-- ----------------------------
INSERT INTO `users_user` VALUES (1, NULL, 1, '', '', 1, 1, '2025-12-11 02:50:29.157447', 'admin', 'admin123', 'admin', 'active', '管理员', '13800138000', '1234562@qq.com', '', '2025-12-11 02:50:29.348646', '2026-02-05 12:53:21.698366', NULL, NULL, NULL, NULL, NULL);
INSERT INTO `users_user` VALUES (2, NULL, 0, '护士王五', '', 1, 1, '2025-12-20 02:03:45.171416', 'staff3', 'staff123', 'staff', 'active', '护士王五', '13800138008', '21355342@qq.com', '', '2025-12-20 02:03:45.171416', '2026-02-05 12:53:36.420985', NULL, NULL, '护士', '护理部', NULL);
INSERT INTO `users_user` VALUES (3, NULL, 0, '医生赵六', '', 1, 1, '2025-12-20 02:03:45.182302', 'staff4', 'staff123', 'staff', 'active', '医生赵六', '13800138009', NULL, '', '2025-12-20 02:03:45.182302', '2026-01-18 08:52:42.334862', NULL, NULL, '医生', '医疗部', NULL);
INSERT INTO `users_user` VALUES (4, NULL, 0, '家属张三', '', 0, 1, '2025-12-20 02:03:45.186892', 'family3', 'family123', 'family', 'active', '家属张三', '13800138010', NULL, '', '2025-12-20 02:03:45.186892', '2026-01-18 08:52:42.338015', NULL, NULL, NULL, NULL, NULL);
INSERT INTO `users_user` VALUES (5, NULL, 0, '家属李四', '', 0, 1, '2025-12-20 02:03:45.191445', 'family4', 'family123', 'family', 'active', '家属李四', '13800138011', NULL, '', '2025-12-20 02:03:45.191445', '2026-01-18 08:52:42.341064', NULL, NULL, NULL, NULL, NULL);
INSERT INTO `users_user` VALUES (6, NULL, 0, '1234', '', 0, 1, '2026-01-09 12:51:23.788485', '3214', '1324', 'staff', 'active', '1234', '1325645644', '1234@qq.com', '', '2026-01-09 12:51:23.788485', '2026-01-18 08:52:42.343965', NULL, NULL, NULL, NULL, 'male');
INSERT INTO `users_user` VALUES (7, NULL, 0, '员工1', '', 0, 1, '2026-01-10 02:16:29.076433', '11111', '11111', 'staff', 'active', '员工1', '1111', '2222@qq.com', '', '2026-01-10 02:16:29.076433', '2026-01-18 08:52:42.346787', NULL, NULL, NULL, NULL, 'male');
INSERT INTO `users_user` VALUES (9, NULL, 0, 'p1', '', 0, 1, '2026-01-27 09:19:18.926396', 'family', 'family123', 'family', 'active', 'p1', '1234512345', NULL, '', '2026-01-27 09:19:18.926396', '2026-01-27 09:19:18.926396', NULL, NULL, NULL, NULL, NULL);
INSERT INTO `users_user` VALUES (10, NULL, 0, '保洁员1', '', 0, 1, '2026-02-05 13:46:03.344136', 'cleaner1', 'password', 'staff', 'active', '保洁员1', '15900000001', '11111', '', '2026-02-05 13:46:03.344136', '2026-02-05 21:36:51.069974', NULL, NULL, '保洁', NULL, 'male');
INSERT INTO `users_user` VALUES (13, NULL, 0, '员工5', '', 0, 1, '2026-02-06 13:32:41.505636', 'staff5', '12345', 'staff', 'active', '员工5', '1354684684', '234562346', '', '2026-02-06 13:32:41.505636', '2026-02-06 13:48:27.565486', NULL, NULL, NULL, NULL, 'male');

SET FOREIGN_KEY_CHECKS = 1;
