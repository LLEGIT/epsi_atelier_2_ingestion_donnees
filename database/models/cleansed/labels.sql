WITH cleaned_data AS (
    SELECT
        name,  -- Keep the label name as is
        LOWER(color) AS normalized_color,  -- Normalize color to lowercase for consistency
        description  -- Retain the description as is
    FROM labels  -- Reference the raw table
    WHERE name IS NOT NULL  -- Exclude rows where the name is NULL
)

SELECT * FROM cleaned_data
