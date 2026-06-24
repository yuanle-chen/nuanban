-- =============================================
-- 暖伴 · 智能陪伴机器人 测试数据
-- =============================================

USE nuanban_db;

-- =============================================
-- 插入测试用户
-- =============================================

-- 老人用户
INSERT INTO users (username, password, phone, role) VALUES
('elder_test', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4gPJm7CKKq1aOOEi', '13800138001', 'elder');

-- 子女用户
INSERT INTO users (username, password, phone, role) VALUES
('child_test', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4gPJm7CKKq1aOOEi', '13900139001', 'child');

-- =============================================
-- 插入老人档案
-- =============================================
INSERT INTO elder_profiles (user_id, real_name, age, gender, address, emergency_contact, emergency_phone) VALUES
(1, '王奶奶', 72, 'female', '北京市朝阳区某某小区1号楼101', '王小明', '13900139001');

-- =============================================
-- 插入家庭关系
-- =============================================
INSERT INTO family_relations (child_user_id, elder_user_id, relation_type) VALUES
(2, 1, '母子');

-- =============================================
-- 插入用药计划
-- =============================================
INSERT INTO medication_plans (elder_user_id, medication_name, dosage, frequency, reminder_times, is_active) VALUES
(1, '硝苯地平缓释片', '20mg', '每日1次', '["08:00"]', TRUE),
(1, '二甲双胍片', '0.5g', '每日3次', '["08:00", "12:00", "18:00"]', TRUE),
(1, '阿托伐他汀', '20mg', '每晚1次', '["21:00"]', TRUE);

-- =============================================
-- 插入健康记录
-- =============================================
INSERT INTO health_records (elder_user_id, record_type, value, recorded_at) VALUES
(1, 'blood_pressure', '128/82', NOW()),
(1, 'heart_rate', '72', NOW()),
(1, 'blood_sugar', '5.6', NOW()),
(1, 'weight', '62.5', NOW()),
(1, 'blood_pressure', '132/85', DATE_SUB(NOW(), INTERVAL 1 DAY)),
(1, 'heart_rate', '75', DATE_SUB(NOW(), INTERVAL 1 DAY));

-- =============================================
-- 插入用药记录
-- =============================================
INSERT INTO medication_logs (plan_id, elder_user_id, scheduled_time, taken_at, status) VALUES
(1, 1, '08:00', DATE_SUB(NOW(), INTERVAL 1 DAY), 'taken'),
(2, 1, '08:00', DATE_SUB(NOW(), INTERVAL 1 DAY), 'taken'),
(2, 1, '12:00', DATE_SUB(NOW(), INTERVAL 1 DAY), 'taken'),
(1, 1, '08:00', NOW(), 'taken'),
(2, 1, '08:00', NOW(), 'taken'),
(2, 1, '12:00', NOW(), 'pending');
