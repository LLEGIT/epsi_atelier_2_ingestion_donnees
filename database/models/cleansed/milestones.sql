WITH cleaned_data AS (
    SELECT
        title,  -- Keep the title as is
        description,  -- Keep the description as is
        dueOn::date AS due_date,  -- Normalize column name and ensure correct data type
        LOWER(state) AS normalized_state,  -- Normalize state to lowercase for consistency
        number,  -- Retain the milestone number
        createdAt::timestamp AS created_at,  -- Normalize column name and ensure correct data type
        updatedAt::timestamp AS updated_at  -- Normalize column name and ensure correct data type
    FROM milestones  -- Reference the raw table
    WHERE state IN ('open', 'closed')  -- Filter to include only valid states
      AND title IS NOT NULL            -- Exclude rows with NULL titles
)

SELECT * FROM cleaned_data
