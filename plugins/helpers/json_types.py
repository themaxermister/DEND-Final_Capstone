class JsonTypes:
    # Outlines data types for each column in JSON data files
    user_types = """data->>'user_id',
        data->>'name',
        CAST(data->>'review_count' AS int8),
        CAST(data->>'yelping_since' AS timestamp),
        CAST(data->>'useful' AS int8),
        CAST(data->>'funny' AS int8),
        CAST(data->>'cool' AS int8),
        CAST(data->>'elite' AS int8[]),
        CAST(data->>'friends' AS varchar(256)[]),
        CAST(data->>'fans' AS int8),
        CAST(data->>'average_stars' AS real),
        data->>'compliment_id',
        CAST(data->>'compliment_hot' AS int8),
        CAST(data->>'compliment_more' AS int8),
        CAST(data->>'compliment_profile' AS int8),
        CAST(data->>'compliment_cute' AS int8),
        CAST(data->>'compliment_list' AS int8),
        CAST(data->>'compliment_note' AS int8),
        CAST(data->>'compliment_plain' AS int8),
        CAST(data->>'compliment_cool' AS int8),
        CAST(data->>'compliment_funny' AS int8),
        CAST(data->>'compliment_writer' AS int8),
        CAST(data->>'compliment_photos' AS int8)
    """

    review_types = """data->>'review_id',
        data->>'user_id',
        data->>'business_id',
        CAST(data->>'stars' AS real),
        CAST(data->>'useful' AS int4),
        CAST(data->>'funny' AS int4),
        CAST(data->>'cool' AS int4),
        data->>'text',
        TO_TIMESTAMP(data->>'date', 'YYYY/MM/DD hh24:mi:ss')
    """