WITH cleaned_data AS (
    SELECT
        title,  -- Keep the pull request title as is
        number, -- Keep the pull request number
        url,    -- Retain the pull request URL for reference
        LOWER(state) AS normalized_state,  -- Normalize state to lowercase for consistency
        createdAt::timestamp AS created_at,  -- Normalize column name and ensure correct data type
        updatedAt::timestamp AS updated_at,  -- Normalize column name and ensure correct data type
    FROM pull_requests  -- Reference the raw table
    WHERE state IN ('open', 'closed', 'merged')  -- Include only valid states
      AND title IS NOT NULL                      -- Exclude rows where title is NULL
)

SELECT * FROM cleaned_data
