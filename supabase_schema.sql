-- 문화 정류장 DB 스키마
-- Supabase SQL Editor에 붙여넣기
-- 1. 유저 테이블

CREATE TABLE users (

    id         BIGSERIAL PRIMARY KEY,

    role       TEXT NOT NULL CHECK (role IN ('resident', 'artist')),

    created_at TIMESTAMPTZ DEFAULT NOW()

);



-- 2. 문화 정류장 테이블

CREATE TABLE stations (

    id               BIGSERIAL PRIMARY KEY,

    latitude         FLOAT8 NOT NULL,

    longitude        FLOAT8 NOT NULL,

    address          TEXT,

    capacity         INTEGER DEFAULT 50,

    supported_genres TEXT,

    hourly_cost      INTEGER DEFAULT 0,

    description      TEXT,

    is_active        BOOLEAN DEFAULT TRUE,

    created_at       TIMESTAMPTZ DEFAULT NOW()

);



-- 3. 체크인 테이블

CREATE TABLE checkins (

    id                 BIGSERIAL PRIMARY KEY,

    user_id            BIGINT REFERENCES users(id) ON DELETE CASCADE,

    station_id         BIGINT REFERENCES stations(id) ON DELETE CASCADE,

    genre              TEXT NOT NULL,

    preferred_timeslot TEXT,

    created_at         TIMESTAMPTZ DEFAULT NOW()

);



-- 4. 아티스트 테이블

CREATE TABLE artists (

    user_id            BIGINT PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,

    display_name       TEXT NOT NULL,

    genres             TEXT NOT NULL,

    activity_radius_km FLOAT8 DEFAULT 5.0,

    base_latitude      FLOAT8 NOT NULL,

    base_longitude     FLOAT8 NOT NULL,

    is_available       BOOLEAN DEFAULT TRUE,

    created_at         TIMESTAMPTZ DEFAULT NOW()

);



-- 5. 매칭 테이블

CREATE TABLE matches (

    id           BIGSERIAL PRIMARY KEY,

    station_id   BIGINT REFERENCES stations(id),

    artist_id    BIGINT REFERENCES artists(user_id),

    genre        TEXT NOT NULL,

    demand_count INTEGER NOT NULL,

    status       TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'accepted', 'rejected')),

    responded_at TIMESTAMPTZ,

    created_at   TIMESTAMPTZ DEFAULT NOW()

);



-- 6. 공연(이벤트) 테이블

CREATE TABLE events (

    id           BIGSERIAL PRIMARY KEY,

    match_id     BIGINT UNIQUE REFERENCES matches(id),

    scheduled_at TIMESTAMPTZ NOT NULL,

    status       TEXT NOT NULL DEFAULT 'scheduled' CHECK (status IN ('scheduled', 'completed', 'canceled')),

    created_at   TIMESTAMPTZ DEFAULT NOW()

);
-- 7. 관람 의사 확인 테이블

CREATE TABLE event_attendances (

    id         BIGSERIAL PRIMARY KEY,

    event_id   BIGINT REFERENCES events(id) ON DELETE CASCADE,

    user_id    BIGINT REFERENCES users(id) ON DELETE CASCADE,

    status     TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'confirmed', 'declined')),

    created_at TIMESTAMPTZ DEFAULT NOW(),

    UNIQUE (event_id, user_id)

);



-- 8. 공연 예매 테이블

CREATE TABLE reservations (

    id         BIGSERIAL PRIMARY KEY,

    user_id    BIGINT REFERENCES users(id) ON DELETE CASCADE,

    event_id   BIGINT REFERENCES events(id) ON DELETE CASCADE,

    created_at TIMESTAMPTZ DEFAULT NOW(),

    UNIQUE (user_id, event_id)

);



-- 9. 알림 테이블

CREATE TABLE notifications (

    id         BIGSERIAL PRIMARY KEY,

    user_id    BIGINT REFERENCES users(id) ON DELETE CASCADE,

    message    TEXT NOT NULL,

    is_read    BOOLEAN DEFAULT FALSE,

    created_at TIMESTAMPTZ DEFAULT NOW()

);