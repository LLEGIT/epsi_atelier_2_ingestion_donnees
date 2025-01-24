WITH cleaned_data AS (
    SELECT
        title,  -- Keep the issue title as is
        number, -- Keep the issue number
        url,    -- Retain the issue URL for reference
        LOWER(state) AS normalized_state,  -- Normalize state to lowercase for consistency
        createdAt::timestamp AS created_at,  -- Normalize column name and ensure correct data type
        updatedAt::timestamp AS updated_at,  -- Normalize column name and ensure correct data type
        LOWER(author.login) AS author_login,  -- Normalize author login to lowercase
    FROM issues  -- Reference the raw table
    WHERE state IN ('open', 'closed')  -- Filter to include only valid states
      AND title IS NOT NULL            -- Ensure title is not NULL
)

SELECT * FROM cleaned_data
