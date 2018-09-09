-- relations
create table attribute_relations (
    super_sid text,
    sub_sid text
);

-- files
create table content_profiles (
    sid text primary key,
    content_path text
);

-- mails
create table mail_profiles (
    sid text primary key,
    judge text
);
create table mail_profile_sets (
    sid text primary key
);

-- models
create table models (
    sid text primary key
);
create table samples (
    sid text primary key,
    word text
);
create table sample_spaces (
    sid text primary key
);
create table events (
    sid text primary key,
    value_map text
);
create table probability_spaces (
    sid text primary key,
    cardinality integer
);
create table probabilities (
    sid text primary key
);
