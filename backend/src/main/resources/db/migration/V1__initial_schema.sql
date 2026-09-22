CREATE TABLE layoffs (
                         id BIGSERIAL PRIMARY KEY,

                         company_name VARCHAR(255) NOT NULL,

                         employees_affected INTEGER,

                         sources TEXT[],

                         country VARCHAR(100) NOT NULL,

                         location VARCHAR(255),

                         headquarters VARCHAR(255),

                         layoff_date DATE,

                         reason TEXT,

                         verification_status VARCHAR(50) NOT NULL DEFAULT 'UNVERIFIED',

                         created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

                         updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);