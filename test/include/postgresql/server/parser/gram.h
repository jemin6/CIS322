/* A Bison parser, made by GNU Bison 3.0.4.  */

/* Bison interface for Yacc-like parsers in C

   Copyright (C) 1984, 1989-1990, 2000-2015 Free Software Foundation, Inc.

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.  */

/* As a special exception, you may create a larger work that contains
   part or all of the Bison parser skeleton and distribute that work
   under terms of your choice, so long as that work isn't itself a
   parser generator using the skeleton or a modified version thereof
   as a parser skeleton.  Alternatively, if you modify or redistribute
   the parser skeleton itself, you may (at your option) remove this
   special exception, which will cause the skeleton and the resulting
   Bison output files to be licensed under the GNU General Public
   License without this special exception.

   This special exception was added by the Free Software Foundation in
   version 2.2 of Bison.  */

#ifndef YY_BASE_YY_GRAM_H_INCLUDED
# define YY_BASE_YY_GRAM_H_INCLUDED
/* Debug traces.  */
#ifndef YYDEBUG
# define YYDEBUG 0
#endif
#if YYDEBUG
extern int base_yydebug;
#endif

/* Token type.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
  enum yytokentype
  {
    IDENT = 258,
    FCONST = 259,
    SCONST = 260,
    BCONST = 261,
    XCONST = 262,
    Op = 263,
    ICONST = 264,
    PARAM = 265,
    TYPECAST = 266,
    DOT_DOT = 267,
    COLON_EQUALS = 268,
    EQUALS_GREATER = 269,
    LESS_EQUALS = 270,
    GREATER_EQUALS = 271,
    NOT_EQUALS = 272,
    ABORT_P = 273,
    ABSOLUTE_P = 274,
    ACCESS = 275,
    ACTION = 276,
    ADD_P = 277,
    ADMIN = 278,
    AFTER = 279,
    AGGREGATE = 280,
    ALL = 281,
    ALSO = 282,
    ALTER = 283,
    ALWAYS = 284,
    ANALYSE = 285,
    ANALYZE = 286,
    AND = 287,
    ANY = 288,
    ARRAY = 289,
    AS = 290,
    ASC = 291,
    ASSERTION = 292,
    ASSIGNMENT = 293,
    ASYMMETRIC = 294,
    AT = 295,
    ATTACH = 296,
    ATTRIBUTE = 297,
    AUTHORIZATION = 298,
    BACKWARD = 299,
    BEFORE = 300,
    BEGIN_P = 301,
    BETWEEN = 302,
    BIGINT = 303,
    BINARY = 304,
    BIT = 305,
    BOOLEAN_P = 306,
    BOTH = 307,
    BY = 308,
    CACHE = 309,
    CALLED = 310,
    CASCADE = 311,
    CASCADED = 312,
    CASE = 313,
    CAST = 314,
    CATALOG_P = 315,
    CHAIN = 316,
    CHAR_P = 317,
    CHARACTER = 318,
    CHARACTERISTICS = 319,
    CHECK = 320,
    CHECKPOINT = 321,
    CLASS = 322,
    CLOSE = 323,
    CLUSTER = 324,
    COALESCE = 325,
    COLLATE = 326,
    COLLATION = 327,
    COLUMN = 328,
    COMMENT = 329,
    COMMENTS = 330,
    COMMIT = 331,
    COMMITTED = 332,
    CONCURRENTLY = 333,
    CONFIGURATION = 334,
    CONFLICT = 335,
    CONNECTION = 336,
    CONSTRAINT = 337,
    CONSTRAINTS = 338,
    CONTENT_P = 339,
    CONTINUE_P = 340,
    CONVERSION_P = 341,
    COPY = 342,
    COST = 343,
    CREATE = 344,
    CROSS = 345,
    CSV = 346,
    CUBE = 347,
    CURRENT_P = 348,
    CURRENT_CATALOG = 349,
    CURRENT_DATE = 350,
    CURRENT_ROLE = 351,
    CURRENT_SCHEMA = 352,
    CURRENT_TIME = 353,
    CURRENT_TIMESTAMP = 354,
    CURRENT_USER = 355,
    CURSOR = 356,
    CYCLE = 357,
    DATA_P = 358,
    DATABASE = 359,
    DAY_P = 360,
    DEALLOCATE = 361,
    DEC = 362,
    DECIMAL_P = 363,
    DECLARE = 364,
    DEFAULT = 365,
    DEFAULTS = 366,
    DEFERRABLE = 367,
    DEFERRED = 368,
    DEFINER = 369,
    DELETE_P = 370,
    DELIMITER = 371,
    DELIMITERS = 372,
    DEPENDS = 373,
    DESC = 374,
    DETACH = 375,
    DICTIONARY = 376,
    DISABLE_P = 377,
    DISCARD = 378,
    DISTINCT = 379,
    DO = 380,
    DOCUMENT_P = 381,
    DOMAIN_P = 382,
    DOUBLE_P = 383,
    DROP = 384,
    EACH = 385,
    ELSE = 386,
    ENABLE_P = 387,
    ENCODING = 388,
    ENCRYPTED = 389,
    END_P = 390,
    ENUM_P = 391,
    ESCAPE = 392,
    EVENT = 393,
    EXCEPT = 394,
    EXCLUDE = 395,
    EXCLUDING = 396,
    EXCLUSIVE = 397,
    EXECUTE = 398,
    EXISTS = 399,
    EXPLAIN = 400,
    EXTENSION = 401,
    EXTERNAL = 402,
    EXTRACT = 403,
    FALSE_P = 404,
    FAMILY = 405,
    FETCH = 406,
    FILTER = 407,
    FIRST_P = 408,
    FLOAT_P = 409,
    FOLLOWING = 410,
    FOR = 411,
    FORCE = 412,
    FOREIGN = 413,
    FORWARD = 414,
    FREEZE = 415,
    FROM = 416,
    FULL = 417,
    FUNCTION = 418,
    FUNCTIONS = 419,
    GLOBAL = 420,
    GRANT = 421,
    GRANTED = 422,
    GREATEST = 423,
    GROUP_P = 424,
    GROUPING = 425,
    HANDLER = 426,
    HAVING = 427,
    HEADER_P = 428,
    HOLD = 429,
    HOUR_P = 430,
    IDENTITY_P = 431,
    IF_P = 432,
    ILIKE = 433,
    IMMEDIATE = 434,
    IMMUTABLE = 435,
    IMPLICIT_P = 436,
    IMPORT_P = 437,
    IN_P = 438,
    INCLUDING = 439,
    INCREMENT = 440,
    INDEX = 441,
    INDEXES = 442,
    INHERIT = 443,
    INHERITS = 444,
    INITIALLY = 445,
    INLINE_P = 446,
    INNER_P = 447,
    INOUT = 448,
    INPUT_P = 449,
    INSENSITIVE = 450,
    INSERT = 451,
    INSTEAD = 452,
    INT_P = 453,
    INTEGER = 454,
    INTERSECT = 455,
    INTERVAL = 456,
    INTO = 457,
    INVOKER = 458,
    IS = 459,
    ISNULL = 460,
    ISOLATION = 461,
    JOIN = 462,
    KEY = 463,
    LABEL = 464,
    LANGUAGE = 465,
    LARGE_P = 466,
    LAST_P = 467,
    LATERAL_P = 468,
    LEADING = 469,
    LEAKPROOF = 470,
    LEAST = 471,
    LEFT = 472,
    LEVEL = 473,
    LIKE = 474,
    LIMIT = 475,
    LISTEN = 476,
    LOAD = 477,
    LOCAL = 478,
    LOCALTIME = 479,
    LOCALTIMESTAMP = 480,
    LOCATION = 481,
    LOCK_P = 482,
    LOCKED = 483,
    LOGGED = 484,
    MAPPING = 485,
    MATCH = 486,
    MATERIALIZED = 487,
    MAXVALUE = 488,
    METHOD = 489,
    MINUTE_P = 490,
    MINVALUE = 491,
    MODE = 492,
    MONTH_P = 493,
    MOVE = 494,
    NAME_P = 495,
    NAMES = 496,
    NATIONAL = 497,
    NATURAL = 498,
    NCHAR = 499,
    NEW = 500,
    NEXT = 501,
    NO = 502,
    NONE = 503,
    NOT = 504,
    NOTHING = 505,
    NOTIFY = 506,
    NOTNULL = 507,
    NOWAIT = 508,
    NULL_P = 509,
    NULLIF = 510,
    NULLS_P = 511,
    NUMERIC = 512,
    OBJECT_P = 513,
    OF = 514,
    OFF = 515,
    OFFSET = 516,
    OIDS = 517,
    OLD = 518,
    ON = 519,
    ONLY = 520,
    OPERATOR = 521,
    OPTION = 522,
    OPTIONS = 523,
    OR = 524,
    ORDER = 525,
    ORDINALITY = 526,
    OUT_P = 527,
    OUTER_P = 528,
    OVER = 529,
    OVERLAPS = 530,
    OVERLAY = 531,
    OWNED = 532,
    OWNER = 533,
    PARALLEL = 534,
    PARSER = 535,
    PARTIAL = 536,
    PARTITION = 537,
    PASSING = 538,
    PASSWORD = 539,
    PLACING = 540,
    PLANS = 541,
    POLICY = 542,
    POSITION = 543,
    PRECEDING = 544,
    PRECISION = 545,
    PRESERVE = 546,
    PREPARE = 547,
    PREPARED = 548,
    PRIMARY = 549,
    PRIOR = 550,
    PRIVILEGES = 551,
    PROCEDURAL = 552,
    PROCEDURE = 553,
    PROGRAM = 554,
    QUOTE = 555,
    RANGE = 556,
    READ = 557,
    REAL = 558,
    REASSIGN = 559,
    RECHECK = 560,
    RECURSIVE = 561,
    REF = 562,
    REFERENCES = 563,
    REFERENCING = 564,
    REFRESH = 565,
    REINDEX = 566,
    RELATIVE_P = 567,
    RELEASE = 568,
    RENAME = 569,
    REPEATABLE = 570,
    REPLACE = 571,
    REPLICA = 572,
    RESET = 573,
    RESTART = 574,
    RESTRICT = 575,
    RETURNING = 576,
    RETURNS = 577,
    REVOKE = 578,
    RIGHT = 579,
    ROLE = 580,
    ROLLBACK = 581,
    ROLLUP = 582,
    ROW = 583,
    ROWS = 584,
    RULE = 585,
    SAVEPOINT = 586,
    SCHEMA = 587,
    SCROLL = 588,
    SEARCH = 589,
    SECOND_P = 590,
    SECURITY = 591,
    SELECT = 592,
    SEQUENCE = 593,
    SEQUENCES = 594,
    SERIALIZABLE = 595,
    SERVER = 596,
    SESSION = 597,
    SESSION_USER = 598,
    SET = 599,
    SETS = 600,
    SETOF = 601,
    SHARE = 602,
    SHOW = 603,
    SIMILAR = 604,
    SIMPLE = 605,
    SKIP = 606,
    SMALLINT = 607,
    SNAPSHOT = 608,
    SOME = 609,
    SQL_P = 610,
    STABLE = 611,
    STANDALONE_P = 612,
    START = 613,
    STATEMENT = 614,
    STATISTICS = 615,
    STDIN = 616,
    STDOUT = 617,
    STORAGE = 618,
    STRICT_P = 619,
    STRIP_P = 620,
    SUBSTRING = 621,
    SYMMETRIC = 622,
    SYSID = 623,
    SYSTEM_P = 624,
    TABLE = 625,
    TABLES = 626,
    TABLESAMPLE = 627,
    TABLESPACE = 628,
    TEMP = 629,
    TEMPLATE = 630,
    TEMPORARY = 631,
    TEXT_P = 632,
    THEN = 633,
    TIME = 634,
    TIMESTAMP = 635,
    TO = 636,
    TRAILING = 637,
    TRANSACTION = 638,
    TRANSFORM = 639,
    TREAT = 640,
    TRIGGER = 641,
    TRIM = 642,
    TRUE_P = 643,
    TRUNCATE = 644,
    TRUSTED = 645,
    TYPE_P = 646,
    TYPES_P = 647,
    UNBOUNDED = 648,
    UNCOMMITTED = 649,
    UNENCRYPTED = 650,
    UNION = 651,
    UNIQUE = 652,
    UNKNOWN = 653,
    UNLISTEN = 654,
    UNLOGGED = 655,
    UNTIL = 656,
    UPDATE = 657,
    USER = 658,
    USING = 659,
    VACUUM = 660,
    VALID = 661,
    VALIDATE = 662,
    VALIDATOR = 663,
    VALUE_P = 664,
    VALUES = 665,
    VARCHAR = 666,
    VARIADIC = 667,
    VARYING = 668,
    VERBOSE = 669,
    VERSION_P = 670,
    VIEW = 671,
    VIEWS = 672,
    VOLATILE = 673,
    WHEN = 674,
    WHERE = 675,
    WHITESPACE_P = 676,
    WINDOW = 677,
    WITH = 678,
    WITHIN = 679,
    WITHOUT = 680,
    WORK = 681,
    WRAPPER = 682,
    WRITE = 683,
    XML_P = 684,
    XMLATTRIBUTES = 685,
    XMLCONCAT = 686,
    XMLELEMENT = 687,
    XMLEXISTS = 688,
    XMLFOREST = 689,
    XMLPARSE = 690,
    XMLPI = 691,
    XMLROOT = 692,
    XMLSERIALIZE = 693,
    YEAR_P = 694,
    YES_P = 695,
    ZONE = 696,
    NOT_LA = 697,
    NULLS_LA = 698,
    WITH_LA = 699,
    POSTFIXOP = 700,
    UMINUS = 701
  };
#endif

/* Value type.  */
#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED

union YYSTYPE
{
#line 202 "gram.y" /* yacc.c:1909  */

	core_YYSTYPE		core_yystype;
	/* these fields must match core_YYSTYPE: */
	int					ival;
	char				*str;
	const char			*keyword;

	char				chr;
	bool				boolean;
	JoinType			jtype;
	DropBehavior		dbehavior;
	OnCommitAction		oncommit;
	List				*list;
	Node				*node;
	Value				*value;
	ObjectType			objtype;
	TypeName			*typnam;
	FunctionParameter   *fun_param;
	FunctionParameterMode fun_param_mode;
	FuncWithArgs		*funwithargs;
	DefElem				*defelt;
	SortBy				*sortby;
	WindowDef			*windef;
	JoinExpr			*jexpr;
	IndexElem			*ielem;
	Alias				*alias;
	RangeVar			*range;
	IntoClause			*into;
	WithClause			*with;
	InferClause			*infer;
	OnConflictClause	*onconflict;
	A_Indices			*aind;
	ResTarget			*target;
	struct PrivTarget	*privtarget;
	AccessPriv			*accesspriv;
	struct ImportQual	*importqual;
	InsertStmt			*istmt;
	VariableSetStmt		*vsetstmt;
	PartitionElem		*partelem;
	PartitionSpec		*partspec;
	PartitionRangeDatum	*partrange_datum;
	RoleSpec			*rolespec;

#line 545 "gram.h" /* yacc.c:1909  */
};

typedef union YYSTYPE YYSTYPE;
# define YYSTYPE_IS_TRIVIAL 1
# define YYSTYPE_IS_DECLARED 1
#endif

/* Location type.  */
#if ! defined YYLTYPE && ! defined YYLTYPE_IS_DECLARED
typedef struct YYLTYPE YYLTYPE;
struct YYLTYPE
{
  int first_line;
  int first_column;
  int last_line;
  int last_column;
};
# define YYLTYPE_IS_DECLARED 1
# define YYLTYPE_IS_TRIVIAL 1
#endif



int base_yyparse (core_yyscan_t yyscanner);

#endif /* !YY_BASE_YY_GRAM_H_INCLUDED  */
