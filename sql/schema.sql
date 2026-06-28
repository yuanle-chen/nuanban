-- =============================================
-- 暖伴 · 智能陪伴机器人 数据库建表脚本
-- =============================================

-- 创建数据库
CREATE DATABASE IF NOT EXISTS nuanban_db DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE nuanban_db;

-- =============================================
-- 1. 用户表（老人和子女）
-- =============================================
CREATE TABLE IF NOT EXISTS users (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '用户ID',
    username VARCHAR(50) NOT NULL UNIQUE COMMENT '用户名',
    password VARCHAR(255) NOT NULL COMMENT '密码（加密存储）',
    phone VARCHAR(20) COMMENT '手机号',
    role ENUM('elder', 'child') NOT NULL COMMENT '角色：elder=老人，child=子女',
    avatar VARCHAR(255) DEFAULT NULL COMMENT '头像URL',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_username (username),
    INDEX idx_role (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';

-- =============================================
-- 2. 老人档案表
-- =============================================
CREATE TABLE IF NOT EXISTS elder_profiles (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '档案ID',
    user_id BIGINT NOT NULL UNIQUE COMMENT '用户ID',
    real_name VARCHAR(50) NOT NULL COMMENT '真实姓名',
    age INT COMMENT '年龄',
    gender ENUM('male', 'female') COMMENT '性别',
    address VARCHAR(255) COMMENT '住址',
    latitude DECIMAL(10, 8) DEFAULT NULL COMMENT '纬度',
    longitude DECIMAL(11, 8) DEFAULT NULL COMMENT '经度',
    emergency_contact VARCHAR(100) COMMENT '紧急联系人',
    emergency_phone VARCHAR(20) COMMENT '紧急联系电话',
    health_info JSON DEFAULT NULL COMMENT '健康信息（既往病史、过敏源等）',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='老人档案表';

-- =============================================
-- 3. 家庭关系表（子女-老人关联）
-- =============================================
CREATE TABLE IF NOT EXISTS family_relations (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '关系ID',
    child_user_id BIGINT NOT NULL COMMENT '子女用户ID',
    elder_user_id BIGINT NOT NULL COMMENT '老人用户ID',
    relation_type VARCHAR(20) DEFAULT '子女' COMMENT '关系类型：父子、母子等',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (child_user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (elder_user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY uk_child_elder (child_user_id, elder_user_id),
    INDEX idx_child (child_user_id),
    INDEX idx_elder (elder_user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='家庭关系表';

-- =============================================
-- 4. 健康记录表
-- =============================================
CREATE TABLE IF NOT EXISTS health_records (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '记录ID',
    elder_user_id BIGINT NOT NULL COMMENT '老人用户ID',
    record_type ENUM('blood_pressure', 'heart_rate', 'blood_sugar', 'weight', 'sleep') NOT NULL COMMENT '记录类型',
    value VARCHAR(50) NOT NULL COMMENT '测量值',
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '记录时间',
    FOREIGN KEY (elder_user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_elder_type (elder_user_id, record_type),
    INDEX idx_recorded_at (recorded_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='健康记录表';

-- =============================================
-- 5. 用药计划表
-- =============================================
CREATE TABLE IF NOT EXISTS medication_plans (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '计划ID',
    elder_user_id BIGINT NOT NULL COMMENT '老人用户ID',
    medication_name VARCHAR(100) NOT NULL COMMENT '药物名称',
    dosage VARCHAR(50) NOT NULL COMMENT '剂量',
    frequency VARCHAR(50) NOT NULL COMMENT '服用频率',
    reminder_times JSON NOT NULL COMMENT '提醒时间列表 ["08:00", "12:00", "21:00"]',
    is_active BOOLEAN DEFAULT TRUE COMMENT '是否启用',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (elder_user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_elder_active (elder_user_id, is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用药计划表';

-- =============================================
-- 6. 用药记录表
-- =============================================
CREATE TABLE IF NOT EXISTS medication_logs (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '记录ID',
    plan_id BIGINT NOT NULL COMMENT '计划ID',
    elder_user_id BIGINT NOT NULL COMMENT '老人用户ID',
    scheduled_time VARCHAR(10) NOT NULL COMMENT '计划时间 HH:MM',
    taken_at TIMESTAMP NULL COMMENT '实际服用时间',
    status ENUM('pending', 'taken', 'missed') DEFAULT 'pending' COMMENT '状态',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (plan_id) REFERENCES medication_plans(id) ON DELETE CASCADE,
    FOREIGN KEY (elder_user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_elder_status (elder_user_id, status),
    INDEX idx_plan_date (plan_id, scheduled_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用药记录表';

-- =============================================
-- 7. 紧急求助记录表
-- =============================================
CREATE TABLE IF NOT EXISTS emergency_records (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '记录ID',
    elder_user_id BIGINT NOT NULL COMMENT '老人用户ID',
    alert_type ENUM('sos', 'fall', 'abnormal', 'voice') NOT NULL COMMENT '报警类型',
    location VARCHAR(255) DEFAULT NULL COMMENT '位置描述',
    latitude DECIMAL(10, 8) DEFAULT NULL COMMENT '纬度',
    longitude DECIMAL(11, 8) DEFAULT NULL COMMENT '经度',
    handled_status ENUM('pending', 'contacting', 'resolved', 'cancelled') DEFAULT 'pending' COMMENT '处理状态',
    handled_at TIMESTAMP NULL COMMENT '处理时间',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '触发时间',
    FOREIGN KEY (elder_user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_elder_status (elder_user_id, handled_status),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='紧急求助记录表';

-- =============================================
-- 8. AI对话记录表
-- =============================================
CREATE TABLE IF NOT EXISTS chat_logs (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '记录ID',
    elder_user_id BIGINT NOT NULL COMMENT '老人用户ID',
    message TEXT NOT NULL COMMENT '用户消息',
    response TEXT NOT NULL COMMENT 'AI回复',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (elder_user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_elder_time (elder_user_id, created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='AI对话记录表';

-- =============================================
-- 9. 通知记录表
-- =============================================
CREATE TABLE IF NOT EXISTS notification_logs (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '通知ID',
    user_id BIGINT NOT NULL COMMENT '接收用户ID',
    title VARCHAR(100) NOT NULL COMMENT '通知标题',
    content TEXT NOT NULL COMMENT '通知内容',
    type ENUM('medication', 'emergency', 'health', 'system') NOT NULL COMMENT '通知类型',
    is_read BOOLEAN DEFAULT FALSE COMMENT '是否已读',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_read (user_id, is_read),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='通知记录表';

-- =============================================
-- 10. 验证码表
-- =============================================
CREATE TABLE IF NOT EXISTS verification_codes (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '记录ID',
    phone VARCHAR(20) NOT NULL COMMENT '手机号',
    code VARCHAR(10) NOT NULL COMMENT '验证码',
    purpose VARCHAR(20) DEFAULT 'reset_password' COMMENT '用途：reset_password=找回密码',
    is_used BOOLEAN DEFAULT FALSE COMMENT '是否已使用',
    expires_at TIMESTAMP NOT NULL COMMENT '过期时间',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_phone (phone),
    INDEX idx_code (code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='验证码表';

-- =============================================
-- 11. 视频通话记录表
-- =============================================
CREATE TABLE IF NOT EXISTS video_calls (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '记录ID',
    caller_id BIGINT NOT NULL COMMENT '发起人ID',
    receiver_id BIGINT NOT NULL COMMENT '接收人ID',
    status VARCHAR(20) DEFAULT 'calling' COMMENT '状态：calling=呼叫中, connected=已接通, ended=已结束, missed=未接通',
    duration INT DEFAULT 0 COMMENT '通话时长（秒）',
    room_id VARCHAR(50) COMMENT '房间号',
    started_at TIMESTAMP NULL COMMENT '开始时间',
    ended_at TIMESTAMP NULL COMMENT '结束时间',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    FOREIGN KEY (caller_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (receiver_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_caller (caller_id),
    INDEX idx_receiver (receiver_id),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='视频通话记录表';
