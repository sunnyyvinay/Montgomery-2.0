import React, { useRef, useEffect } from 'react';

export default function VideoComponent({ videoUrl }) {
  const videoRef = useRef(null);

  // Play the video when videoUrl changes
  useEffect(() => {
    if (videoRef.current && videoUrl) {
      videoRef.current.src = videoUrl; // Update the video source
      videoRef.current.load();         // Reload the video
      videoRef.current.play();         // Autoplay the video
    }
  }, [videoUrl]);  // Runs only when videoUrl changes

  return (
    <div style={{ width: '100%', height: '100%', overflow: 'hidden' }}>
      <video
        ref={videoRef}
        style={{ width: '100%', height: '100%', objectFit: 'cover' }} // Ensure the video covers the available space
        autoPlay
        playsInline  // Ensures inline playback on mobile devices
      >
        <source src={videoUrl} type="video/mp4" />
        Your browser does not support the video tag.
      </video>
    </div>
  );
}
