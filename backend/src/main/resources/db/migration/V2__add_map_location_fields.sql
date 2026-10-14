ALTER TABLE layoffs
    ADD COLUMN location_status VARCHAR(30) NOT NULL DEFAULT 'UNKNOWN',
ADD COLUMN latitude DOUBLE PRECISION,
ADD COLUMN longitude DOUBLE PRECISION;

ALTER TABLE layoffs
    ADD CONSTRAINT chk_layoffs_location_status
        CHECK (
            location_status IN (
                                'CONFIRMED',
                                'OFFICE_REFERENCE',
                                'UNKNOWN'
                )
            );

ALTER TABLE layoffs
    ADD CONSTRAINT chk_layoffs_latitude
        CHECK (
            latitude IS NULL OR latitude BETWEEN -90 AND 90
            );

ALTER TABLE layoffs
    ADD CONSTRAINT chk_layoffs_longitude
        CHECK (
            longitude IS NULL OR longitude BETWEEN -180 AND 180
            );

ALTER TABLE layoffs
    ADD CONSTRAINT chk_layoffs_coordinates_pair
        CHECK (
            (latitude IS NULL AND longitude IS NULL)
                OR
            (latitude IS NOT NULL AND longitude IS NOT NULL)
            );
