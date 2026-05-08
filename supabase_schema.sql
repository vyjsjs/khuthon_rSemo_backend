-- 문화 정류장 DB 스키마
-- Supabase SQL Editor에 붙여넣기

CREATE TABLE users (
    id        BIGSERIAL PRIMARY KEY,
    role      TEXT NOT NULL CHECK (role IN ('resident', 'artist')),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE artists (
    user_id            BIGINT PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    display_name       TEXT NOT NULL,
    genres             TEXT,
    activity_radius_km FLOAT DEFAULT 5.0,
    base_latitude      FLOAT,
    base_longitude     FLOAT,
    is_available       BOOLEAN DEFAULT TRUE
);

CREATE TABLE stations (
    id               BIGSERIAL PRIMARY KEY,
    latitude         FLOAT NOT NULL,
    longitude        FLOAT NOT NULL,
    address          TEXT,
    capacity         INTEGER DEFAULT 50,
    supported_genres TEXT,
    hourly_cost      FLOAT DEFAULT 0,
    is_active        BOOLEAN DEFAULT TRUE
);

CREATE TABLE checkins (
    id                 BIGSERIAL PRIMARY KEY,
    user_id            BIGINT REFERENCES users(id) ON DELETE CASCADE,
    station_id         BIGINT REFERENCES stations(id) ON DELETE CASCADE,
    genre              TEXT NOT NULL,
    preferred_timeslot TEXT,
    created_at         TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE matches (
    id           BIGSERIAL PRIMARY KEY,
    station_id   BIGINT REFERENCES stations(id),
    artist_id    BIGINT REFERENCES artists(user_id),
    genre        TEXT NOT NULL,
    demand_count INTEGER DEFAULT 0,
    status       TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'accepted', 'rejected')),
    responded_at TIMESTAMPTZ,
    created_at   TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE events (
    id           BIGSERIAL PRIMARY KEY,
    match_id     BIGINT UNIQUE REFERENCES matches(id),
    scheduled_at TIMESTAMPTZ NOT NULL,
    status       TEXT NOT NULL DEFAULT 'scheduled' CHECK (status IN ('scheduled', 'completed', 'canceled')),
    created_at   TIMESTAMPTZ DEFAULT NOW()
);
