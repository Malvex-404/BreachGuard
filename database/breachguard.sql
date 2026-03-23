CREATE DATABASE breachguard;

USE breachguard;

-- ==============================
-- USERS TABLE
-- ==============================

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==============================
-- MONITORED EMAILS
-- ==============================

CREATE TABLE monitored_emails (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    email VARCHAR(150) NOT NULL,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT unique_user_email UNIQUE (user_id, email),

    FOREIGN KEY (user_id)
    REFERENCES users(id)
    ON DELETE CASCADE
);

-- ==============================
-- SEARCH HISTORY
-- ==============================

CREATE TABLE searches (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NULL,
    query VARCHAR(150) NOT NULL,
    searched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
    REFERENCES users(id)
    ON DELETE SET NULL
);

-- ==============================
-- BREACH RESOLUTION STATUS
-- ==============================

CREATE TABLE monitored_breach_status (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    email VARCHAR(150) NOT NULL,
    breach_name VARCHAR(150) NOT NULL,

    resolved BOOLEAN DEFAULT FALSE,
    resolved_at TIMESTAMP NULL,

    CONSTRAINT unique_breach_resolution
    UNIQUE (user_id, email, breach_name),

    FOREIGN KEY (user_id)
    REFERENCES users(id)
    ON DELETE CASCADE
);

-- ==============================
-- BREACH NOTIFICATIONS
-- ==============================

CREATE TABLE breach_notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,

    email VARCHAR(150),
    breach_name VARCHAR(150),

    message TEXT,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT unique_notification
    UNIQUE (user_id, email, breach_name),

    FOREIGN KEY (user_id)
    REFERENCES users(id)
    ON DELETE CASCADE
);