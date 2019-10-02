class SqlInsert:
	location_table_insert = ("""
		SELECT DISTINCT address, city, state, postal_code, latitude, longitude
		FROM public.staging_business
		WHERE address IS NOT NULL
	""")
	
	opening_table_insert = ("""
		SELECT DISTINCT opening_id, monday, tuesday, wednesday, thursday, friday, saturday, sunday
		FROM public.staging_business
		WHERE opening_id IS NOT NULL
	""")
	
	business_table_insert = ("""
		SELECT DISTINCT b.business_id, b.name, b.address, b.stars, b.review_count, b.is_open, b.attributes,
			b.categories, b.opening_id, c.checkin_count
		FROM public.staging_business b
		INNER JOIN public.staging_checkin c ON b.business_id = c.business_id
		WHERE b.business_id IS NOT NULL
	""")
	
	compliment_table_insert = ("""
		SELECT DISTINCT compliment_id, compliment_hot, compliment_more, compliment_profile, compliment_cute,
			compliment_list, compliment_note, compliment_plain, compliment_cool, compliment_funny,
			compliment_writer, compliment_photos
		FROM public.staging_user
		WHERE compliment_id IS NOT NULL
	""")
	
	user_table_insert = ("""
		SELECT DISTINCT user_id, name, compliment_id, review_count, yelping_since, useful, funny, cool, elite,
			friends, fans, average_stars
		FROM public.staging_user
		WHERE user_id IS NOT NULL AND compliment_id IS NOT NULL
	""")

	review_table_insert = ("""
		SELECT review_id, user_id, business_id, stars, useful, funny, cool, text, date
		FROM public.staging_review
		WHERE review_id IS NOT NULL and user_id IS NOT NULL AND business_id IS NOT NULL
	""")

	tip_table_insert = ("""
		SELECT tip_id, user_id, business_id, text, date, compliment_count
		FROM public.staging_tip
		WHERE tip_id IS NOT NULL AND business_id IS NOT NULL
	""")