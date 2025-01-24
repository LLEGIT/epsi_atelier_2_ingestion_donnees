WITH cleaned_data AS (
    SELECT
        name,  -- Keep the name as is
        createdAt::timestamp AS created_at,  -- Normalize column name and ensure correct data type
        LOWER(owner.login) AS owner_login  -- Normalize owner login to lowercase for consistency
    FROM forks  -- Reference the raw table
    WHERE name IS NOT NULL              -- Exclude rows where name is null
)

SELECT * FROM cleaned_data
