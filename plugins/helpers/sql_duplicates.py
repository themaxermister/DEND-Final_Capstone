class SqlDuplicates:
	# SQL to remove duplicates in main database tables
	deletedup_sql = """
		WITH cte AS
			(SELECT ctid,
				   row_number() OVER (PARTITION BY {}
									  ORDER BY {}) rn
				   FROM {}
			)
			DELETE FROM {} temp
				   USING cte
				   WHERE cte.rn > 1
						 AND cte.ctid = temp.ctid;
	"""

	deletedup_location_table = deletedup_sql.format(
		"address, city, state, postal_code, latitude, longitude",
		"address, city, state, postal_code, latitude, longitude",
		"public.location_table",
		"public.location_table"
	)

	deletedup_opening_table = deletedup_sql.format(
		"opening_id, monday, tuesday, wednesday, thursday, friday, saturday, sunday",
		"opening_id, monday, tuesday, wednesday, thursday, friday, saturday, sunday",
		"public.opening_table",
		"public.opening_table"
	)

	deletedup_business_table = deletedup_sql.format(
		"business_id, name, address, stars, review_count, is_open, attributes, categories, opening_id, checkin_count",
		"business_id, name, address, stars, review_count, is_open, attributes, categories, opening_id, checkin_count",
		"public.business_table",
		"public.business_table"
	)

	deletedup_compliment_table = deletedup_sql.format(
		"compliment_id, hot, more, profile, cute, list, note, plain, cool, funny, writer, photos",
		"compliment_id, hot, more, profile, cute, list, note, plain, cool, funny, writer, photos",
		"public.compliment_table", 
		"public.compliment_table"
	)
	
	deletedup_user_table = deletedup_sql.format(
		"user_id, name, compliment_id, review_count, yelping_since, useful, funny, cool, elite, friends, fans, average_stars",
		"user_id, name, compliment_id, review_count, yelping_since, useful, funny, cool, elite, friends, fans, average_stars",
		"public.user_table",
		"public.user_table"
	)

	deletedup_review_table = deletedup_sql.format(
		"review_id, user_id, business_id, stars, useful, funny, cool, text, date",
		"review_id, user_id, business_id, stars, useful, funny, cool, text, date",
		"public.review_table",
		"public.review_table"
	)

	deletedup_tip_table = deletedup_sql.format(
		"tip_id, user_id, business_id, text, date, compliment_count",
		"tip_id, user_id, business_id, text, date, compliment_count",
		"public.tip_table",
		"public.tip_table"
	)
