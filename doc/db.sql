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

CREATE TABLE IF NOT EXISTS datasources (
    source_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(32) UNIQUE NOT NULL
);

CREATE UNIQUE INDEX idx_datasources_name ON datasources(name);

CREATE TABLE IF NOT EXISTS artists (
    artist_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(32) NOT NULL,
    popularity BIGINT
);

CREATE INDEX idx_artists_name ON artists(name);
CREATE INDEX idx_artists_popularity ON artists(popularity);

CREATE TABLE IF NOT EXISTS albums (
    album_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    artist_id UUID REFERENCES artists(artist_id),
    name VARCHAR(32) NOT NULL,
    popularity BIGINT
);

CREATE INDEX idx_albums_name ON albums(name);
CREATE INDEX idx_albums_popularity ON albums(popularity);

CREATE TABLE IF NOT EXISTS tracks (
    track_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    album_id UUID REFERENCES albums(album_id),
    name VARCHAR(512) NOT NULL,
    popularity BIGINT,
    track_number INT
);

CREATE INDEX idx_tracks_name ON tracks(name);
CREATE INDEX idx_tracks_popularity ON tracks(popularity);

CREATE TABLE IF NOT EXISTS repository (
    track_id UUID REFERENCES tracks(track_id),
    source_id UUID REFERENCES datasources(source_id),
    link VARCHAR(512) NOT NULL,
    duration_second INT,
    updated_time TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

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
    artist_id UUID REFERENCES artists(artist_id),
    image_id UUID REFERENCES images(image_id)
);

CREATE TABLE IF NOT EXISTS albums_images (
    album_id UUID REFERENCES albums(album_id),
    image_id UUID REFERENCES images(image_id)
);

CREATE TABLE IF NOT EXISTS artists_genres (
    artist_id UUID REFERENCES artists(artist_id),
    genre_id UUID REFERENCES genres(genre_id)
);

CREATE TABLE IF NOT EXISTS albums_genres (
    album_id UUID REFERENCES albums(album_id),
    genre_id UUID REFERENCES genres(genre_id)
);

CREATE TABLE IF NOT EXISTS tracks_genres (
    track_id UUID REFERENCES tracks(track_id),
    genre_id UUID REFERENCES genres(genre_id)
);
