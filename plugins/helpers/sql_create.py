class SqlCreate:
	## DROP TABLES
	DROP_TABLE = """
		DROP TABLE IF EXISTS {};
	"""

	# ## DROP STAGING TABLES
	DROP_STAGING_TIP_TABLE = DROP_TABLE.format(
		"public.staging_tip"
	)

	DROP_STAGING_REVIEW_TABLE = DROP_TABLE.format(
		"public.staging_review"
	)

	DROP_STAGING_USER_TABLE = DROP_TABLE.format(
		"public.staging_user"
	)

	DROP_STAGING_BUSINESS_TABLE = DROP_TABLE.format(
		"public.staging_business"
	)

	DROP_STAGING_CHECKIN_TABLE = DROP_TABLE.format(
		"public.staging_checkin"
	)
	
	# ## DROP FACT TABLES
	DROP_TIP_FACT_TABLE = DROP_TABLE.format(
		"public.tip_table"
	)

	DROP_REVIEW_FACT_TABLE = DROP_TABLE.format(
		"public.review_table"
	)

	# ## DROP DIM TABLES
	DROP_USER_DIM_TABLE = DROP_TABLE.format(
		"public.user_table"
	)
	
	DROP_COMPLIMENT_DIM_TABLE = DROP_TABLE.format(
		"public.compliment_table"
	)

	DROP_BUSINESS_DIM_TABLE = DROP_TABLE.format(
		"public.business_table"
	)

	DROP_LOCATION_DIM_TABLE = DROP_TABLE.format(
		"public.location_table"
	)

	DROP_OPENING_DIM_TABLE = DROP_TABLE.format(
		"public.opening_table"
	)

	## CREATE TABLES
	# ## CREATE STAGING TABLES
	CREATE_STAGING_BUSINESS_TABLE = """CREATE TABLE IF NOT EXISTS public.staging_business (
		business_id      	varchar(256),
		name             	varchar(256),
		address          	text,
		city             	varchar(256),
		state            	varchar(256),
		postal_code      	varchar(256),
		latitude      	 	double precision,
		longitude			double precision,
		stars           	real,
		review_count      	int8,
		is_open           	bool,
		attributes       	text,
		categories       	varchar(256)[],
		hours				text,
		opening_id			varchar(256),
		monday            	varchar(256),
		tuesday            	varchar(256),
		wednesday          	varchar(256),
		thursday           	varchar(256),	
		friday            	varchar(256),
		saturday           	varchar(256),
		sunday            	varchar(256)
	);"""

	CREATE_STAGING_CHECKIN_TABLE = """CREATE TABLE IF NOT EXISTS public.staging_checkin (
		business_id 		varchar(256),
		date				varchar(256)[],
		checkin_count     	int8
	);"""

	CREATE_STAGING_REVIEW_TABLE = """CREATE TABLE IF NOT EXISTS public.staging_review (
		review_id           varchar(256),
		user_id             varchar(256),
		business_id			varchar(256),
		stars               real,
		useful              int4,
		funny               int4,
		cool  				int4,
		text                text,
		date           		timestamp
	);"""

	CREATE_STAGING_TIP_TABLE = """CREATE TABLE IF NOT EXISTS public.staging_tip (
		tip_id              	varchar(256),
		user_id             	varchar(256),
		business_id         	varchar(256),
		text                	text,
		date                	timestamp,
		compliment_count     	int4
	);"""

	CREATE_STAGING_USER_TABLE = """CREATE TABLE IF NOT EXISTS public.staging_user (
		user_id                	varchar(256),
		name                   	varchar(256),
		review_count            int8,
		yelping_since          	timestamp,
		useful                  int8,	
		funny                   int8,
		cool                    int8,
		elite                   int8[],
		friends                 varchar(256)[],
		fans                    int8,
		average_stars         	real,
		compliment_id			varchar(256),
		compliment_hot          int8,
		compliment_more         int8,
		compliment_profile      int8,
		compliment_cute         int8,
		compliment_list         int8,
		compliment_note         int8,
		compliment_plain        int8,
		compliment_cool         int8,
		compliment_funny        int8,
		compliment_writer       int8,
		compliment_photos       int8
	);"""

	# ##  CREATE DIM TABLES
	CREATE_LOCATION_DIM_TABLE = """CREATE TABLE IF NOT EXISTS public.location_table (
		address			text			NOT NULL,	
		city			varchar(256),
		state			varchar(256),
		postal_code		varchar(256),
		latitude		double precision,
		longitude		double precision
	);"""

	CREATE_BUSINESS_DIM_TABLE = """CREATE TABLE IF NOT EXISTS public.business_table (
		business_id			varchar(256)	NOT NULL,
		name				varchar(256),
		address				text,
		stars				real,
		review_count		int8,
		is_open				bool,
		attributes			text,
		categories			varchar(256)[],
		opening_id			varchar(256),
		checkin_count		int8
	);"""

	CREATE_COMPLIMENT_DIM_TABLE = """CREATE TABLE IF NOT EXISTS public.compliment_table (
		compliment_id			varchar(256)	NOT NULL,
		hot						int8,
		more					int8,
		profile					int8,
		cute					int8,
		list					int8,
		note					int8,
		plain					int8,
		cool					int8,
		funny					int8,
		writer					int8,
		photos					int8
	);"""

	CREATE_USER_DIM_TABLE = """CREATE TABLE IF NOT EXISTS public.user_table (
		user_id			varchar(256)	NOT NULL,
		name			varchar(256),
		compliment_id	varchar(256)	NOT NULL,
		review_count	int8,
		yelping_since	timestamp,
		useful			int8,
		funny			int8,
		cool			int8,
		elite			int8[],
		friends			varchar(256)[],
		fans			int8,
		average_stars	real
	);"""

	CREATE_OPENING_DIM_TABLE = """CREATE TABLE IF NOT EXISTS public.opening_table (
		opening_id		varchar(256)	NOT NULL,
		monday			varchar(256),
		tuesday			varchar(256),
		wednesday		varchar(256),
		thursday		varchar(256),
		friday			varchar(256),
		saturday		varchar(256),
		sunday			varchar(256)
	);"""

	# ## CREATE FACT TABLES
	CREATE_REVIEW_FACT_TABLE = """CREATE TABLE IF NOT EXISTS public.review_table (
		review_id		varchar(256)	NOT NULL,
		user_id			varchar(256)	NOT NULL,
		business_id		varchar(256)	NOT NULL,
		stars			real,
		useful			int4,
		funny			int4,
		cool			int4,
		text			text,
		date			timestamp
	);"""

	CREATE_TIP_FACT_TABLE = """CREATE TABLE IF NOT EXISTS public.tip_table (
		tip_id				varchar(256)	NOT NULL,
		user_id				varchar(256)	NOT NULL,
		business_id			varchar(256)	NOT NULL,
		text				text,
		date				timestamp,
		compliment_count	int4
	);"""