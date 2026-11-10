
CREATE TABLE ingestion_candidates (
                                      id BIGSERIAL PRIMARY KEY,

                                      company_name VARCHAR(255),
                                      employees_affected INTEGER,

                                      country VARCHAR(100),
                                      location VARCHAR(255),
                                      headquarters VARCHAR(255),

                                      layoff_date DATE,
                                      reason TEXT,

                                      article_title TEXT NOT NULL,
                                      source_url TEXT NOT NULL UNIQUE,
                                      source_name VARCHAR(255),
                                      article_published_at TIMESTAMP,

                                      company_evidence TEXT,
                                      employees_evidence TEXT,
                                      country_evidence TEXT,
                                      evidence_summary TEXT,

                                      extraction_data JSONB,

                                      review_status VARCHAR(30) NOT NULL DEFAULT 'PENDING_REVIEW',

                                      created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                                      updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

                                      CONSTRAINT chk_ingestion_candidates_employees
                                          CHECK (
                                              employees_affected IS NULL
                                                  OR employees_affected >= 0
                                              ),

                                      CONSTRAINT chk_ingestion_candidates_review_status
                                          CHECK (
                                              review_status IN (
                                                                'PENDING_REVIEW',
                                                                'NEEDS_REVIEW',
                                                                'APPROVED',
                                                                'REJECTED'
                                                  )
                                              )
);

CREATE INDEX idx_ingestion_candidates_review_status
    ON ingestion_candidates(review_status);

CREATE INDEX idx_ingestion_candidates_company_name
    ON ingestion_candidates(company_name);

CREATE INDEX idx_ingestion_candidates_layoff_date
    ON ingestion_candidates(layoff_date);
