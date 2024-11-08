// Global variables for Plyr and current track
let plyr;
let currentTrackIndex = 0;
let tracks = [
    {
        title: "Track Title 1",
        artist: "Artist Name 1",
        url: "path_to_your_audio_file_1.mp3", // Replace with actual track URL
        cover: "path_to_your_album_cover_1.jpg" // Replace with actual cover image URL
    },
    {
        title: "Track Title 2",
        artist: "Artist Name 2",
        url: "path_to_your_audio_file_2.mp3", // Replace with actual track URL
        cover: "path_to_your_album_cover_2.jpg" // Replace with actual cover image URL
    }
    // Add more tracks as needed
];

// Load the first track and initialize Plyr
window.onload = function() {
    loadTrack(currentTrackIndex);
    const audioPlayer = document.getElementById('audioPlayer');
    plyr = new Plyr(audioPlayer);
};

// Load track information and set Plyr source
function loadTrack(index) {
    currentTrackIndex = index;

    // Set the new source for Plyr
    const audioSource = document.getElementById('audioSource');
    audioSource.src = tracks[currentTrackIndex].url;
    plyr.source = {
        type: 'audio',
        sources: [
            {
                src: tracks[currentTrackIndex].url,
                type: 'audio/mp3',
            },
        ],
    };

    document.getElementById('albumCover').src = tracks[currentTrackIndex].cover;
    document.getElementById('trackTitle').innerText = tracks[currentTrackIndex].title;
    document.getElementById('trackArtist').innerText = tracks[currentTrackIndex].artist;
}

// Sample function to simulate searching for beats (implement as needed)
function searchBeats() {
    alert("Search functionality is not yet implemented.");
}

// Sample function to create a playlist (implement as needed)
function createPlaylist() {
    alert("Create playlist functionality is not yet implemented.");
}
