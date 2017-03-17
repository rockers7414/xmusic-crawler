CREATE EXTENSION pgcrypto;

CREATE FUNCTION update_modtime() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
  BEGIN
    NEW.updated_time = NOW();
    RETURN NEW;
  END;
$$;

CREATE TABLE IF NOT EXISTS genres (
    genre_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(32) UNIQUE NOT NULL
);

CREATE UNIQUE INDEX idx_genres_name ON genres(name);

CREATE TABLE IF NOT EXISTS providers (
    provider_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(32) UNIQUE NOT NULL
);

CREATE UNIQUE INDEX idx_providers_name ON providers(name);

INSERT INTO providers(name) VALUES('youtube'), ('spotify');

CREATE TABLE IF NOT EXISTS artists (
    artist_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    provider_id UUID REFERENCES providers(provider_id) NOT NULL,
    provider_res_id VARCHAR(256) NOT NULL,
    name VARCHAR(32) NOT NULL,
    popularity BIGINT,
    UNIQUE(provider_id, provider_res_id)
);

CREATE INDEX idx_artists_name ON artists(name);
CREATE INDEX idx_artists_popularity ON artists(popularity);
CREATE INDEX idx_artists_provider_id ON artists(provider_id);
CREATE INDEX idx_artists_provider_res_id ON artists(provider_res_id);

CREATE TABLE IF NOT EXISTS albums (
    album_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    artist_id UUID REFERENCES artists(artist_id) NOT NULL,
    provider_id UUID REFERENCES providers(provider_id) NOT NULL,
    provider_res_id VARCHAR(256) NOT NULL,
    name VARCHAR(32) NOT NULL,
    popularity BIGINT,
    UNIQUE(provider_id, provider_res_id)
);

CREATE INDEX idx_albums_name ON albums(name);
CREATE INDEX idx_albums_artis_id ON albums(artist_id);
CREATE INDEX idx_albums_popularity ON albums(popularity);
CREATE INDEX idx_albums_provider_id ON albums(provider_id);
CREATE INDEX idx_albums_provider_res_id ON albums(provider_res_id);

CREATE TABLE IF NOT EXISTS tracks (
    track_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    album_id UUID REFERENCES albums(album_id) NOT NULL,
    name VARCHAR(512) NOT NULL,
    popularity BIGINT,
    track_number INT,
    lyric TEXT
);

CREATE INDEX idx_tracks_name ON tracks(name);
CREATE INDEX idx_tracks_album_id ON tracks(album_id);
CREATE INDEX idx_tracks_popularity ON tracks(popularity);
CREATE INDEX idx_tracks_lyric ON tracks(lyric);

CREATE TABLE IF NOT EXISTS repository (
    track_id UUID REFERENCES tracks(track_id) NOT NULL,
    provider_id UUID REFERENCES providers(provider_id) NOT NULL,
    link VARCHAR(512) NOT NULL,
    duration_second INT,
    updated_time TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_repository_track_id ON repository(track_id);
CREATE INDEX idx_repository_provider_id ON repository(provider_id);

CREATE TRIGGER update_repository_modtime BEFORE UPDATE ON repository FOR EACH ROW EXECUTE PROCEDURE update_modtime();

CREATE TABLE IF NOT EXISTS images (
    image_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    width INT NOT NULL,
    height INT NOT NULL,
    path VARCHAR(1024) NOT NULL
);

CREATE INDEX idx_images_name ON images(width);
CREATE INDEX idx_images_popularity ON images(height);

CREATE TABLE IF NOT EXISTS artists_images (
    artist_id UUID REFERENCES artists(artist_id) NOT NULL,
    image_id UUID REFERENCES images(image_id) NOT NULL
);

CREATE TABLE IF NOT EXISTS albums_images (
    album_id UUID REFERENCES albums(album_id) NOT NULL,
    image_id UUID REFERENCES images(image_id) NOT NULL
);

CREATE TABLE IF NOT EXISTS artists_genres (
    artist_id UUID REFERENCES artists(artist_id) NOT NULL,
    genre_id UUID REFERENCES genres(genre_id) NOT NULL
);

CREATE TABLE IF NOT EXISTS albums_genres (
    album_id UUID REFERENCES albums(album_id),
    genre_id UUID REFERENCES genres(genre_id)
);

CREATE TABLE IF NOT EXISTS tracks_genres (
    track_id UUID REFERENCES tracks(track_id),
    genre_id UUID REFERENCES genres(genre_id)
);
