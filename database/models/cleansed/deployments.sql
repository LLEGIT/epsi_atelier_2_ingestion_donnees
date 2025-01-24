WITH cleaned_data AS (
    SELECT
        id,  -- Keep the ID as is
        createdAt::timestamp AS created_at,  -- Normalize column name and ensure correct data type
        LOWER(state) AS normalized_state,    -- Normalize state to lowercase for consistency
        CASE
            WHEN environment = 'prod' THEN 'production'   -- Standardize environment names
            WHEN environment = 'stg' THEN 'staging'
            ELSE environment
        END AS standardized_environment,
        description                          -- Keep the description as is
    FROM deployments  -- Reference the raw table
    WHERE state IN ('active', 'inactive')    -- Filter out unnecessary rows
)

SELECT * FROM cleaned_data
