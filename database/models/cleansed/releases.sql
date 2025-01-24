WITH cleaned_data AS (
    SELECT
        name,  -- Keep the release name as is
        tagName AS tag_name,  -- Rename tagName to tag_name for consistency
        createdAt::timestamp AS created_at,  -- Normalize column name and ensure correct data type
        description  -- Retain the description as is
    FROM releases  -- Reference the raw table
    WHERE name IS NOT NULL  -- Exclude rows where the name is NULL
      AND tagName IS NOT NULL  -- Exclude rows where the tag name is NULL
)

SELECT * FROM cleaned_data
