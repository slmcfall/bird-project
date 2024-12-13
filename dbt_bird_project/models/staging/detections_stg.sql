select * from {{ source('birdweather', 'detections') }}
