CREATE TABLE revocations (
    id UUID NOT NULL,
    bit_index INTEGER NOT NULL,
    reason TEXT,
    revoked TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

ALTER TABLE revocations OWNER TO revocation;

CREATE INDEX ix_revocations_bit_index ON revocations (bit_index);

CREATE TABLE allocations (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    last_allocated_id INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (id)
);

ALTER TABLE allocations OWNER TO revocation;
