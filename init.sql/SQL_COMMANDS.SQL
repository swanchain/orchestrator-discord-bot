create table users
(
    id                  serial
        primary key,
    discord_id          varchar,
    discord_name        varchar,
    from_wallet_address varchar,
    to_wallet_address   varchar,
    last_claim_time     timestamp,
    claimed_amount      double precision,
    transaction_hash    varchar,
    token_symbol        varchar
);

create table config
(
    id        serial
        constraint config_pk
            primary key,
    key       varchar           not null,
    value     varchar           not null,
    is_active integer default 1 not null
);
