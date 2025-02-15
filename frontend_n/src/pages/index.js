import { useState } from "react";
import { Box, Flex } from "@chakra-ui/react";
import SideBar from "@/components/sidebar";
import UserInput from "@/components/userinput";
import Spline from "@splinetool/react-spline";
import TypewriterText from "@/components/typewriter";
import VideoComponent from "@/components/video";  // Import VideoComponent

export default function Home() {
  const [videoUrl, setVideoUrl] = useState(null);  // State to store the video URL
  const [showTypewriter, setShowTypewriter] = useState(false);  // State to toggle TypewriterText visibility
  const [userInputValue, setUserInputValue] = useState("");  // State for the user input field

  // Function to update the user input value when an item from the sidebar is clicked
  const handleAutoFill = (value) => {
    setUserInputValue(value);  // Autofill the user input with the clicked value
  };

  // Function passed to UserInput to handle the API response (the video blob URL)
  const handleUserInputResponse = (url) => {
    setVideoUrl(url);  // Update the state with the video URL
    setShowTypewriter(false);  // Hide the Typewriter when video is displayed
  };

  // Toggle the visibility of the TypewriterText when Spline is clicked
  const handleSplineClick = () => {
    setShowTypewriter((prev) => !prev);  // Toggle showTypewriter state
  };

  // Reset the state to show Spline without TypewriterText when EditIcon is clicked
  const handleReset = () => {
    setVideoUrl(null);  // Reset the video URL
    setShowTypewriter(false);  // Keep Typewriter hidden on reset
  };

  return (
    <Flex minHeight="100vh" width="100%">
      {/* Sidebar */}
      <Box
        width="25%"
        bg="gray.100"
        p="4"
        boxShadow="md"
        position="fixed"
        height="100vh"
        left={0}
        top={0}
      >
        {/* Pass the handleAutoFill function to the sidebar */}
        <SideBar onReset={handleReset} onAutoFill={handleAutoFill} />
      </Box>

      {/* Main content area for Spline or Video */}
      <Box
        flex="1"
        ml="25%"
        display="flex"
        flexDirection="column"
        justifyContent="center"
        alignItems="center"
        height="100vh"
        position="relative"
        overflow="hidden"
      >
        {!videoUrl ? (
          <Box width="100%" height="100%" position="relative">
            {/* Spline Component */}
            <Spline 
              scene="https://prod.spline.design/NiiiQrjNKkVNlTYO/scene.splinecode" 
              onClick={handleSplineClick}
            />

            {/* Conditionally render TypewriterText based on showTypewriter */}
            {showTypewriter && (
              <Box
                position="absolute"
                top="45%"
                left="50%"
                transform="translate(-50%, -50%)"
              >
                <TypewriterText />
              </Box>
            )}
          </Box>
        ) : (
          <Box flex="1" width="100%" height="100%" position="relative">
            {/* Pass the blob URL to VideoComponent */}
            <VideoComponent videoUrl={videoUrl} />
          </Box>
        )}

        {/* UserInput component at the bottom */}
        <Box
          position="absolute"
          bottom="0"
          left="0"
          width="100%"
          zIndex="10"
          height="10vh"
        >
          <UserInput 
            onApiResponse={handleUserInputResponse} 
            inputValue={userInputValue}  // Pass the input value for autofill
            setInputValue={setUserInputValue}  // Pass function to update input value
          />
        </Box>
      </Box>
    </Flex>
  );
}
