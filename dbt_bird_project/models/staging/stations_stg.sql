select * from {{ source('birdweather', 'stations') }}
